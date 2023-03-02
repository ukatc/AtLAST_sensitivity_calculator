import pytest
import os
from atlast_sc.utils import FileHelper

TEST_FILES_PATH = os.path.join(os.path.dirname(__file__), 'test_files')


class TestFileHelper:

    def test_read_from_file(self):
        """
        Test that a dictionary is generated from data in a file
        """
        test_file = 'test_input_file.yaml'

        result = FileHelper.read_from_file(TEST_FILES_PATH, test_file)
        expected_result = {
            'sensitivity': {
                'value': 0,
                'unit': 'mJy'
            },
            't_int': {
                'value': 100,
                'unit': 's'
            }
        }

        assert result == expected_result

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
        Test that the appropriate file reader function is returned
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
        Test that an error is reported if the file type is not supported
        """

        with pytest.raises(ValueError) as e:
            FileHelper._get_reader(file_name)
        print(e)
        # TODO: pick up from here. What's the best way to get the exception
        #   message? Logger?? https://realpython.com/python-logging/
        #
        # print(repr(e))
        # assert "" + str(e) == f"Unsupported file type {extension}. " \
        #                  f"Must be one of: "
        #                  F"{FileHelper.SUPPORTED_FILE_EXTENSIONS}"

    def test__dict_from_yaml(self):
        pass

    def test__dict_from_json(self):
        pass

    def test__dict_from_txt(self):
        pass

    def test_write_to_file(self):
        pass
