import requests
import re
import json
from common import conf, get_null_obj

def compose_request(conf, par):

    #here_geocode = "https://geocoder.api.here.com/6.2/geocode.json?locationattributes=addressDetails&app_id={a_id}&app_code={a_code}&searchtext={indirizzo}"
    #here_geocode = here_geocode.format(a_id = conf["geocode"]["here"]["app_id"], a_code = conf["geocode"]["here"]["app_code"], indirizzo = "{indirizzo}")

    '''
    MODIFICATO CON PUNTAMENTO A NUOVO SERVIZIO REST HERE: LIMITE SI 250K CHIAMATE AL MESE
    '''

    here_geocode = "https://geocoder.ls.hereapi.com/6.2/geocode.json?locationattributes=addressDetails&apiKey={api_key}&searchtext={indirizzo}"
    here_geocode = here_geocode.format(api_key = conf["geocode"]["here"]["api_key"], indirizzo = "{indirizzo}")

    here_address = '+'.join([par['stato'].replace(' ', '+'), 
                         par['regione'].replace(' ', '+'), 
                         par['provincia'].replace(' ', '+'),
                         par['citta'].replace(' ', '+'),
                         par['indirizzo'].replace(' ', '+')])
    
    here_geocode_mod = here_geocode.format(indirizzo = here_address)
    
    #print(here_geocode_mod)

    return here_geocode_mod
    
def get_importance(addr):
    try:
        return addr["Relevance"]
    except:
        return 0.0

def get_latitude(addr):
    try:
        return addr["Location"]["DisplayPosition"]["Latitude"]
    except:
        return 0.0

def get_longitude(addr):
    try:
        return addr["Location"]["DisplayPosition"]["Longitude"]
    except:
        return 0.0

def get_country(addr):
    try:
        return addr["Location"]["AddressDetails"]["Country"]["value"]
    except:
        return ""

def get_state(addr):
    try:
        return addr["Location"]["AddressDetails"]["State"]["value"]
    except:
        return ""

def get_county(addr):
    try:
        return addr["Location"]["AddressDetails"]["County"]["value"]
    except:
        return ""

def get_city(addr):
    try:
        return addr["Location"]["AddressDetails"]["City"]["value"]
    except:
        return ""
    
def get_postal_code(addr):
    try:
        return addr["Location"]["AddressDetails"]["PostalCode"]
    except:
        return ""

def get_street(addr):
    try:
        return addr["Location"]["AddressDetails"]["Street"]["value"]
    except:
        return ""

def get_housenumber(addr):
    try:
        return addr["Location"]["AddressDetails"]["HouseNumber"]["value"]
    except:
        return ""
    
def simplify_obj(addr):
    try:
        ret_obj = {
            'stato':get_country(addr),
            'regione':get_state(addr),
            'provincia':get_county(addr),
            'comune':get_city(addr),
            'cap':get_postal_code(addr),
            'indirizzo':get_street(addr),
            'civico':get_housenumber(addr),
            'lat':get_latitude(addr),
            'lon':get_longitude(addr),
            'importance': get_importance(addr)
            }
    except Exception as e:
        print(e)
        ret_obj = get_null_obj()
    return ret_obj

def simplify_response(resp):
    
    addresses = [i for i in resp["Response"]["View"][0]["Result"]]
    
    simplify_addresses = list(map(simplify_obj, addresses))
    
    return simplify_addresses

def geocode(par):

    get_string = compose_request(conf, par)

    response = requests.get(get_string)
    content = response.json()

    if content["Response"]["View"] == []:
        
        return get_string, []
    
    else:

        return get_string, simplify_response(content)