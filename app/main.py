import os
import sys
import json
import time
import tweepy
import facebook
import serial

config = json.loads(open('config.json').read())

mySerial = serial.Serial('/dev/serial0', 9600, timeout = 1)

# ---------------------------------- Facebook ----------------------------------
graph = facebook.GraphAPI(access_token=config['facebookAccessToken'], version=2.10)

# ---------------------------------- Twitter -----------------------------------
auth = tweepy.OAuthHandler(config['twitterConsumerKey'], config['twitterConsumerSecret'])
auth.set_access_token(config['twitterAccessToken'], config['twitterAccessTokenSecret'])
api = tweepy.API(auth)
# ------------------------------------------------------------------------------

def printToLcd(pos, text):
    mySerial.write(chr(0xfe))
    mySerial.write(chr(0x80 + pos))
    mySerial.write(text)

def clearLcd():
    mySerial.write(chr(0xfe)) # Control Character
    mySerial.write(chr(0x01)) # Clear screen

clearLcd()
printToLcd(0, "Starting v." + str(config['applicationVersion']))
printToLcd(64, "Embriq SOME")
time.sleep(3)

clearLcd()
printToLcd(0, "Facebook:")
printToLcd(64, "Twitter:")

while True:
    try:
        numberOffacebookFollowers = graph.get_object(id=config['facebookCompanyId'], fields='fan_count')['fan_count']
        numberOfTwitterFollowers = api.get_user(config['twitterUser']).followers_count

        printToLcd(0+10, str(numberOffacebookFollowers));
        printToLcd(64+10, str(numberOfTwitterFollowers));

        time.sleep(config['pollIntervalSeconds'])

    except:
        clearLcd()
        printToLcd(0, "Program stopped");
        printToLcd(64, "Try restarting");
        mySerial.close()
        raise
