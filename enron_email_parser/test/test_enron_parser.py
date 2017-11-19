from unittest import TestCase
from unittest.mock import patch, call

from enron_email_parser import enron_parser


class TestEnronParser(TestCase):
    @patch('os.path.isdir')
    def test_main_fail_on_missing_argument(self, mock_os_path_isdir):
        mock_os_path_isdir.return_value = False

        self.assertFalse(enron_parser.main([]))

    @patch('enron_email_parser.enron_parser.UserParser')
    @patch('os.path.join')
    @patch('os.listdir')
    @patch('os.path.isdir')
    def test_do_parse(self,
                      mock_os_path_isdir,
                      mock_os_listdir,
                      mock_os_path_join,
                      mock_user_parser):
        mock_os_path_isdir.return_value = True
        mock_os_listdir.return_value = ['dir-1', 'dir-2']
        joined_dirs = ['joined-dir-1', 'joined-dir-2']
        mock_os_path_join.side_effect = joined_dirs

        main_result = enron_parser.main(["total-garbage", "some-maildir-path"])

        self.assertTrue(main_result)

        expected_user_parser_calls = [call().parse_user('joined-dir-1'),
                                      call().parse_user('joined-dir-2')]
        mock_user_parser.assert_has_calls(expected_user_parser_calls, any_order=True)
