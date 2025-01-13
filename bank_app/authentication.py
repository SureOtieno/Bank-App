import bcrypt
from sqlalchemy import create_engine
import pandas as pd
import oracledb
import os
from dotenv import load_dotenv


load_dotenv()
oracle_conn_string = os.getenv('ORACLE_CONN_STRING')


try:
    engine = create_engine(oracle_conn_string, echo=True)
    engine = create_engine(f"{oracle_conn_string}")
    with engine.connect() as conn:
        print('Connected to Oracle DB successfully')
except oracledb.DatabaseError as e:
    print(f'Could not make a connection to the database. {e}')
  

class Security:
    @staticmethod
    def hash_password(password):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt).decode()

    @staticmethod
    def verify_password(password, hashed_password):
        return bcrypt.checkpw(password.encode(), hashed_password.encode())
    
def validate_account_type(acc_type):
    """Validate the account type input."""
    if acc_type not in ["Checking", "Savings"]:
        raise ValueError("Invalid account type. Please choose either 'Checking' or 'Savings'.")

def check_duplicate_account(accounts, owner, acc_type):
    """Check if the user already has an account of the given type."""
    if acc_type in accounts.get(owner, {}):
        raise ValueError(f"You already have a {acc_type} account.")

def hash_user_password(password):
    """Hash the password for secure storage."""
    return Security.hash_password(password)


def authenticate_user(password, hashed_password):
    """
    Authenticate a user based on their name and password.
    """
    if Security.verify_password(password, hashed_password):
        print("Authentication successful!")
        return True
    else:
        print("Incorrect password.")
        return False

