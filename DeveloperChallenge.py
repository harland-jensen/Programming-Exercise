import csv, sys, json, time, re, requests
from re import T
from os.path import exists


def get_file_name():
    """
    get_file_name()
    Prompts user for filename 
    Returns: 
    string: Given filename
    """
    print("Enter a filename:")
    return input()      

def get_token():
    """
    get_token()
    Prompts user for token 
    Returns: 
    string: Given token
    """
    print("Enter a token:")
    return input()    

def validate_file(file):
    """
    validate_file(file)
    Function which validates user inputted file can be opened. 

    Params: 
    file (string): Filename provided
    
    Returns: 
    1 if file can be opened, 0 otherwise
    """
    try:
        f = open(file)
        return 1

    except FileNotFoundError:
        print("Invalid file address")
        return 0

def send_message(token, line):
    """
    send_message(line)

    Function which attempts to send an sms using the mailjet API.

    Params:
    Token (string): User's mailjet token
    Line (List): List of fields obtained from a line of the provided csv file

    """
    (clientName, state, number, message) = line
    print(clientName, state, number, message)
    headers = {"Authorization" : f"Bearer {token}", 'Content-Type' : 'application/json'}
    url = "https://api.mailjet.com/v4/sms-send"
    data = json.dumps({
        "Text": f"{message}",
        "To": f"{number}",
        "From": "Harland"
        })
    response = requests.post(url, data = data, headers = headers)
   
def receive_status(token):
    """
    receive_status()

    Function which prints the total number of successful and unsuccessful sms messages that have been sent 
    in the past three months

    Params: 
    Token (string): User's mailjet token
    """
    headers = {"Authorization" : f"Bearer {token}"}
    
    successUrl = "https://api.mailjet.com/v4/sms/count?StatusCode=1,2,3"
    unsuccessUrl = "https://api.mailjet.com/v4/sms/count?StatusCode=4,5,6,7,8,9,10,11,12,13,14"
    successfulSends = requests.get(successUrl, headers = headers)
    unsuccessfulSends = requests.get(unsuccessUrl, headers = headers)

    countSuccess = successfulSends.text.split(":")[1].strip('}')
    countUnsuccess = unsuccessfulSends.text.split(":")[1].strip('}')
    print("Successful sends:", countSuccess)
    print("Unsuccessful sends:", countUnsuccess)


def validate_line(line):
    """
    validate_line(line)

    Function which validates that the provided phone number is of the correct format. If the provided
    phone number does not conform with the required format, raises the issue with user and exits with 
    status 3. 
    
    Params: 
    Line (List): List of fields obtained from a line of the provided csv file


    """
    try:
        #Establish whether provided phone number meets format required by the Mailjet API
        match = re.search("[+]\d{11}", line[2])
    except AttributeError:
        print("Unable to process number, should be of format [+ : Area Code : Number]")
        exit(3)

def generate_csv(token, timeBefore):
    """
    generate_csv(timeBefore)

    Function which creates a csv of sms messages which failed to send correctly. This csv is generated from 
    messages the user sent in the past three months.
    csv is named UnsuccessfulSends.csv

    Params: 
    Token (string): User's mailjet token
    timeBefore (int): Integer representing time before the program was run.
    """
    headers = {"Authorization" : f"Bearer {token}"}
    url = "https://api.mailjet.com/v4/sms?StatusCode=4,5,6,7,8,9,10,11,12,13,14"

    stats = requests.get(url, headers = headers)
    print(stats.text)
    with open('UnsuccessfulSends.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow([stats.text])


    


def initialise_reader():
    """
    initialise_reaeder()

    Function which prompts the user for a filename if not provided as a command-line argument, and continually
    prompts user for a correct filename if it is not able to be opened. Then proceeds to send messages for each
    line in the provided csv file. 

    Csv file is assumed to have a row of headers on the first line, followed by data. 
    Each line in the csv is checked to ensure it has four fields, if not user is notified and the program
    will exit with status 2. 
    
    """
    if len(sys.argv) == 1: 
        file = get_file_name()
        token = get_token()
    elif len(sys.argv) == 2:
        file = sys.argv[1]
        token = get_token()
    else:
        file = sys.argv[1]
        token = sys.argv[2]

    while validate_file(file) != 1:
        file = get_file_name()
        print("Your file was:" + file) 

    with open(file, 'r') as csvfile:
        #create csv reader
        csvreader = csv.reader(csvfile)

        #Obtain headers-> Should be name, state, mobile#, message
        headers = next(csvreader)
        timeBefore = int(time.time())

        for line in csvreader:
            #Check csv has four fields of data
            if (len(line) != 4):
                print("CSV incorrectly formatted, should be: [client name, state, mobile number, message]")
                exit(2)
            validate_line(line)
            send_message(token, line)

        receive_status(token)
        generate_csv(token, timeBefore)

def main():
    """
    main()
    Function which calls initialise_reader. 
    """
    initialise_reader()
        
    

if __name__ == "__main__":
    main() 
    