#!/usr/bin/env python
import os
import sys

from enron_email_parser.user_parser import UserParser

parser_output_dir = 'data'


def main(args):
    print("Enron Email Parser by Gibson\n")

    if len(args) < 2 or not os.path.isdir(args[1]):
        print("Enron mail directory not supplied!")
        return False

    ENRON_MAIL_DIRECTORY = args[1]
    do_parse(ENRON_MAIL_DIRECTORY)
    return True


def do_parse(enron_mail_directory):
    user_directories = list_folders(enron_mail_directory)

    print("Found " + str(len(user_directories)) + " users")
    print("Processing...")
    print("[ ", end='', flush=True)

    user_parser = UserParser(parser_output_dir)

    for user_directory in user_directories:
        user_parser.parse_user(user_directory)
        print("|", end='', flush=True)

    print(" ]")
    print("Processing complete!")


def list_folders(directory):
    folders = []

    for folder_path in os.listdir(directory):
        folder_path_full = os.path.join(directory, folder_path)
        if os.path.isdir(folder_path_full):
            folders.append(folder_path_full)

    return folders


if __name__ == '__main__':
    main(sys.argv)
