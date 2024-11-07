#!/usr/bin/env python3
"""
simple module for formatting the users' data.
"""
import os
import logging
import mysql.connector
import re
from mysql.connector import connection
from typing import List, Tuple

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: \
              %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        intiating a class instance.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        formatting a login record.
        """
        message = super().format(record)
        return filter_datum(self.fields, self.REDACTION, message,
                            self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Replaces sensitive fields in the log message with
    redaction text.
    """
    pattern = f"({'|'.join(fields)})=.*?{separator}"
    return re.sub(pattern, lambda match:
                  f"{match.group(1)}={redaction}{separator}", message)


def get_logger() -> logging.Logger:
    """
    Returns a logger object configured to use RedactingFormatter.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger


def get_db() -> connection.MySQLConnection:
    """
    Returns a MySQL database connection using
    environment variables for credentials.
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME")

    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )


def main() -> None:
    """
    Fetches user data from the database and logs
    it in an obfuscated format.
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT name, email, phone, ssn, password, ip, \
                    last_login, user_agent FROM users;")

    logger = get_logger()
    for row in cursor:
        message = (
            f"name={row[0]}; email={row[1]}; phone={row[2]}; \
                    ssn={row[3]}; "
            f"password={row[4]}; ip={row[5]}; last_login={row[6]}; \
                    user_agent={row[7]};"
        )
        logger.info(message)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
