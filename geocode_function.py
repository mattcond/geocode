import requests
import re
import json
import here_wrapper as here
import osm_wrapper as osm
import mysql.connector as mariadb
import geopandas as gpd

from shapely.geometry import Point
from common import get_null_obj, conf, get_geocode_df

fp = 'shapefile/Com01012020_g/Com01012020_g_WGS84.shp'
shp = gpd.read_file(fp)
shp = shp.to_crs("EPSG:4326")

codici_istati_df = get_geocode_df()

def get_latlon(par, limit_result=None):
    '''
    1. provo a arricchire attraverso here. Se content vuoto allora OSM
    '''

    get_string , content = here.geocode(par)
    geocode_service = "HERE"
    if content == []:

        get_string, content = osm.geocode(par)
        geocode_service = "OSM"

    if content == []:
        get_string = {'here': here.compose_request(conf, par), 'osm': osm.compose_request(par)}
        geocode_service = ""
        content = [get_null_obj()]
        limit_result = 1

    return {'req':get_string, 
            'resp':content[:limit_result],
            'geocode_service':geocode_service
            }


def reverse_geocode(lat, lng):
    
    pt = Point(lng, lat)

    record = None
    
    for ix, row in shp.iterrows():
        if row["geometry"].contains(pt):
            pro_com = row["PRO_COM"]
            
            record = codici_istati_df.query('codice_istat_comune == {}'.format(pro_com))
            
            record = record.iloc[0,:]

            
    if record is not None:
        response = {
            'request':{
                'latitudine':lat,
                'longitudine':lng
            }, 
            'response':{
                'id_regione':int(record[0]), 
                'regione':record[1], 
                'id_provincia':int(record[2]), 
                'provincia':record[3], 
                'sigla':record[4], 
                'id_comune':str(record[5]), 
                'comune':record[6], 
                'centroide':{
                    'latitudine': record[8], 
                    'longitudine': record[7]
                }
            }
        }
    else:
        response = [] 

    return response