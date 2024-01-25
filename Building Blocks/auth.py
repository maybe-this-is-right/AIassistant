import hashlib
import logging
import getpass
import os
import json
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from database_manager import DatabaseManager  # Import DatabaseManager for user data handling

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password_hash = Column(String)
    # Add a column for two-factor authentication, if necessary
    # two_factor_secret = Column(String)

class Authenticator:
    def __init__(self, db_path):
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    @staticmethod
    def _hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    def _get_password_hash(self, username):
        session = self.Session()
        user = session.query(User).filter(User.username == username).first()
        session.close()
        return user.password_hash if user else None

    def authenticate(self, username):
        try:
            password_hash = self._get_password_hash(username)
            if not password_hash:
                raise ValueError(f"No user found with username: {username}")

            entered_password = getpass.getpass("Enter password to access the assistant: ")
            entered_hash = self._hash_password(entered_password)
            if entered_hash == password_hash:
                # Here you can add a call to a two-factor authentication method
                # if self.verify_two_factor_token(username):
                logging.info("Authentication successful.")
                return True
                # else:
                #     logging.warning("Two-factor authentication failed.")
                #     return False
            else:
                logging.warning("Authentication failed.")
                return False
        except Exception as e:
            logging.error(f"Error during authentication: {e}")
            return False

    def setup_password(self, username, new_password):
        hashed_password = self._hash_password(new_password)
        session = self.Session()
        user = User(username=username, password_hash=hashed_password)
        session.add(user)
        session.commit()
        session.close()

    # Placeholder for two-factor authentication methods
    # def setup_two_factor_authentication(self, username):
    #     # Implementation for setting up two-factor authentication
    #     pass

    # def verify_two_factor_token(self, username, token):
    #     # Implementation for verifying the two-factor token
    #     pass

logging.basicConfig(filename='C:/Users/rudym/Desktop/PersonalAI/Logs/auth.log', 
                    level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Example usage
# authenticator = Authenticator("C:/Users/rudym/Desktop/PersonalAI/Database/mydb.db")
# authenticator.setup_password("username", "your_secure_password")
# is_authenticated = authenticator.authenticate("username")
# print(is_authenticated)
