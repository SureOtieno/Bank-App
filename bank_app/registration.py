from sqlalchemy import text
from .my_sql_engine import my_engine
from .authentication import hash_user_password, authenticate_user


class Register:

    def create_new_user():
        username = input("Enter username: ").strip()
        firstname = input('Enter firstname: ').strip().capitalize()
        lastname = input('Enter lastname: ').strip().capitalize()
        email = input('Enter email: ').strip()
        password = input('Enter password: ').strip()
        hashed_password = hash_user_password(password)
        user_plsql = """
                    BEGIN
                        INSERT INTO users (user_id, username, first_name, last_name, email, password)
                        VALUES (users_seq.NEXTVAL, :username, :firstname, :lastname, :email, :hashed_password);
                    END;
                    """
        params = {
            'username':username,
            'firstname':firstname,
            'lastname':lastname,
            'email':email,
            'hashed_password':hashed_password, 
        }
        engine = my_engine()
        with engine.connect() as conn:
            conn.execute(text(user_plsql), params)
            conn.commit()

    
    def login():
        email = input('Enter email: ').strip()
        password = input('Enter password: ').strip()
        hashed_password = hash_user_password(password)
        engine = my_engine()
        with engine.connect() as conn:
            users = conn.execute(text('SELECT * FROM users'))
            for row in users:
                if email in row:
                    authenticate_user(password, hashed_password)
                else:
                    print('Email does not exists.')
                       
                