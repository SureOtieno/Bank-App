from main import main
from bank_app.registration import Register
from bank_app.authentication import hash_user_password, authenticate_user
from bank_app.my_sql_engine import my_engine


engine = my_engine()


def interface():
    print('Welcome to customer CLI. To continue please select an option 1 / 2.')
    print('\nOptions')
    print('1: Register')
    print('2: Login')


    choice = int(input('Please select an option: '))
    if choice == 1: # Register
        Register.create_new_user()
        print('Registration successful.')
        Register.login()
        main()
        

    else: # user_login
        Register.login()
        main()

interface()