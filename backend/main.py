# Waleed Yusuf

import flask
from flask import jsonify
from flask import request
from sql import create_connection
from sql import execute_read_query
from datetime import datetime
import creds

app = flask.Flask(__name__) #sets up the application
app.config["DEBUG"] = True #allow to show errors in browser

myCreds = creds.Creds()
conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbname)
cursor = conn.cursor(dictionary=True)

authorizedusers = [
  {
    #default user
    'username': 'username',
    'password': 'password',
    'role': 'Admin',
    'token': '0',
    'admininfo': None
  },
]

@app.route('/login', methods = ['GET'])
def app_login():
    username = request.headers['username'] #get header parameter
    pw = request.headers['password']
    for au in authorizedusers: 
        if au['username'] == username and au['password'] == pw: #found an auth user
          sessiontoken = au['token']
          admininfo = au['admininfo']
          returninfo = []
          returninfo.append(au['role'])
          return jsonify(returninfo)
    return 'SECURITY ERROR'

spaceship_list = []
cargo_list = []
captain_list = []

# Get all spaceships
@app.route('/spaceship', methods=['GET'])
def get_spaceship():
    sql = 'SELECT * from spaceship'
    get_spaceship = execute_read_query(conn, sql)
    spaceship_list.append(get_spaceship)
    return jsonify(spaceship_list)

# Add Spaceship
@app.route('/spaceship', methods=['POST'])
def add_spaceship():          
  request_data = request.get_json()   
  add_weight = request_data['maxweight']    
  add_captainid = request_data['captainid']
  sql_captainid = "Select * from captain where id = %s"
  val1 = (add_captainid,)
  cursor.execute(sql_captainid,val1)
  result = cursor.fetchone()
  if result is None:
     return 'Captain Does not exist'
  sql = "INSERT INTO spaceship(maxweight, captainid) VALUES (%s, %s)"   #SQL Insert command
  val = (add_weight, add_captainid)                
  cursor.execute(sql, val)
  conn.commit()
  return 'Add request successful'
      
# Update Spaceship
@app.route('/spaceship/<id>', methods=['PUT']) #Id must be in the url
def update_spaceship(id):
  request_data = request.get_json()   
  update_weight = request_data['maxweight']    
  update_captainid = request_data['captainid']

  sql_spaceshipid = "Select * from spaceship where id = %s"
  val_spaceship = (id, )
  cursor.execute(sql_spaceshipid, val_spaceship)
  result_spaceship = cursor.fetchone()
  if result_spaceship is None:
     return 'Spaceship Does not exist'

  sql_captainid = "Select * from captain where id = %s"
  val1 = (update_captainid,)
  cursor.execute(sql_captainid,val1)
  result = cursor.fetchone()
  if result is None:
     return 'Captain Does not exist' 
        
  sql = "UPDATE spaceship SET maxweight = %s, captainid = %s Where id = %s" #SQL Command to Update
  val = (update_weight, update_captainid, id)                

  cursor.execute(sql, val)
  conn.commit() #To make sure changes are made in databse
  return 'Update request successful'

# Delete spaceship
@app.route('/spaceship/<id>', methods=['DELETE']) #Id must be in the url
def delete_spaceship(id):
  sql = "DELETE FROM spaceship WHERE id = %s" #SQl command for delete
  val = (id,)
  cursor.execute(sql, val)
  conn.commit()
  return 'Delete request successful'

app.run()
    
