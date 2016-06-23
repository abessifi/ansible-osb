import os.path
import sys

def control_managed_servers(action, current_expected_status):
    """
    Control managed servers status using MBean objects.
    Supported actions are 'start' and 'stop'.
    """
    is_failed=false
    try:
        domainRuntime()
        server_lifecycles = cmo.getServerLifeCycleRuntimes()
        for server_lifecycle in server_lifecycles:
            server_status = server_lifecycle.getState()
            server_name = server_lifecycle.getName()
            if (server_status in current_expected_status and server_name != admin_server_name):
                print "[DEBUG] '%s' server status is: %s" % (server_name, server_status)
                if (control_action == 'start'):
                    print "[INFO] Starting server %s.." % server_name
                    task = server_lifecycle.start()
                elif (control_action == 'stop'):
                    print "[INFO] Stopping server %s.." % server_name
                    task = server_lifecycle.shutdown(1000, java.lang.Boolean('true'))
                java.lang.Thread.sleep(1000)
    except:
        dumpStack()
        print "[ERROR] Failed to %s '%s' server !" % (control_action, server_name)
        is_failed=true

    return is_failed

# Get control action from the command line
control_action=sys.argv[1]
# Set parameters from environment variables and the sourced property file passed
# as argument to the script.
print '[INFO] Setting parameters..'
domain_configuration_home = os.getenv('DOMAIN_CONFIGURATION_HOME')
admin_server_url = 't3://' + admin_server_listen_address + ':' + admin_server_listen_port
admin_server_config_file = domain_configuration_home + '/admin_server_config_file.properties'
admin_server_key_file = domain_configuration_home + '/admin_server_key_file.properties'

# Connect to AdminServer to issue commands and control the Managed Servers
print '[INFO] Connecting to AdminServer..'
if os.path.isfile(admin_server_config_file) and os.path.isfile(admin_server_key_file):
    print "[INFO] Authentication type: 'key_file'"
    connect(userConfigFile=admin_server_config_file, userKeyFile=admin_server_key_file, \
            url=admin_server_url)
else:
    print "[INFO] Authentication type: 'login/password'"
    connect(admin_username, admin_password, admin_server_url)

# Control WLS instances/servers
if (control_action == 'start'):
    print '[INFO] Starting managed servers..'
    if control_managed_servers('start', ['SHUTDOWN', 'FAILED_NOT_RESTARTABLE']):
        exit(defaultAnswer='y', exitcode=1)
elif (control_action == 'stop'):
    print '[INFO] Stopping managed servers..'
    if control_managed_servers('stop', 'RUNNING'):
        exit(defaultAnswer='y', exitcode=1)

# Quit current session
print '[INFO] Disconnecting from AdminServer..'
disconnect()
