#!/usr/bin/env python3
""" Module for protecting sensitive information (PII) in log records """

from typing import List
import logging
import re
from mysql.connector import connection
from os import environ

PII_FIELDS = ('name', 'email', 'password', 'ssn', 'phone')


def filter_datum(fields: List[str], mask: str,
                 log_message: str, delimiter: str) -> str:
    """ Replaces specified fields in log_message with a redaction mask """
    obscured_message = log_message
    for field in fields:
        obscured_message = re.sub(f"{field}=.*?{delimiter}",
                                  f"{field}={mask}{delimiter}", obscured_message)
    return obscured_message


def get_logger() -> logging.Logger:
    """ Configures and returns a logger for user data """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger


def get_db() -> connection.MySQLConnection:
    """
    Establishes a database connection using environment variables
    """
    user = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    database = environ.get("PERSONAL_DATA_DB_NAME")
    
    conn = connection.MySQLConnection(
        user=user,
        password=password,
        host=host,
        database=database
    )
    return conn


class RedactingFormatter(logging.Formatter):
    """ Custom logging formatter to redact specified fields """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"


    def __init__(self, fields: List[str]):
        """ Initializes the formatter with fields to redact """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields


    def format(self, record: logging.LogRecord) -> str:
        """ Applies redaction to sensitive fields in log records """
        return filter_datum(
            self.fields, self.REDACTION, super(
                RedactingFormatter, self).format(record),
            self.SEPARATOR)


def main() -> None:
    """
    Connects to the database, retrieves user data,
    and logs each record with sensitive data redacted
    """
    db = get_db()
    cursor = db.cursor()

    query = 'SELECT * FROM users;'
    cursor.execute(query)
    results = cursor.fetchall()

    logger = get_logger()

    for row in results:
        log_message = 'name={}; email={}; phone={}; ssn={}; password={}; ip={}; '\
                      'last_login={}; user_agent={};'
        log_message = log_message.format(row[0], row[1], row[2], row[3],
                                         row[4], row[5], row[6], row[7])
        logger.info(log_message)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
