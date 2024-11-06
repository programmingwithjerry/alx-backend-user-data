#!/usr/bin/env python3
"""
Handling Personal Data
"""

import logging
import os
import re
from typing import List
import mysql.connector


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction_text: str, log_message: str,
                 delimiter: str) -> str:
    """ Replace field values with a redacted string in the log message """
    for field in fields:
        log_message = re.sub(rf"{field}=(.*?)\{delimiter}",
                             f'{field}={redaction_text}{delimiter}', \
                               log_message)
    return log_message


class RedactingFormatter(logging.Formatter):
    """ Formatter class that redacts sensitive data """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    DELIMITER = ";"

    def __init__(self, fields_to_redact: List[str]):
        """ Initialize the formatter with the fields to be redacted """
        self.fields_to_redact = fields_to_redact
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """ Apply redaction to the formatted log record """
        return filter_datum(self.fields_to_redact, self.REDACTION,
                            super().format(record), self.DELIMITER)


def get_logger() -> logging.Logger:
    """ Set up and configure a logger """
    user_logger = logging.getLogger("user_data")
    user_logger.setLevel(logging.INFO)
    user_logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    user_logger.addHandler(stream_handler)
    return user_logger


def get_db_connection() -> mysql.connector.connection.MySQLConnection:
    """ Establish and return a database connection """
    db_password = os.environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    db_username = os.environ.get('PERSONAL_DATA_DB_USERNAME', "root")
    db_host = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.environ.get('PERSONAL_DATA_DB_NAME')
    connection = mysql.connector.connect(
        host=db_host,
        database=db_name,
        user=db_username,
        password=db_password)
    return connection


def main() -> None:
    """ Execute the main logic of connecting to the
        database and retrieving data """
    db_connection = get_db_connection()
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM users;")
    for user_record in cursor:
        log_message = f"name={user_record[0]}; email={user_record[1]}; \
                        phone={user_record[2]}; " +\
            f"ssn={user_record[3]}; password={user_record[4]}; \
               ip={user_record[5]}; " +\
            f"last_login={user_record[6]}; user_agent={user_record[7]};"
        print(log_message)
    cursor.close()
    db_connection.close()


if __name__ == '__main__':
    main()
