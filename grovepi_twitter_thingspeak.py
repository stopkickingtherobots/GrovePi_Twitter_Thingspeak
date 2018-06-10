# Tweet the temperature, light, and sound levels with our Raspberry Pi
# http://www.dexterindustries.com/GrovePi/projects-for-the-raspberry-pi/raspberry-pi-twitter-sensor-feed/

# GrovePi + Sound Sensor + Light Sensor + Temperature Sensor + LED
# http://www.seeedstudio.com/wiki/Grove_-_Sound_Sensor
# http://www.seeedstudio.com/wiki/Grove_-_Light_Sensor
# http://www.seeedstudio.com/wiki/Grove_-_Temperature_and_Humidity_Sensor_Pro
# http://www.seeedstudio.com/wiki/Grove_-_LED_Socket_Kit

# Update by Benn Zeppelin

'''
## License

The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2017  Dexter Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
'''

import twitter
import time
import grovepi
import math
import datetime
import urllib2
import thingspeak

# Connections
sound_sensor = 0        # port A0
light_sensor = 1        # port A1
temperature_sensor = 2  # port D2
led = 3                 # port D3

intro_str = "Dexter Lab's"

# Connect to Twitter
api = twitter.Api(
    consumer_key='YOUR_KEY',
    consumer_secret='YOUR_SECRET',
    access_token_key='YOUR_TOKEN',
    access_token_secret='YOUR_SECRET'
    )

# Constants
THINGSPEAKKEY = 'ABCDEFGHIJKLMNOP'
THINGSPEAKCHANNEL = '123456'

# Update channel feeds
grovepi.pinMode(led,"OUTPUT")
grovepi.analogWrite(led,255)  #turn led to max to show readiness

while True:


    # Error handling in case of problems communicating with the GrovePi
    try:

        # Get value from light sensor
        light_intensity = grovepi.analogRead(light_sensor)    
        
        # Give PWM output to LED
        grovepi.analogWrite(led,light_intensity/4)

        # Get sound level
        sound_level = grovepi.analogRead(sound_sensor)

        # Get value from temperature sensor
        [t,h]=[0,0]
        [t,h] = grovepi.dht(temperature_sensor,0)
        
        time.sleep(0.5)
        
        # Get current date and time
        clock = datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S")

        # Post a tweet
        out_str ="%s Temp: %d C, Humidity: %d, Light: %d, Sound: %d, Time: %s" %(intro_str,t,h,light_intensity/10,sound_level, clock)
        print (out_str)
        api.PostUpdate(out_str)
    except IOError:
        print("Error")
    except KeyboardInterrupt:
        exit()
    except Exception as e:
        print("Duplicate Tweet or Twitter Refusal: {}".format(e))
        
    channel = thingspeak.Channel(id=THINGSPEAKCHANNEL,write_key=THINGSPEAKKEY)
    
    try:
        response = channel.update({1:t, 2:h, 3:light_intensity/10, 4:sound_level})
        print ("Thingspeak Updated.\n" )        
    except:
        print ("connection failed")

    time.sleep(299)
