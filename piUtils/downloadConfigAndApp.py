import sys
import boto3
import json
import serial

bucketName = '<your bucket name>'

mySerial = serial.Serial('/dev/serial0', 9600, timeout = 1)

def printToLcd(pos, text):
    mySerial.write(chr(0xfe))
    mySerial.write(chr(0x80 + pos))
    mySerial.write(text)

def clearLcd():
    mySerial.write(chr(0xfe)) # Control Character
    mySerial.write(chr(0x01)) # Clear screen

try:
    clearLcd()
    s3_client = boto3.client('s3')

    printToLcd(0, "Downloading:")
    printToLcd(64, "config")
    s3_client.download_file(bucketName, 'config/config.json', 'config.json')

    config = json.loads(open('config.json').read())

    printToLcd(64, "app v" + str(config['applicationVersion']))
    s3_client.download_file(bucketName, 'application/embriq-some-' + config['applicationVersion'] + '.zip', 'app.zip')

    mySerial.close()

except:
    clearLcd()
    printToLcd(0, "Download error")
    printToLcd(64, "Try restarting")
    mySerial.close()
    sys.exit(1)
