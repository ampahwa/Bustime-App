#Aaron Pahwa

"""
Bus Tracker that uses MTA BusTime API to
track the B11 at the 306582 stop at
49th Street and 6th Ave Brooklyn
"""

"""
Future Patches:
--> Next Bus
--> Specify what line and stop you want
    --> Use maps api and location data to find closest stop to your line
"""

# [START python_app]

import requests
import json
from flask import Flask, make_response, request, jsonify

app = Flask(__name__)


def get_request1():
    req = request.get_json(force=True)
    action = req.get('queryResult').get('action')

    if action == "get_distance":
        payload = {'key':'3a03f90d-7ca3-4b74-b22f-8b6535e6d788','OperatorRef':'MTA','MonitoringRef':'306582','Li':'NYCT_B11','StopMonitoringDetailLevel':'basic','MaximumStopVisits':'1','MinimumStopVisitsPerLine':'1'}
        obj = requests.get('http://bustime.mta.info/api/siri/stop-monitoring.json', params=payload)
        res = obj.json()
        distance = res['Siri']['ServiceDelivery']['StopMonitoringDelivery'][0]['MonitoredStopVisit'][0]['MonitoredVehicleJourney']['MonitoredCall']['Extensions']['Distances']['PresentableDistance']
        payloadStops = {'key':'3a03f90d-7ca3-4b74-b22f-8b6535e6d788','OperatorRef':'MTA','MonitoringRef':'306582','Li':'NYCT_B11','StopMonitoringDetailLevel':'basic','MaximumStopVisits':'1','MinimumStopVisitsPerLine':'1'}
        objStops = requests.get('http://bustime.mta.info/api/siri/stop-monitoring.json', params=payload)
        resStops = obj.json()
        stops = res['Siri']['ServiceDelivery']['StopMonitoringDelivery'][0]['MonitoredStopVisit'][0]['MonitoredVehicleJourney']['MonitoredCall']['Extensions']['Distances']['StopsFromCall']
        is_stop = distance.find('stops')
        if stops <= 0:
            result = {'fulfillmentText': "The bus is " + str(distance)}
        elif is_stop != -1:
            result = {'fulfillmentText': "The bus is " + str(stops) + " stops away"}
        else:
            result = {'fulfillmentText': "The bus is " + str(distance) + " or " + str(stops) + " stops away"}
        
        return jsonify(result)


@app.route('/webhook', methods=['GET','POST'])
def index():
    return get_request1()


@app.route("/")
def hello():
    return "Hello!"

if __name__ == "__main__":
    app.run("127.0.0.1", debug=True, port=8080)
# [END python_app]

"""    
@app.route("/2")
def get_request2():
    payloadStops = {'key':'3a03f90d-7ca3-4b74-b22f-8b6535e6d788','OperatorRef':'MTA','MonitoringRef':'306582','Li':'NYCT_B11','StopMonitoringDetailLevel':'basic','MaximumStopVisits':'1','MinimumStopVisitsPerLine':'1'}
    objStops = requests.get('http://bustime.mta.info/api/siri/stop-monitoring.json', params=payload)
    resStops = obj.json()
    stops = res['Siri']['ServiceDelivery']['StopMonitoringDelivery'][0]['MonitoredStopVisit'][0]['MonitoredVehicleJourney']['MonitoredCall']['Extensions']['Distances']['StopsFromCall']
    return str(stops)
    
"""


