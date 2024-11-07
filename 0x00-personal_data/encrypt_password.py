#!/usr/bin/env python3
"""
simple module to encrypt data
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt with automatic salting."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed
