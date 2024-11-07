#!/usr/bin/env python3
"""
simple module for logging system
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    filtering the message for logging file
    """
    return re.sub(
        f"({'|'.join(fields)})=[^;]*",
        lambda m: f"{m.group(1)}={redaction}",
        message
    )
