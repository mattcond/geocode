import requests
from common import get_null_obj
import time

def compose_request(par, conf=None):
    
    nominatin_get = """https://nominatim.openstreetmap.org/search?q={stato}+{provincia}+{regione}+{citta}+{indirizzo}&format=json&addressdetails=1"""
    
    nominatin_get = nominatin_get.format_map(par)

    return nominatin_get

def get_provincia(addr):
    try:
        return addr["county"]
    except:
        ret_value = ''
        search_list = ['local_administrative_area', 'county_code']
        cnt = 0
        while ret_value == '' and cnt<len(search_list):
            try:
                tmp_value = search_list[cnt]
                ret_value = addr[tmp_value]
            except:
                ret_value = ''
            cnt += 1
        return ret_value

def get_regione(addr):
    try:
        return addr["state"]
    except:
        ret_value = ''
        search_list = ['province', 'state_code']
        cnt = 0
        while ret_value == '' and cnt<len(search_list):
            try:
                tmp_value = search_list[cnt]
                ret_value = addr[tmp_value]
            except:
                ret_value = ''
            cnt += 1
        return ret_value

def get_citta(addr):
    try:
        return addr['city']
    except:
        ret_value = ''
        search_list = ['town', 'municipality']
        cnt = 0
        while ret_value == '' and cnt<len(search_list):
            try:
                tmp_value = search_list[cnt]
                ret_value = addr[tmp_value]
            except:
                ret_value = ''
            cnt += 1
        return ret_value

def get_indirizzo(addr):
    try:
        return addr['road']
    except:
        ret_value = ''
        search_list = ['footway', 'street','street_name','residential','path','pedestrian','road_reference','road_reference_intl','square','place']
        cnt = 0
        while ret_value == '' and cnt<len(search_list):
            try:
                tmp_value = search_list[cnt]
                ret_value = addr[tmp_value]
            except:
                ret_value = ''
            cnt += 1
        return ret_value

def get_numero_civico(addr):
    try:
        return addr['house_number']
    except:
        try:
            return addr['street_number']
        except:
            return ''

def get_stato(addr):
    try:
        return addr['country']
    except:
        try:
            return addr['country_name']
        except:
            return ''        

def get_cap(addr):
    try:
        return addr["postcode"]
    except:
        return ''

def simplify_obj(obj):
    try:
        address = obj["address"]
        ret_obj = {'stato':get_stato(address),
        'regione':get_regione(address),
        'provincia':get_provincia(address),
        'comune':get_citta(address),
        'cap':get_cap(address),
        'indirizzo':get_indirizzo(address),
        'civico':get_numero_civico(address),
        'lat':obj["lat"],
        'lon':obj["lon"],
        'importance':obj["importance"]
        }
    except:
        ret_obj = get_null_obj()

    return ret_obj

def simplify_response(resp):

    simplify_resp = list(map(simplify_obj, resp))

    return simplify_resp

def geocode(par):

    get_string = compose_request(par)

    response = requests.get(get_string)
    content = response.json()

    time.sleep(1)

    if content == []:
        
        return get_string, []
    
    else:

        return get_string, simplify_response(content)




