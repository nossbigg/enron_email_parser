import datetime
import os
import pathlib
import re


class MessageParser:
    regex_headers_to_extract = {
        'message_id': (re.compile("(?<=Message-ID: ).*?(?=\n)")),
        'date': (re.compile("(?<=Date: ).*?(?=\n)")),
        'to': (re.compile("(?<=To: ).*?(?=\n[a-zA-Z-]*?: )", re.DOTALL)),
        'from': (re.compile("(?<=From: ).*?(?=\n[a-zA-Z-]*?: )", re.DOTALL)),
        'subject': (re.compile("(?<=Subject: ).*?(?=\n)")),
        'mime_version': (re.compile("(?<=Mime-Version: ).*?(?=\n)")),
        'content_type': (re.compile("(?<=Content-Type: ).*?(?=\n)")),
        'content_transfer_encoding': (re.compile(
            "(?<=Content-Transfer-Encoding: ).*?(?=\n)")),
        'x_from': (re.compile("(?<=X-From: ).*?(?=\n)")),
        'x_to': (re.compile("(?<=X-To: ).*?(?=\n)")),
        'x_cc': (re.compile("(?<=X-cc: ).*?(?=\n)")),
        'x_bcc': (re.compile("(?<=X-bcc: ).*?(?=\n)")),
        'x_folder': (re.compile("(?<=X-Folder: ).*?(?=\n)")),
        'x_origin': (re.compile("(?<=X-Origin: ).*?(?=\n)")),
        'x_filename': (re.compile("(?<=X-FileName: ).*?(?=\n)")),
        'body': (re.compile("(?<=\.(pst|PST|nsf)\n\n).*$", re.DOTALL))
    }

    @staticmethod
    def parse_message(message_path, base_dir):
        message = {}

        subdirectory_path = MessageParser.__get_subdirectory_path(message_path, base_dir)
        if len(subdirectory_path) > 0:
            message['subdirectory_path'] = subdirectory_path

        # Use ISO-8859-1 instead of UTF-8 for compatibility reasons
        message_text = pathlib.Path(message_path).read_text(encoding="ISO-8859-1")

        message.update(MessageParser.__parse_message_contents(message_text))

        return message

    @staticmethod
    def __parse_message_contents(message_text):
        message_headers = {}

        for field, matcher in MessageParser.regex_headers_to_extract.items():
            match_object = matcher.search(message_text)

            if match_object is None:
                continue
            match_content = match_object.group(0)

            if len(match_content) == 0:
                continue
            message_headers[field] = match_content

        if "to" in message_headers:
            message_headers['to'] = \
                MessageParser.convert_email_addresses_to_list(message_headers['to'])
        if "date" in message_headers:
            message_headers['date'] = \
                MessageParser.convert_datetime(message_headers['date'])
        if "x_to" in message_headers:
            message_headers['x_to'] = \
                MessageParser.convert_email_addresses_to_list(message_headers['x_to'])

        return message_headers

    @staticmethod
    def convert_email_addresses_to_list(emails_string):
        return emails_string.replace("\n", "").replace("\t", "").replace(", ", ",").strip().split(
            ",")

    @staticmethod
    def convert_datetime(datetime_string):
        datetime_without_timezone_prefix = datetime_string[:-6]
        return datetime.datetime.strptime(datetime_without_timezone_prefix,
                                          "%a, %d %b %Y %H:%M:%S %z")

    @staticmethod
    def __get_subdirectory_path(full_path, base_dir):
        return os.path.dirname(full_path).replace(base_dir, '')
