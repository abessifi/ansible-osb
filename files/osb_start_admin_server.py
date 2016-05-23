import socket;
import os.path;

print '[INFO] Setting parameters..';
domain_application_home = os.getenv('DOMAIN_APPLICATION_HOME');
domain_configuration_home = os.getenv('DOMAIN_CONFIGURATION_HOME');
domain_name = os.getenv('DOMAIN_NAME');
fusion_middleware_home = os.getenv('FUSION_MIDDLEWARE_HOME');
middleware_home = os.getenv('MIDDLEWARE_HOME');
nodemanager_home = os.getenv('NODE_MANAGER_HOME');
weblogic_home = os.getenv('WEBLOGIC_HOME');

nodemanager_config_file = domain_configuration_home +'/nodemanager_config_file.properties';
nodemanager_key_file = domain_configuration_home + '/nodemanager_key_file.properties';

print '[INFO] Connecting to NodeManager..';
if os.path.isfile(nodemanager_config_file) and os.path.isfile(nodemanager_key_file):
    print "[INFO] Authentication type: 'key_file'";
    nmConnect(userConfigFile=nodemanager_config_file, userKeyFile=nodemanager_key_file, \
              host=nodemanager_listen_address, port=nodemanager_listen_port, domainName=domain_name, \
              domainDir=domain_configuration_home, nmType=nodemanager_connection_mode);
else:
    print "[INFO] Authentication type: 'login/password'";
    nmConnect(nodemanager_username, nodemanager_password, nodemanager_listen_address, \
              nodemanager_listen_port, domain_name, domain_configuration_home, nodemanager_connection_mode);

print '[INFO] Start AdminServer..';
nmStart(admin_server_name);

print '[INFO] Disconnecting from NodeManager..';
nmDisconnect();

print '[INFO] Done !'
