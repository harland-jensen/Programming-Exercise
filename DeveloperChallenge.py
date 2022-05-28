import csv, sys, fileinput
import requests
import string
from os.path import exists

def get_file_name():
    print("Enter a filename:")
    return input()      

def validate_file(file):
    try:
        f = open(file)
        return 1

    except FileNotFoundError:
        print("Invalid file address")
        return 0

def main():
    if len(sys.argv) == 1: 
        file = get_file_name()
    else:
        file = sys.argv[1]

    while validate_file(file) != 1:
        file = get_file_name()
        print("Your file was:" + file) 

"""
# Create : Send SMS Message to a selected recipient.
curl -X POST \
 https://api.mailjet.com/v4/sms-send \
  
  -d '{

  }'

"""

if __name__ == "__main__":
    #main() 
    headers = {"Authorization" : "Bearer $MJ_TOKEN", 'Content-Type' : 'application/json'}
    url = "https://webhook.site/e511b7e5-628a-463e-9424-65fe3a727c0b"
    data = {"Text": "Have a nice SMS flight with Mailjet !",
    "To": "+33600000000",
    "From": "MJPilot"}
    requests.post(url, data = data, headers = headers  )