import mysql.connector as connector
import os

# define a class for SQL user config(names)
class USER_CONFIG:
    CHECK_EMAIL_PROCDURE ="CheckEmailExists"
    CHECK_ACCOUNT_DATA = "check_account_data"
    ADD_ACOUNT ="add_account"
    ADD_USER ="add_user"
    
DB_HOST = os.getenv("DB_HOST")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_USER = os.getenv("DB_USER")
DB_DATABASE = os.getenv("DB_DATABASE")    
    
def create_connection(*args):
    conn = connector.connect(
        host=args[0],
        user=args[1],
        password=args[2],
        database=args[3]
    )
    return conn

def check_if_user_exists(email : str) -> bool:
    conn  = create_connection(DB_HOST,DB_USER,DB_PASSWORD,DB_DATABASE)
    cursor = conn.cursor()
    # the procdure returns 1 if the user exists,else returns 0
    res = cursor.callproc(USER_CONFIG.CHECK_EMAIL_PROCDURE, [email])
    return True if res==1 else False

async def insert_account_data(email : str, password : str) :
    conn = await create_connection(DB_HOST,DB_USER,DB_PASSWORD,DB_DATABASE)
    cursor = conn.cursor()
    cursor.callproc(USER_CONFIG.ADD_ACOUNT, [email,password])
    conn.commit()
    cursor.close()
    
async def insert_user_data(email : str, first_name : str, last_name : str, phone_number : str) :
    conn = await create_connection(DB_HOST,DB_USER,DB_PASSWORD,DB_DATABASE)
    cursor = conn.cursor()
    cursor.callproc(USER_CONFIG.ADD_USER, [email,first_name,last_name,phone_number])
    conn.commit()
    conn.close()

def check_if_account_exists(email : str, password : str) -> bool:
    conn  = create_connection(DB_HOST,DB_USER,DB_PASSWORD,DB_DATABASE)
    cursor = conn.cursor()
    # the procdure returns 1 if the account exists,else returns 0
    res = cursor.callproc(USER_CONFIG.CHECK_ACCOUNT_DATA, [email,password])
    return True if res==1 else False