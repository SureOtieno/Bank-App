import pandas as pd
from sqlalchemy import text
import oracledb
import os
from dotenv import load_dotenv

from .authentication import (validate_account_type,
                             hash_user_password,
                              check_duplicate_account,
                              authenticate_user)
from .my_sql_engine import my_engine



try:
    engine = my_engine()
except oracledb.DatabaseError as e:
    print(f'Could not make a connection to the database. {e}')



def get_accounts():
    with engine.connect() as conn:
        query = 'SELECT * FROM Accounts'
        accounts_df = conn.execute(text(query))
        return accounts_df

def get_users():
    with engine.connect() as conn:
        query = 'SELECT * FROM Users'
        users_df = conn.execute(text(query))
        return users_df

class AccountCreation:
    def __init__(self):
        self.accounts_df = get_accounts()
    def create_new_account(self):
        owner = input("Enter your name: ").capitalize().strip()
        acc_type = input("Select account type (Checking/Savings): ").capitalize().strip()
        initial_balance = float(input("Enter an initial balance: "))
        password = input('Set a password for your account: ')
        validate_account_type(acc_type)   
        hashed_password = hash_user_password(password)
        """Create a new BankAccount instance."""
        # PL/SQL block

        plsql_block = text("""
        BEGIN
            INSERT INTO accounts (account_id, owner_name, account_type, balance, password)
            VALUES (accounts_seq.NEXTVAL, :owner, :acc_type, :initial_balance, :hashed_password);
            COMMIT;
        END;
        """)
        params = {
            'owner': owner,
            'acc_type': acc_type,
            'initial_balance': initial_balance,
            'hashed_password': hashed_password
        }

        try:
            with engine.connect() as conn:
                conn.execute(plsql_block, params)
                print("Account created successfully.")
        except oracledb.Error as error:
            print("Error:", error)
        finally:
            conn.close()


    def create_account(self):
        owner = input("Enter your name: ").capitalize().strip()
        acc_type = input("Select account type (Checking/Savings): ").capitalize().strip()
        initial_balance = float(input("Enter an initial balance: "))
        password = input('Set a password for your account: ')
        validate_account_type(acc_type)   
        hashed_password = hash_user_password(password)
        """
        Create a new bank account for a user, separating concerns into smaller tasks.
        """
        plsql_block = text("""
                DECLARE
                    v_exists NUMBER;
                BEGIN
                    SELECT COUNT(*)
                    INTO v_exists
                    FROM accounts
                    WHERE account_type = :acc_type;
                    IF v_exists = 0 THEN
                        INSERT INTO accounts (account_id, owner_name, account_type, balance, password)
                        VALUES (accounts_seq.NEXTVAL, :owner, :acc_type, :initial_balance, :password);
                    ELSE
                        DBMS_OUTPUT.PUT_LINE('Account type already exists. No new account created.');
                    END IF;

                    COMMIT;
                    END;

                """)
        params = {
            'owner': owner,
            'acc_type': acc_type,
            'initial_balance': initial_balance,
            'password': password
        }
        try:
            with engine.connect() as conn:
                for account in self.accounts_df:
                    if owner in account and acc_type not in account:
                        authenticate_user(password, hashed_password)
                        conn.execute(plsql_block, params)
                        print("Account created successfully.")
                    else:
                        print(f'{owner} already holds {acc_type} account.')
        
        except oracledb.Error as error:
            print("Error:", error)
        finally:
            conn.close()
   
def list_accounts(owner, accounts):
    accounts_df = get_accounts()
    if owner not in accounts_df:
        print('No account found for this user')
        return 
    else:
        print(f'Accounts for {owner}: ')
        for account in accounts:
            if owner in account:
                print(f'- Account type -- {account[2]} Account: Balance: {account.get_balance()}')

