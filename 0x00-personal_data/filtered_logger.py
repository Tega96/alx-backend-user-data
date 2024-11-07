#!/usr/bin/env python3
"""
Script for handling Personal Data
"""

from typing import List
import re
from os import environ
import mysql.connector
import logging


# # PII fields to be redacted
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
        message: str, separator: str) -> str:
    """
    Replaces sensitive information in a a message with a redacted value
    based on the list of fields to redact

    Args:
    fields: list of fields to redact
    redaction: the value to use for redaction
    message: the string message to filter
    separator: the separator to use between fields

    Returns:
    The filtered string message with redacted values
    """
    for f in fields:
        message = re.sub(f'{f}=.*?{separator}',
                f'{f}={redaction}{separator}', message)
        return message
