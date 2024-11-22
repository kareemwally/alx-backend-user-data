#!/usr/bin/env python3
"""
simplr module to encrypt the password
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user
        Args:
            email (str): The email of the user
            password (str): The password of the user
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user


def _hash_password(password):
    """
    using the bycrypt module to hash the password
    """
    encoded = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(encoded, salt)
