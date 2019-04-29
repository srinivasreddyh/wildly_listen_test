'''code for wav File monitoring
'''

from ftplib import FTP
import time
import argparse
import requests



DESCRIPTION = 'Input The path to the directory'
HELP = 'Input the path'
PARSER = argparse.ArgumentParser(description=DESCRIPTION)
PARSER.add_argument('-input_path', '--input_path', action='store',
                    help=HELP, default='/home/user-u0xzU/')

RESULT = PARSER.parse_args()
PRIMARY_PATH = "/home/user-u0xzU" + RESULT.input_path
print PRIMARY_PATH


#connect to ftp
def connect():
	''' fuction to connect it to FTP
  '''
	global ftp
	ftp = FTP('******', user='******', passwd='******')
	ftp.cwd(PRIMARY_PATH)
	print "connected to FTP", ftp.pwd()

#directory which you want to parse

#to get list of all the files
def sms():
	''' to send sms
	'''
	global URL, PAYLOAD, HEADERS
	URL = "https://www.fast2sms.com/dev/bulk"
	PAYLOAD = "sender_id=FSTSMS&message=NOTIFY_ME_ONCE&language=english&route=p&numbers=******"
	HEADERS = {'authorization': "******",
      			   'Content-Type': "application/x-www-form-urlencoded",
      			   'Cache-Control': "no-cache"}



def upload_status():
	''' Tell the status whether the file is uploaded or not
	'''
	names = ftp.nlst()
  #used flag to get notify only once if multiple files are uploaded
	flag = 0
  #store all the previous file in the dict to compare later
	before = dict([(f, None) for f in names])
	print before
	while 1:
    #time after which it will compare
		time.sleep(60)
    #get the list after that time
		names = ftp.nlst()
    #store the list obtain in the dict
		after = dict([(f, None) for f in names])
    #Check if the new files are added
		added = [f for f in after if f not in before]
		print added
		if added:
			print "Added: ", ", ".join(added)
      #check if we have already notifed or not
			if flag == 0:
				print "Notify me once"
				response = requests.request("POST", URL, data=PAYLOAD, headers=HEADERS)
				print response.text
			flag = 1
    #check if there is no files added in the directory
		if after == before:
			print "No files uploaded in 10 minutes"
			break
		before = after
if __name__ == '__main__':
	connect()
	sms()
	upload_status()
