#Aaron Pahwa

"""
Bus Tracker that uses MTA BusTime API to
track the B11 at the 306582 stop at
49th Street and 6th Ave Brooklyn
"""

"""
Future Versions:
--> Next Bus
--> Specify what line and stop you want
    --> Use maps api and location data to find closest stop to your line
"""

import requests
import json
import datetime
import time
import iso8601
import math
import calendar
import pytz
from flask import Flask, make_response, request, jsonify, render_template

app = Flask(__name__)


def get_request1():
    req = request.get_json(force=True)
    action = req.get('queryResult').get('action')

    if action == "get_distance":
        #API GET:
        
        payload = {'key':'3a03f90d-7ca3-4b74-b22f-8b6535e6d788','OperatorRef':'MTA','MonitoringRef':'306582','Li':'NYCT_B11','StopMonitoringDetailLevel':'basic','MaximumStopVisits':'1','MinimumStopVisitsPerLine':'1'}
        obj = requests.get('http://bustime.mta.info/api/siri/stop-monitoring.json', params=payload)
        res = obj.json()

        
        distance = res['Siri']['ServiceDelivery']['StopMonitoringDelivery'][0]['MonitoredStopVisit'][0]['MonitoredVehicleJourney']['MonitoredCall']['Extensions']['Distances']['PresentableDistance']
        stops = res['Siri']['ServiceDelivery']['StopMonitoringDelivery'][0]['MonitoredStopVisit'][0]['MonitoredVehicleJourney']['MonitoredCall']['Extensions']['Distances']['StopsFromCall']
        busTime = res['Siri']['ServiceDelivery']['StopMonitoringDelivery'][0]['MonitoredStopVisit'][0]['MonitoredVehicleJourney']['MonitoredCall']["ExpectedArrivalTime"]

        #Time parsing:

        iso_time = iso8601.parse_date(busTime)
        curr_time = (datetime.datetime.now())
        local = pytz.timezone('America/New_York')
        local_dt = local.localize(curr_time)
        utc_dt = curr_time.astimezone(pytz.utc)
        utc_dt2 = iso_time.astimezone(pytz.utc)
        arrival_time = calendar.timegm(utc_dt2.timetuple())
        current_time = calendar.timegm(utc_dt.timetuple())
        eta = math.floor(math.floor((arrival_time - current_time) / 60 * 100) / 100)

        #Cleans up fulfillment text
        
        is_stop = distance.find('stops')
        if stops <= 0:
            result = {'fulfillmentText': "The bus is " + str(distance)}
            
        elif is_stop != -1:
            result = {'fulfillmentText': "The bus is " + str(eta) + " minutes away or " + str(stops) + " stops away"}            

        else:
            result = {'fulfillmentText': "The bus is " + str(eta) + " minutes away or " + str(stops) + " stops away"}

        return jsonify(result)


@app.route('/webhook', methods=['GET','POST'])
def index():
    return get_request1()


@app.route("/")
def hello():
    payload = {'key':'3a03f90d-7ca3-4b74-b22f-8b6535e6d788','OperatorRef':'MTA','MonitoringRef':'306582','Li':'NYCT_B11','StopMonitoringDetailLevel':'basic','MaximumStopVisits':'1','MinimumStopVisitsPerLine':'1'}
    obj = requests.get('http://bustime.mta.info/api/siri/stop-monitoring.json', params=payload)
    res = obj.json()
    busTime = res['Siri']['ServiceDelivery']['StopMonitoringDelivery'][0]['MonitoredStopVisit'][0]['MonitoredVehicleJourney']['MonitoredCall']["ExpectedArrivalTime"]
    distance = res['Siri']['ServiceDelivery']['StopMonitoringDelivery'][0]['MonitoredStopVisit'][0]['MonitoredVehicleJourney']['MonitoredCall']['Extensions']['Distances']['PresentableDistance']
    iso_time = iso8601.parse_date(busTime)
    curr_time = (datetime.datetime.now())
    local = pytz.timezone('America/New_York')
    local_dt = local.localize(curr_time)
    utc_dt = curr_time.astimezone(pytz.utc)
    utc_dt2 = iso_time.astimezone(pytz.utc)
    arrival_time = calendar.timegm(utc_dt2.timetuple())
    current_time = calendar.timegm(utc_dt.timetuple())
    eta = math.floor(math.floor((arrival_time - current_time) / 60 * 100) / 100)
    return render_template('index.html', eta = eta, current_time = current_time, arrival_time = arrival_time, distance = distance)

if __name__ == "__main__":
    app.run("0.0.0.0", debug=True, port=8080)

