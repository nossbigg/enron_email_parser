#!/usr/bin/env python
import os
import sys

from enron_email_parser.user_parser import UserParser

parser_output_dir = 'data'


def main(args):
    print("Enron Email Parser by Gibson\n")

    if not os.path.isdir(args[1]):
        print("Enron mail directory not supplied!")
        return

    ENRON_MAIL_DIRECTORY = args[1]

    do_parse(ENRON_MAIL_DIRECTORY)


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
    return [os.path.join(directory, d)
            for d in os.listdir(directory)
            if os.path.isdir(os.path.join(directory, d))]


if __name__ == '__main__':
    main(sys.argv)
