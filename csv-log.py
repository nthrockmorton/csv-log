import sys
import time
import datetime
import urllib2
import json

import Adafruit_DHT

# Type of sensor
DHT_TYPE = Adafruit_DHT.DHT22

# Sensor Connected to pin 4
DHT_PIN  = 4

# Put near the beginning to open file and write header
csv = open('sensor_log.csv', 'w')
csv.write(",".join(['datetime', 'int_temp', 'temp','humidity', 'rel_humidity', 'condition', 'location']))

# How long to wait (in seconds) between measurements.
FREQUENCY_SECONDS      = 10

#Access URL of wunderground API
f = urllib2.urlopen('http://api.wunderground.com/api/4f8a332ddf048e1a/conditions/q/MN/Minneapolis.json')

#read and parse the JSON file from wunderground
json_string = f.read()
parsed_json = json.loads(json_string)

#variables from JSON
location = parsed_json['current_observation']['display_location']['full']
temp_f = parsed_json['current_observation']['temp_f']
current_condition = parsed_json['current_observation']['weather']
rel_humidity = parsed_json['current_observation']['relative_humidity']



i = 0
for i in range(0,350):

        # Attempt to get sensor reading.
        humidity, temp = Adafruit_DHT.read(DHT_TYPE, DHT_PIN)


        # Skip to the next reading if a valid measurement couldn't be taken.
        if humidity is None or temp is None:
                time.sleep(2)
                continue
         
        timestamp = str(datetime.datetime.now())
                
        print (i)
        print ('Temperature: {0:0.1f} C').format(temp)
        print ('Humidity:    {0:0.1f} %').format(humidity)
        print "Current temperature in %s is: %s F" % (location, temp_f)
        print "Current weather is %s in %s" % (current_condition, location)
        print "Current relative humidity is %s in %s" % (rel_humidity, location)

# Put at after each reading is done
        csv.write(",".join([timestamp, temp,temp_f, humidity, rel_humidity, current_condition, location]))

# Append the data in the spreadsheet, including a timestamp
        try:
                worksheet.append_row((datetime.datetime.now(), int_temp_f, temp_f, humidity, rel_humidity, current_condition, location))
        except:
                # Error appending data, most likely because credentials are stale.
                # Null out the worksheet so a login is performed at the top of the loop.
                print ('Append error, logging in again')
                worksheet = None
                time.sleep(FREQUENCY_SECONDS)
                continue

        # Wait 30 seconds before continuing
        print ('Wrote a row to {0}').format(GDOCS_SPREADSHEET_NAME)
        f.close()
        csv.close()
        time.sleep(FREQUENCY_SECONDS)


