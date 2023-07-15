import mindsdb_sdk
import pandas as pd
import mindsdb
import os
from dotenv import load_dotenv


load_dotenv()
MINDSDB_USERNAME = os.getenv('MINDSDB_USERNAME')
MINDSDB_PASSWORD = os.getenv('MINDSDB_PASSWORD')
server = mindsdb_sdk.connect('https://cloud.mindsdb.com', login=MINDSDB_USERNAME, password=MINDSDB_PASSWORD)

databases = server.list_databases()
database = databases[0]

 


def train(x):
    
    project=server.get_project()

    try:
     project.drop_model(x[0])
    except Exception as e:
        pass 
    
    try:
        query = database.query('CREATE MODEL mindsdb.{} FROM mysql_datasource (SELECT * FROM {}) PREDICT {} ORDER BY {} GROUP BY {} WINDOW {} HORIZON {};'.format(*x[:2], x[2], x[3], ', '.join(x[4]), x[5], x[6]))
        s=query.fetch()
        return(1)
    except Exception as e:
        return(e)



def status(y):
    query2=database.query("SELECT * FROM mindsdb.models WHERE NAME ='{}'".format(y))
    s=query2.fetch()
    status= s["STATUS"].tolist()
    accuracy=s["ACCURACY"].tolist()
    return("status : "+str(status)+"\naccuracy : "+str(accuracy))



def prediction_m(px):
    q=px
    databases = server.list_databases()
    database = databases[0]
    query1=database.query(q)
    try:
        s=query1.fetch()
        return(s)
    except Exception as e:
        return(e)
    





 
