import pytest
import os
import astropy.units as u
from atlast_sc.utils import Decorators
from atlast_sc.utils import FileHelper
from atlast_sc.utils import DataHelper
from atlast_sc.calculator import Calculator
from tests.utils import does_not_raise
# from tests.utils import MockCalculator


TEST_FILES_PATH = os.path.join(os.path.dirname(__file__), '../test_files')


class TestDecorators:

    class MockCalculator:

        def __init__(self):
            self._value = 1
            self._quantity = 1 * u.GHz
            self._calculation_inputs = \
                TestDecorators.MockCalculator.MockCalculationInputs()

        class MockCalculationInputs:
            @staticmethod
            def validate_update(param, value):
                if value == "invalid":
                    raise ValueError

                return True

        @property
        def prop1(self):
            return 1

        @property
        def prop2(self):
            return 2.0

        @property
        def prop3(self):
            return '3'

        @property
        def decorated_validate_update(self):
            return self._value

        @decorated_validate_update.setter
        @Decorators.validate_update
        def decorated_validate_update(self, new_value):
            self._value = new_value

        @property
        def decorated_validate_and_update_params(self):
            return self._quantity

        @decorated_validate_and_update_params.setter
        @Decorators.validate_and_update_params
        def decorated_validate_and_update_params(self, new_quantity):
            self._quantity = new_quantity

        @property
        def calculation_inputs(self):
            return self._calculation_inputs

        @staticmethod
        def _calculate_derived_parameters():
            pass

    @staticmethod
    def mock__do_validation(*args):
        if args[2] == 'invalid':
            raise ValueError

    @pytest.mark.parametrize(
        'new_value,expect_raises,expect_value_updated',
        [
            (2, does_not_raise(), True),
            ('invalid', pytest.raises(ValueError), False)
        ]
    )
    def test_validate_update(self, new_value, expect_raises,
                             expect_value_updated, mocker):

        mock_calculator = TestDecorators.MockCalculator()

        # Patch _do_validation and check it was called with the correct params
        mocker.patch(__name__ + '.Decorators._do_validation',
                     side_effect=TestDecorators.mock__do_validation)
        do_validation_spy = mocker.spy(Decorators, '_do_validation')

        with expect_raises:
            mock_calculator.decorated_validate_update = new_value
            do_validation_spy\
                .assert_called_once_with(mock_calculator,
                                         'decorated_validate_update',
                                         new_value)
        # Check that the value was updated only if the validation function
        # did not raise an error
        if expect_value_updated:
            assert mock_calculator.decorated_validate_update == new_value
        else:
            assert mock_calculator.decorated_validate_update == 1

    @pytest.mark.parametrize(
        'new_value,expect_raises,expect_value_updated,'
        'expect_params_recalculated',
        [
            (2 * u.GHz, does_not_raise(), True, True),
            (1 * u.GHz, does_not_raise(), True, False),
            (1 * u.MHz, does_not_raise(), True, True),
            ('invalid', pytest.raises(ValueError), False, False)
        ]
    )
    def test_validate_and_update_params(self, new_value, expect_raises,
                                        expect_value_updated,
                                        expect_params_recalculated,
                                        mocker):

        mock_calculator = TestDecorators.MockCalculator()

        # Patch the _do_validation function and check it was called with
        # the correct params
        mocker.patch(__name__ + '.Decorators._do_validation',
                     side_effect=TestDecorators.mock__do_validation)
        do_validation_spy = mocker.spy(Decorators, '_do_validation')

        calculate_derived_params_spy = \
            mocker.spy(TestDecorators.MockCalculator,
                       '_calculate_derived_parameters')

        with expect_raises:
            mock_calculator.decorated_validate_and_update_params = new_value
            do_validation_spy\
                .assert_called_once_with(
                    mock_calculator,
                    'decorated_validate_and_update_params',
                    new_value)

        # Check that the value was updated only if the validation function
        # did not raise an error
        if expect_value_updated:
            assert mock_calculator.decorated_validate_and_update_params == \
                   new_value
        else:
            assert mock_calculator.decorated_validate_and_update_params == \
                   1 * u.GHz

        # Check that the params were recalculated if the new value differs from
        # the old
        if expect_params_recalculated:
            calculate_derived_params_spy.assert_called_once()
        else:
            calculate_derived_params_spy.assert_not_called()

    @pytest.mark.parametrize(
        'param_name,value,expect_raises,expect_validation_performed,scenario',
        [
            ('prop1', 2, pytest.raises(ValueError), False,
             'Validate update int with int (ints are converted to floats, '
             'so this will fail because converted value is of wrong type)'),
            ('prop1', '2', pytest.raises(ValueError), False,
             'Validate update int with string'),
            ('prop1', 2.0, pytest.raises(ValueError), False,
             'Validate update int with float'),
            ('prop2', 1.0, does_not_raise(), True,
             'Validate update float with float'),
            ('prop2', 1, does_not_raise(), True,
             'Validate update float with int (ints are converted to floats)'),
            ('prop3', '2', does_not_raise(), True,
             'Validate update string with string'),
            ('prop3', 2, pytest.raises(ValueError), False,
             'Validate update string with int'),
            ('prop3', 'invalid', pytest.raises(ValueError), True,
             'Invalid parameter value')
        ])
    def test__do_validation(self, param_name, value, expect_raises,
                            expect_validation_performed, scenario,
                            mocker):

        mock_calculator = TestDecorators.MockCalculator()

        with expect_raises as e:
            validate_update_spy = \
                mocker.spy(TestDecorators.MockCalculator.MockCalculationInputs,
                           'validate_update')

            Decorators._do_validation(mock_calculator, param_name, value)

            if expect_validation_performed:
                validate_update_spy.assert_called_once_with(param_name, value)
            else:
                validate_update_spy.assert_not_called()


class TestFileHelper:

    test_files = ['test_input_file.yaml',
                  'test_input_file.json',
                  'test_input_file.txt']

    @pytest.mark.parametrize('test_file', test_files)
    def test_read_from_file(self, test_file):
        """
        Test that a dictionary is generated from data in a file.
        Provides an indirect test of _dict_from_yaml, _dict_from_json,
        and _dict_from_txt.
        """
        result = FileHelper.read_from_file(TEST_FILES_PATH, test_file)

        expected_result = {
            'sensitivity': {
                'value': 0,
                'unit': 'mJy'
            },
            't_int': {
                'value': 100,
                'unit': 's'
            },
            'n_pol': {
                'value': 2
            }
        }

        assert result == expected_result

    def test_read_from_file_raises_error(self):
        """
        Test that an error is raised if any of the values in an input
        file are non-numeric.
        """

        test_file = 'test_input_file_invalid.yaml'

        with pytest.raises(TypeError) as e:
            FileHelper.read_from_file(TEST_FILES_PATH, test_file)

        assert str(e.value) == \
               'Value "badvalue" is invalid for parameter "sensitivity". ' \
               'Parameter values must be numeric.'

    file_names = [
        ('test_file.yaml', FileHelper._dict_from_yaml),
        ('test_file.yml', FileHelper._dict_from_yaml),
        ('test_file.json', FileHelper._dict_from_json),
        ('test_file.JSON', FileHelper._dict_from_json),
        ('test_file.txt', FileHelper._dict_from_txt),
    ]

    @pytest.mark.parametrize("file_name,expected_reader", file_names)
    def test__get_reader(self, file_name, expected_reader):
        """
        Test that the appropriate file reader function is returned.
        """

        file_reader = FileHelper._get_reader(file_name)
        assert file_reader == expected_reader

    invalid_file_names = [
        ('test_file.text', 'text'),
        ('test_file', '')
    ]

    @pytest.mark.parametrize("file_name,extension", invalid_file_names)
    def test__get_reader_raises_error(self, file_name, extension):
        """
        Test that an error is reported if the file type is not supported.
        """

        with pytest.raises(ValueError) as e:
            FileHelper._get_reader(file_name)

        assert str(e.value) == \
               f'Unsupported file type "{extension}". ' \
               f'Must be one of: {FileHelper._SUPPORTED_FILE_EXTENSIONS}'

    ill_formatted_txt_files = [
        ('test_input_file_ill_formatted_1.txt',
         'No "="', ValueError),
        ('test_input_file_ill_formatted_2.txt',
         'No space between value and unit', TypeError)
    ]

    @pytest.mark.parametrize('test_file,scenario,expected_error',
                             ill_formatted_txt_files)
    def test_read_from_file_txt_file_errors(self, test_file, scenario,
                                            expected_error):
        """
        Test that appropriate errors are captured for txt files that do
        not follow the correct format (i.e., expect "=" between parameter
        name and value, and expect space between value and unit).
        """

        print(f'\nTesting scenario: {scenario}')

        with pytest.raises(expected_error):
            FileHelper.read_from_file(TEST_FILES_PATH, test_file)

    output_file_info = [
        ('output_params', 'txt'),
        ('output_params', 'yaml'),
        ('output_params', 'yml'),
        ('output_params', 'json'),
    ]

    @pytest.mark.parametrize('file_name,file_type',
                             output_file_info)
    def test_write_to_file(self, file_name, file_type,
                           tmp_output_dir, calculator):
        """
        Test that a file of the appropriate type and with the correct
        name is written to the correct location with the correct data.
        Provides an indirect test of _to_yaml, _to_json,
        and _to_txt.
        """

        FileHelper.write_to_file(calculator, tmp_output_dir,
                                 file_name, file_type)

        # Make sure the file has been written
        expected_file_name = file_name + '.' + file_type
        assert expected_file_name in os.listdir(tmp_output_dir)

        # Make sure the file has been written in a format that allows it
        # to be read by the FileHelper to produce an appropriately formatted
        # dictionary that could be used by the Calculator.
        expected_params = ['t_int', 'sensitivity', 'bandwidth', 'n_pol',
                           'obs_freq', 'weather', 'elevation', 'tau_atm',
                           'T_atm', 'T_rx', 'eta_a', 'eta_s', 'T_sys',
                           'sefd']
        # sort the expected parameters
        expected_params.sort()

        result_dict = \
            FileHelper.read_from_file(tmp_output_dir,
                                      expected_file_name)
        # list and sort the results dictionary keys
        result_dict_keys = list(result_dict.keys())
        result_dict_keys.sort()

        assert result_dict_keys == expected_params

        # Create a new calculator with the subset of parameters from
        # result_dict
        input_params = {key: val for key, val in result_dict.items()
                        if key in
                        ['t_int', 'sensitivity', 'bandwidth', 'n_pol',
                         'obs_freq', 'weather', 'elevation']}
        new_calculator = Calculator(input_params)

        assert new_calculator.user_input == \
               calculator.user_input
        assert new_calculator.instrument_setup == \
               calculator.instrument_setup
        assert new_calculator.derived_parameters == \
               calculator.derived_parameters

    file_types = [
        ('yaml', FileHelper._to_yaml),
        ('yml', FileHelper._to_yaml),
        ('json', FileHelper._to_json),
        ('JSON', FileHelper._to_json),
        ('txt', FileHelper._to_txt),
    ]

    @pytest.mark.parametrize("file_type,expected_writer", file_types)
    def test__get_writer(self, file_type, expected_writer):
        """
        Test that the appropriate file writer function is returned.
        """

        file_writer = FileHelper._get_writer(file_type)
        assert file_writer == expected_writer

    def test__get_writer_raises_error(self):
        """
        Test that an error is reported if the file type is not supported.
        """

        bad_file_type = 'notafiletype'

        with pytest.raises(ValueError) as e:
            FileHelper._get_writer(bad_file_type)

        assert str(e.value) == \
               f'Unsupported file type "{bad_file_type}". ' \
               f'Must be one of: {FileHelper._SUPPORTED_FILE_EXTENSIONS}'


class TestDataHelper:

    test_conversion_data = [
        ('GHz', ['GHz', 'MHz'], {'GHz': 1, 'MHz': 0.001}),
        ('s', ['s', 'min', 'h'], {'s': 1, 'min': 60, 'h': 3600}),
        ('h', ['s', 'min', 'h'], {'s': 1/3600, 'min': 1/60, 'h': 1})
    ]

    def test__convert(self):
        test_value = 1000
        test_unit = "MHz"
        target_unit = "GHz"

        result = DataHelper._convert(test_value, test_unit, target_unit)

        assert result == 1

    @pytest.mark.parametrize('default_unit,allowed_units,expected_result',
                             test_conversion_data)
    def test_data_conversion_factors(self, default_unit, allowed_units,
                                     expected_result):

        result = DataHelper.data_conversion_factors(default_unit,
                                                    allowed_units)

        assert result == expected_result
