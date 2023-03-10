import pytest
import os
from astropy import units as u
from atlast_sc.utils import FileHelper

TEST_FILES_PATH = os.path.join(os.path.dirname(__file__), '../test_files')


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
               f'Must be one of: {FileHelper.SUPPORTED_FILE_EXTENSIONS}'

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
                           tmp_output_dir):
        """
        Test that a file of the appropriate type and with the correct
        name is written to the correct location with the correct data.
        Provides an indirect test of _to_yaml, _to_json,
        and _to_txt.
        """

        test_data = {
            "param1": 1*u.m,
            'param2': 10*u.GHz,
            'param3': 2
        }

        FileHelper.write_to_file(test_data, tmp_output_dir,
                                 file_name, file_type)

        # Make sure the file has been written
        expected_file_name = file_name + '.' + file_type
        assert expected_file_name in os.listdir(tmp_output_dir)

        # Make sure the file has been written in a format that allows it
        # to be read by the FileHelper to produce an appropriately formatted
        # dictionary that could be used by the Calculator.
        expected_dict = {
            'param1': {
                'value': 1,
                'unit': 'm'
            },
            'param2': {
                'value': 10,
                'unit': 'GHz'
            },
            'param3': {
                'value': 2
            }
        }

        result_dict = \
            FileHelper.read_from_file(tmp_output_dir,
                                      expected_file_name)
        assert result_dict == expected_dict

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
               f'Must be one of: {FileHelper.SUPPORTED_FILE_EXTENSIONS}'
