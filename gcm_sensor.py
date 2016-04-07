#!/usr/bin/python
import subprocess 
 
action_command_send = 'php gcm.php '
message_capteur = '1'
base_dir = '/sys/bus/w1/devices/'
nb_device = len(glob.glob(base_dir + '28*'))


############################################################
#                   Main Program                           #
############################################################

def main():
	if nb_device==0:
		#send notifcation
		proc = subprocess.Popen(action_command_send + message_capteur, shell=True, stdout=subprocess.PIPE)
		script_response = proc.stdout.read()
		print script_response
		
if __name__ == "__main__":
	main()