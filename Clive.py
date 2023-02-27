from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import pandas as pd


app = Flask(__name__)
CORS(app)
# api = CORS(app, resources={r"/api/": {"origins": "*"}})


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/api/users')
def get():
    database = pd.read_csv('FTP.csv')
    return database.to_json(orient='records')


@app.route('/api/pos/indicator')
def getIndicator():
    indicator = request.args.get('RETURN_INDICATOR')
    starttime = request.args.get('TRANS_TIME_START')
    stoptime = request.args.get('TRANS_TIME_STOP')
    print(indicator, starttime, stoptime)
    database = pd.read_csv('FTP.csv')
    return database.to_json(orient='records')


@app.route('/api/pos/drflag')
def getdrflag():
    smonth = request.args.get('SMONTH')
    sday = request.args.get('SDAY')
    syear = request.args.get('SYEAR')
    emonth = request.args.get('EMONTH')
    eday = request.args.get('EDAY')
    eyear = request.args.get('EYEAR')
    dr_flag1 = request.args.get('DIR_FLAG1')
    dr_flag2 = request.args.get('DIR_FLAG2')
    starttime = request.args.get('TRANS_TIME_START')
    stoptime = request.args.get('TRANS_TIME_STOP')
    print(smonth, sday, syear, emonth, eday, eyear,
          dr_flag1, dr_flag2, starttime, stoptime)
    database = pd.read_csv('FTP.csv')
    return database.to_json(orient='records')


@app.route('/api/locations')
def post():
    pass


if __name__ == '__main__':
    app.run()  # run our Flask app
