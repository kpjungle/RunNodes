#!/usr/bin/python

# Version 1.3
# Author: Kim Pedersen
# Email: k.jungle@gmail.com
# Twitter: @kpjungle
# Website: www.packet-forwarding.net

from netmiko import ConnectHandler
import time;
import sys;


# Static information you might want to change ;)
ip_of_esxi_host = "8.8.8.8"
username_of_esxi_host = "root"
password_of_esxi_host = "SuperSecret"


ESXiHost = {
'device_type': 'cisco_ios',
'ip': ip_of_esxi_host,
'username': username_of_esxi_host,
'password': password_of_esxi_host,
'port' : 22, 
'secret': 'ENABLE', 
'verbose': False, 
}


# Global Variables
is_connected = True

# Dictionary holding device names and ID's
my_dict = {}

# Try and connect to the device
try:
    net_connect = ConnectHandler(**ESXiHost)
except:
    print "Couldnt connect... :("
    is_connected = False
    pass

# Try and get all VM's
try:
    output = net_connect.send_command('vim-cmd vmsvc/getallvms')
except:
    print "Couldnt get all VM's"
    is_connected = True
    pass


# Split it into manageable pieces
organized_output = output.split('\n')


counter = 1
while counter < len(organized_output):
    split_line = organized_output[counter].split('    ')

    # Find CSR's
    if split_line[1] == 'Cisco CSR1Kv - 1':
        my_dict['R1'] = split_line[0]
    if split_line[1] == 'Cisco CSR1Kv - 2':
        my_dict['R2'] = split_line[0]
    if split_line[1] == 'Cisco CSR1Kv - 3':
        my_dict['R3'] = split_line[0]
    if split_line[1] == 'Cisco CSR1Kv - 4':
        my_dict['R4'] = split_line[0]
    if split_line[1] == 'Cisco CSR1Kv - 5':
        my_dict['R5'] = split_line[0]
    if split_line[1] == 'Cisco CSR1Kv - 6':
        my_dict['R6'] = split_line[0]
    if split_line[1] == 'Cisco CSR1Kv - 7':
        my_dict['R7'] = split_line[0]
    if split_line[1] == 'Cisco CSR1Kv - 8':
        my_dict['R8'] = split_line[0]
    if split_line[1] == 'Cisco CSR1Kv - 9':
        my_dict['R9'] = split_line[0]


    # Find XR's
    if split_line[1] == 'Cisco IOS XRv - 1':
        my_dict['XR1'] = split_line[0]
    if split_line[1] == 'Cisco IOS XRv - 2':
        my_dict['XR2'] = split_line[0]
    if split_line[1] == 'Cisco IOS XRv - 3':
        my_dict['XR3'] = split_line[0]
    if split_line[1] == 'Cisco IOS XRv - 4':
        my_dict['XR4'] = split_line[0]
    if split_line[1] == 'Cisco IOS XRv - 5':
        my_dict['XR5'] = split_line[0]
    if split_line[1] == 'Cisco IOS XRv - 6':
        my_dict['XR6'] = split_line[0]
    if split_line[1] == 'Cisco IOS XRv - 7':
        my_dict['XR7'] = split_line[0]
    if split_line[1] == 'Cisco IOS XRv - 8':
        my_dict['XR8'] = split_line[0]
    if split_line[1] == 'Cisco IOS XRv - 9':
        my_dict['XR9'] = split_line[0]
    
    
    counter = counter + 1



# Function to issue the start command to the router (VM)
def start_router(Router_Name):
    return_value = True
    Router_ID = my_dict[Router_Name]
    command_to_issue = "vim-cmd vmsvc/power.on " + Router_ID
    
    # Boot the router
    try:
        output = net_connect.send_command(command_to_issue)
    except:
        print "Couldnt Start the VM"
        return_value = False
        pass
    
    return return_value


# Function to issue the stop command to the router (VM)
def stop_router(Router_Name):
    return_value = True
    Router_ID = my_dict[Router_Name]
    command_to_issue = "vim-cmd vmsvc/power.off " + Router_ID
    
    # Shutdown the router
    try:
        output = net_connect.send_command(command_to_issue)
    except:
        print "Couldnt Stop the VM"
        return_value = False
        pass
    
    return return_value


# Check parameters
if len(sys.argv) == 1:
    print "Usage: RunNodes.py <start/stop> <router-name1> <router-name2> .."
else:
    # Which action to perform
    action = sys.argv[1];
    
    # Start/Stop the Routers
    router_counter = 2
    while router_counter < len(sys.argv):
        if action == "start":
            if (start_router(sys.argv[router_counter])):
                print sys.argv[router_counter] + " Started... Have fun!"
                if action == "stop":
                    if (stop_router(sys.argv[router_counter])):
                        print sys.argv[router_counter] + " Stopped... Have a great break!"
        
        router_counter = router_counter + 1


# Close the connection
if is_connected:
    net_connect.disconnect()

