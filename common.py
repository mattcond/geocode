import json
#import mysql.connector
import mysql.connector as mariadb
from mysql.connector import Error
import pandas as pd

with open('conf.json', 'r') as rf:
    conf = json.loads(rf.read())

def get_null_obj():

    obj = {
        'stato':None,
        'regione':None,
        'provincia':None,
        'comune':None,
        'cap':None,
        'indirizzo':None,
        'civico':None,
        'lat':None,
        'lon':None,
        'importance':None
        }
    
    return obj

def seq(start, end, by=1):
    cnt = start
    seq_list = []
    while cnt < end:
        seq_list.append(cnt)
        cnt += 1
    return seq_list

'''
definire get_geocode_df()
'''

def get_geocode_df():

    geo_conn = mariadb.connect(host='localhost',
                                  database='geo_data',
                                  user='admin',
                                  password='passpass@123')
  
    df = pd.read_sql('SELECT * FROM codici_istat', geo_conn)

    geo_conn.close()

    return df