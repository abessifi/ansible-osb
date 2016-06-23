import socket
import os.path
import sys

# Get control action from the command line
control_action=sys.argv[1]
# Set parameters from environment variables and the sourced property file passed
# as argument to the script.
print '[INFO] Setting parameters..'
domain_configuration_home = os.getenv('DOMAIN_CONFIGURATION_HOME')
domain_name = os.getenv('DOMAIN_NAME')
nodemanager_config_file = domain_configuration_home +'/nodemanager_config_file.properties'
nodemanager_key_file = domain_configuration_home + '/nodemanager_key_file.properties'

# Connect to Nodemanager to control the AdminServer
print '[INFO] Connecting to NodeManager..'
if os.path.isfile(nodemanager_config_file) and os.path.isfile(nodemanager_key_file):
    print "[INFO] Authentication type: 'key_file'"
    nmConnect(userConfigFile=nodemanager_config_file, userKeyFile=nodemanager_key_file, \
              host=nodemanager_listen_address, port=nodemanager_listen_port, domainName=domain_name, \
              domainDir=domain_configuration_home, nmType=nodemanager_connection_mode)
else:
    print "[INFO] Authentication type: 'login/password'"
    nmConnect(nodemanager_username, nodemanager_password, nodemanager_listen_address, \
              nodemanager_listen_port, domain_name, domain_configuration_home, nodemanager_connection_mode)

# NOTE: The server status is logged twice.
# TODO: Check why nmServerStatus() logs to stdout despite the assignement action below
server_status = nmServerStatus(admin_server_name)
print "[DEBUG] Server status is: %s" % server_status

try:
    if (control_action == 'start') and (server_status != 'RUNNING'):
        print '[INFO] Starting AdminServer..'
        nmStart(admin_server_name)
    elif (control_action == 'stop') and (server_status == 'RUNNING') :
        print '[INFO] Stopping AdminServer..'
        nmKill(admin_server_name)
except:
    dumpStack()
    print "[ERROR] Failed to %s the AdminServer !" % control_action
    exit(defaultAnswer='y', exitcode=1)

# Quit current session
print '[INFO] Disconnecting from NodeManager..'
nmDisconnect()
