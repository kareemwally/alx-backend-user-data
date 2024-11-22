#!/usr/bin/env python3
"""
simplr module to encrypt the password
"""
import bcrypt


def _hash_password(password):
    """
    using the bycrypt module to hash the password
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)
