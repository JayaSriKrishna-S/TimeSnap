import subprocess
import re
import time
import requests
from urllib.parse import urlparse


import mindsdb_sdk
import pandas as pd
import mindsdb
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
MINDSDB_USERNAME = os.getenv('MINDSDB_USERNAME')
MINDSDB_PASSWORD = os.getenv('MINDSDB_PASSWORD')
server = mindsdb_sdk.connect('https://cloud.mindsdb.com', login=MINDSDB_USERNAME, password=MINDSDB_PASSWORD)
# server=mindsdb_sdk.connect('http://localhost:47334')
databases = server.list_databases()
database = databases[0]
# print(server.list_databases())





def establish():
    working_folder = os.getcwd()
    loc_ngrok = os.path.join(working_folder,"ngrok.exe")

    ngrok_cmd = loc_ngrok  # Replace with the actual path to your NGROK executable
    
    # Run NGROK with the command "ngrok tcp 3306"
    ngrok_process = subprocess.Popen([ngrok_cmd, 'tcp', '3306'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    
    # Read stdout line by line until the NGROK process completes
    
    # NGROK API endpoint to get the tunnel information
    api_url = "http://127.0.0.1:4040/api/tunnels"
    
    print("Establishing NGROK tunnel...")
    
    while True:
        # Pause execution for a few seconds
        time.sleep(3)
        
        # Send an HTTP GET request to the NGROK API
        try:
         response = requests.get(api_url)
        except Exception as e:  
          time.sleep(3)
          continue
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Extract the public URL from the response JSON
            data = response.json()
            public_url = data["tunnels"][0]["public_url"]
            print("NGROK tunnel established.")
            parsed_url = urlparse(public_url)
            forwarding_port = parsed_url.port
            update_local_connection(forwarding_port)
            return 1
        print("Trying to establish the NGROK tunnel...")
   

def update_local_connection(port):
 try:
  query = database.query('DROP DATABASE mysql_datasource')
  query.fetch()
 except Exception as e:
    pass 
 

 user=os.getenv('MYSQL_USER')
 password=os.getenv('MYSQL_PASSWORD')
 database_name=os.getenv('MYSQL_DATABASE')
 q = f'''
 CREATE DATABASE mysql_datasource
 WITH ENGINE = "mysql",
 PARAMETERS = {{
     "user": "{user}",
     "password": "{password}",
     "host": "0.tcp.in.ngrok.io",
     "port": "{port}",
     "database": "{database_name}"
 }};
 '''
 

 query = database.query(q)
 query.fetch()
 return 1




       


