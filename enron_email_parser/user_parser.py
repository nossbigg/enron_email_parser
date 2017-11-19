import glob
import os

from enron_email_parser import save_to_disk_util
from enron_email_parser.message_parser import MessageParser


class UserParser:
    def __init__(self, parser_output_dir):
        self.message_parser = MessageParser()

        self.parser_output_dir = parser_output_dir

    def parse_user(self, user_directory):
        user_name = os.path.basename(user_directory)
        user_folders = UserParser.__list_folders(user_directory)

        user_contents = {}
        for folder in user_folders:
            current_directory_name = os.path.basename(folder)
            folder_contents = self.__parse_user_folder(os.path.join(folder))
            user_contents[current_directory_name] = folder_contents

        user_dict = {user_name: user_contents}
        save_path = os.path.join(os.getcwd(), self.parser_output_dir, user_name + ".gz")

        save_to_disk_util.save_to_disk(save_path, user_dict)

    def __parse_user_folder(self, user_folder):
        messages = {}

        message_paths = [message_path
                         for message_path in
                         glob.glob(os.path.join(user_folder, "**"), recursive=True)
                         if not os.path.isdir(message_path)]

        for message_path in message_paths:
            message_filename = os.path.basename(message_path)

            try:
                subdirectory_path = UserParser.__get_subdirectory_path(message_path, user_folder)
                message_filename_key = subdirectory_path + "/" + message_filename
                message_contents = self.message_parser.parse_message(message_path, user_folder)

                messages[message_filename_key] = message_contents

            except UnicodeDecodeError:
                print("Could not parse '" + message_path + "'\n")

        return messages

    @staticmethod
    def __get_subdirectory_path(full_path, base_dir):
        return os.path.dirname(full_path).replace(base_dir, '')

    @staticmethod
    def __list_folders(directory):
        return [os.path.join(directory, d)
                for d in os.listdir(directory)
                if os.path.isdir(os.path.join(directory, d))]
