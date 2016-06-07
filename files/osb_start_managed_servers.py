import os.path;

print '[INFO] Setting parameters..';
domain_application_home = os.getenv('DOMAIN_APPLICATION_HOME');
domain_configuration_home = os.getenv('DOMAIN_CONFIGURATION_HOME');
domain_name = os.getenv('DOMAIN_NAME');
fusion_middleware_home = os.getenv('FUSION_MIDDLEWARE_HOME');
middleware_home = os.getenv('MIDDLEWARE_HOME');
nodemanager_home = os.getenv('NODE_MANAGER_HOME');
weblogic_home = os.getenv('WEBLOGIC_HOME');

admin_server_url = 't3://' + admin_server_listen_address + ':' + admin_server_listen_port;
admin_server_config_file = domain_configuration_home + '/admin_server_config_file.properties';
admin_server_key_file = domain_configuration_home + '/admin_server_key_file.properties';

print '[INFO] Connecting to AdminServer..';
if os.path.isfile(admin_server_config_file) and os.path.isfile(admin_server_key_file):
    print "[INFO] Authentication type: 'key_file'";
    connect(userConfigFile=admin_server_config_file, userKeyFile=admin_server_key_file, \
            url=admin_server_url);
else:
    print "[INFO] Authentication type: 'login/password'";
    connect(admin_username, admin_password, admin_server_url);

print '[INFO] Starting managed servers..';
domainRuntime();
server_lifecycles = cmo.getServerLifeCycleRuntimes();

for server_lifecycle in server_lifecycles:
    if (server_lifecycle.getState() == 'SHUTDOWN' and \
        server_lifecycle.getName() != admin_server_name):
        print '[INFO] Start server ' + server_lifecycle.getName();
        task = server_lifecycle.start();
        java.lang.Thread.sleep(1000);
        print '[INFO] %s, %s' % (task.getStatus(), server_lifecycle.getState());
    else:
        print '[INFO] Server %s is in %s state and will not be started' % \
                (server_lifecycle.getName(), server_lifecycle.getState());

print '[INFO] Disconnecting from AdminServer..';
disconnect();

print '[INFO] Done !'
