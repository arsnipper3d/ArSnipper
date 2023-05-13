from flask import Blueprint, request, jsonify

from api.models.user import check_if_user_exists,insert_account_data, insert_user_data, check_if_account_exists


users = Blueprint('users', __name__, url_prefix='/users')

db_conn = None





users.route('/add', methods=['POST'])
def add_user():
      
   data = request.get_json()
   email = data.get('email')
   password = data.get('password')
   first_name = data.get('first_name')
   last_name = data.get('last_name')
   phone = data.get('phone')
   
   if check_if_user_exists(email):
      return jsonify({"status":400,"message":"User already exists"}) 
   # insert into users table
   insert_user_data(email, first_name, last_name, phone)
   
   # create account record for user with hash password
   insert_account_data(email, password)

   return jsonify({"status":200,"message":"User added"})

users.route('/login', methods=['POST'])
def login():
   data = request.get_json()
   email = data.get('email')
   password = data.get('password')
   
   if check_if_account_exists(email,password):
      return jsonify({"status":200,"message":"Login successful"})
   
   return jsonify({"status":400,"message":"Invalid credentials"})


