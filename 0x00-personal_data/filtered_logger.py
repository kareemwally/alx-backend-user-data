#!/usr/bin/env python3
"""
simple module for logging system
"""
import re


def filter_datum(fields, redaction, message, separator):
    """
    filtering the message for logging file
    """
    return re.sub(
        f"({'|'.join(fields)})=[^;]*",
        lambda m: f"{m.group(1)}={redaction}",
        message
    )
