import bcrypt

class Security:
    @staticmethod
    def hash_password(password):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt).decode()

    @staticmethod
    def verify_password(password, hashed_password):
        return bcrypt.checkpw(password.encode(), hashed_password.encode())
    



def hash_user_password(password):
    """Hash the password for secure storage."""
    return Security.hash_password(password)

def authenticate_user(accounts, owner, password):
    """
    Authenticate a user based on their name and password.
    """
    if owner in accounts:

        # Iterate through the user's accounts to find a matching password
        for acc_type, account in accounts[owner].items():
            hashed_password = account.password
            if Security.verify_password(password, hashed_password):
                print("Authentication successful!")
                return True

        print("Incorrect password.")
        return False
    else:
        print("Account not found. Please create an account first.")
        return False

  
