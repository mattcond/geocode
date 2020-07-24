from flask import Flask, request, jsonify
from geocode_function import get_latlon, reverse_geocode
import requests
import time

app = Flask(__name__)

@app.route("/")
def home():
    return "I'm super alive *-*"

@app.route("/geocode")
def geocode():
    if len(request.args)==0:
        return jsonify('No parameter supply')
    try:
        citta = '+'.join(request.args.get('citta').split(" "))
    except:
        citta = ''
    
    try:
        stato = '+'.join(request.args.get('stato').split(" "))
    except:
        stato = ''
    
    try:
        provincia = '+'.join(request.args.get('provincia').split(" "))
    except:
        provincia = ''

    try:
        regione = '+'.join(request.args.get('regione').split(" "))
    except:
        regione = ''

    try:
        indirizzo = '+'.join(request.args.get('indirizzo').split(" "))
    except:
        indirizzo = ''

    limit_result = request.args.get('limit')
    if limit_result is not None:
        limit_result = int(limit_result)
        
    parameters = {
        'citta': citta,
        'stato': stato,
        'provincia': provincia,
        'regione': regione,
        'indirizzo': indirizzo
    }

    return jsonify(get_latlon(parameters, limit_result))

@app.route('/geocode/reverse')
def reverse():
    if len(request.args)==0:
        return jsonify('Reverse gecoding it\'s alive *-*. No parameter supply')
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    print(lat, lng)
    return jsonify(reverse_geocode(float(lat), float(lng)))

if __name__ == "__main__":
    app.config['JSON_SORT_KEYS'] = False
    app.run(host= '127.0.0.1') #debug=True
