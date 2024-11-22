#!/usr/bin/env python3
"""
simplr module to encrypt the password
"""
import bcrypt


def _hash_password(password):
    """
    using the bycrypt module to hash the password
    """
    encoded = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(encoded, salt)
