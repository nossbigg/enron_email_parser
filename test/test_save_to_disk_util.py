from unittest import TestCase
from unittest.mock import patch, MagicMock

import callee

from enron_email_parser import save_to_disk_util


class TestSaveToDiskUtil(TestCase):
    @patch('pickle.dump')
    @patch('gzip.open')
    @patch('pathlib.Path')
    @patch('os.path.dirname')
    def test_save_to_disk(self,
                          mock_os_path_dirname,
                          mock_pathlib_path,
                          mock_gzip_open,
                          mock_pickle_dump):
        mock_path = MagicMock()
        mock_os_path_dirname.return_value = "/dirname"
        mock_pathlib_path.return_value = mock_path

        some_dict = {"some-key": "some-value"}
        some_full_path = "/dirname/filename"

        save_to_disk_util.save_to_disk(some_full_path, some_dict, -1)

        mock_os_path_dirname.assert_called_with(some_full_path)
        mock_pathlib_path.assert_called_with("/dirname")
        mock_path.mkdir.assert_called_once()
        mock_path.mkdir.assert_called_with(parents=True, exist_ok=True)
        mock_pickle_dump.assert_called_with(some_dict, callee.Any(), -1)
