# Embriq Social Media Followers App
Simple app getting follower count from different social media apps running on a Raspberry Pi. Currently gets likes from Facebook and followers on Twitter.

The Raspberry Pi is preloaded with a .sh script which is run aftter boot. This script will in turn run a python script downloading a .json configuration file and a .zip file containing the main application from an AWS S3 bucket. It will then unzip and start the main application. Multiple versions can be uploaded to the S3 bucket, and which version is run is determined by the configuration file.

The AWS part of this project can easily be skipped by manually transefering the application to the pi and modify the startup script.

## Hardware
Raspberry Pi Zero w (https://www.sparkfun.com/products/14277)
Serial LCD Screen (https://www.sparkfun.com/products/9394)

## Credentials for Facebook and Twitter
To use the python sdks for Facebook and Twitter you will need to register and get a set of credentials.
https://developers.facebook.com/
https://developer.twitter.com/en/docs

## Setting up the Pi
### AWS Setup
This is only one way to set up access to AWS resources for the Pi, and probably not the recomended way. The reason being that if someone has physical access to the Pi, they can easily remove the memory card and get the credentials. Therefore it is important to restrict the access this application has to your AWS resources. If you follow this setup the user will only have access to a designated S3 bucket. It might be worth to check out AWS IoT.

Create an IAM user for your Pi with programatic access and remeber to save the generated credentials. Attach the following policy:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:Get*",
                "s3:List*"
            ],
            "Resource": "<arn for your S3 bucket>"
        }
    ]
}
```
Create an S3 bucket (i named mine embriq-some-bucket) and attach the following policy.
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "<arn for your user>"
            },
            "Action": [
                "s3:Get*",
                "s3:List*"
            ],
            "Resource": "<arn for your S3 bucket>"
        }
    ]
}
```
Make a folder named .aws in the home directory of your Pi and add the two following files:
**config**
```
[default]
region = eu-west-1 (or your default region)
output = json
```
**credentials**
```
[default]
aws_access_key_id = <access key for Pi IAM user>
aws_secret_access_key = <secret access key for Pi IAM user>
```
### General Setup
Remember to enable serial (use raspi-config).

Get dependencies for python script. If pip is already istalled skip the first line.
```
sudo apt-get install python-pip
pip install pyserial
pip install boto3
pip install tweepy
pip install facebook-sdk
```
This makes it possible to use serial without elevated priviledge:
```
sudo usermod -a -G dialout pi
```
To run make the application on startup:
```
crontab -e
```
If you havent used crontab before this will prompt you to choose an editor. After that add the following to the bottom of the file:
```
@reboot cd /home/pi/programs/embriq-some && ./startUpScript.sh
```
## Configuration file
Determines what version of the application is downloaded and run, which sites to follow, polling interval and it is here you can configure your Facebook and Twitter credentials. For Twitter you can put in the name of the user you want to follow, but finding the right user for Facebook was a bit harder. A tip is to avigate to the desired Facebook page, inspect and look for `page_id`. E.g. https://www.facebook.com/Embriq/, left click, inspect and search.

## Utilities
I've included a couple of utility files making it easier to transfer the code and configration to S3 (`Makefile`) and to transfer the start up scripts to the Pi(`transfer-to-pi.sh`).

Run
```
make package
```
to make a .zip of the application
```
make upload
```
to transfer the .zip file to S3
```
make upload-config
```
to upload the config file to S3, or simply
```
make
```
to execute all steps.

Note that the AWS CLI must be installed and configured for the Makefile to work. See https://aws.amazon.com/cli/
