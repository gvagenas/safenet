#!flask/bin/python
from flask import Flask, request
import handle_emergency, handle_mac_addr
import logging as logger

app = Flask(__name__)


@app.route('/about')
def about():
    return  'SafeNet REST API. Use /alarm?location=[your_location] Endpoint to create new Alarm '

@app.route('/alarm')
def alert():
    location = request.args.get('location')
    logger.info("New Alarm request for location %s", location)

    numOfPeople = handle_mac_addr.get_macs_for_location(location)
    handle_emergency.raise_alarm(location, numOfPeople)

    msg = ("Alarm received for location \"%s\" where there are %s people, will handle emergency" % (location, numOfPeople))
    return msg

def start_restapi():
    logger.info('About to start Rest API on 0.0.0.0:5000')
    # app.run(debug=True)
    # If use_reloader is not FALSE, then Flask will fork() to two
    # Check here: https://stackoverflow.com/a/24618018
    app.run(host='0.0.0.0', debug=True, use_reloader=False)
    logger.info('Rest API started on 0.0.0.0')

if __name__ == '__main__':
    print('Main Line Starting')

    # app.run(debug=True)
    # If use_reloader is not FALSE, then Flask will fork() to two
    # Check here: https://stackoverflow.com/a/24618018
    app.run(host='0.0.0.0', debug=True, use_reloader=False)