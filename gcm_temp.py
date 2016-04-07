#!/usr/bin/python
import subprocess 
import glob
from script import getValueFromFile, activated_file

action_command_send = 'php gcm.php '
message_chauffage = '2'

############################################################
#                   Main Program                           #
############################################################

def main():
	if getValueFromFile(activated_file).lower()=="true":
		#send notifcation
		proc = subprocess.Popen(action_command_send + message_chauffage, shell=True, stdout=subprocess.PIPE)
		script_response = proc.stdout.read()
		print script_response
		
if __name__ == "__main__":
	main()