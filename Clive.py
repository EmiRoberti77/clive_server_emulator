from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import pandas as pd
import ftplib
import psycopg2 as ps
from sqlalchemy import create_engine
from sqlalchemy import text

# Database Connection
engine = create_engine('postgresql://postgres:admin@localhost:5432/POS')

app = Flask(__name__)
CORS(app)
# api = CORS(app, resources={r"/api/": {"origins": "*"}})

def monthval(x):
    if x==1:
        y = 'Jan'
    elif x==2:
        y = 'Feb'
    elif x==3:
        y = 'Mar'
    elif x==4:
        y = 'Apr'
    elif x==5:
        y = 'May'
    elif x==6:
        y = 'Jun'
    elif x==7:
        x = 'Jul'
    elif x==8:
        x = 'Aug'
    elif x==9:
        x = 'Sep'
    elif x==10:
        x = 'Oct'
    elif x==11:
        x = 'Nov'
    elif x==12:
        x = 'Dec'
    else:
        y = 'Invalid'
    return y

def process(sday,smonth,syear,eday,emonth,eyear):
    s_month=monthval(int(smonth))
    e_month=monthval(emonth)
    stxt=s_month+str(sday)+str(syear)
    etxt=e_month+str(eday)+str(eyear)
    sdate='"FTP_ExternalSD'+stxt+'"'
    edate='"FTP_ExternalSD'+etxt+'"'
    return sdate,edate

@app.route('/')
def hello():
    return "Hello World!"


@app.route('/api/users')
def get():
    database = pd.read_csv('FTP.csv')
    return database.to_json(orient='records')


@app.route('/api/pos/indicator')
def getIndicator():
    smonth = request.args.get('SMONTH')
    sday = request.args.get('SDAY')
    syear = request.args.get('SYEAR')
    emonth = request.args.get('EMONTH')
    eday = request.args.get('EDAY')
    eyear = request.args.get('EYEAR')
    indicator = request.args.get('RETURN_INDICATOR')
    starttime = request.args.get('TRANS_TIME_START')
    stoptime = request.args.get('TRANS_TIME_STOP')
    
    sdate,edate = process(sday,smonth,syear,eday,emonth,eyear)
    print(
        smonth,
        sday,
        syear,
        emonth,
        eday,
        eyear,
        starttime,
        stoptime,
        indicator)
    with engine.begin() as conne:
        query = text('SELECT * FROM public.'+sdate+' WHERE ("TRANS_TIME">'+str(stoptime)+' OR "TRANS_TIME"<'+str(starttime)+') AND "RETURN_INDICATOR" = '+str(indicator)+' LIMIT 1000')
        database=pd.read_sql_query(query,conne)
    #database = pd.read_csv('FTP.csv')
    
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
    sdate,edate = process(sday,smonth,syear,eday,emonth,eyear)
    with engine.begin() as conne:
        query = text('SELECT * FROM public.'+sdate+' WHERE ("TRANS_TIME">'+str(stoptime)+' OR "TRANS_TIME"<'+str(starttime)+') AND "RETURN_INDICATOR" = '+str(indicator)+' LIMIT 1000')
        database=pd.read_sql_query(query,conne)
    database = pd.read_csv('FTP.csv')
    return database.to_json(orient='records')


@app.route('/api/locations')
def post():
    pass


if __name__ == '__main__':
    app.run()  # run our Flask app
