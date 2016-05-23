# -*- mode: ruby -*-
# vi: set ft=ruby :

ORACLE_BASE_DIR="/u01/app/oracle"
ORACLE_MIDDLEWARE_DIR="#{ORACLE_BASE_DIR}/product/middleware"
OSB_HOME_DIR="#{ORACLE_MIDDLEWARE_DIR}/osb"
WEBLOGIC_DOMAIN_HOME="#{ORACLE_MIDDLEWARE_DIR}/user_projects/domains/osb_domain"
WEBLOGIC_NODEMANAGER_HOME="#{ORACLE_MIDDLEWARE_DIR}/user_projects/nodemanagers/osb_domain"
WEBLOGIC_ADMIN_SERVER_HOME="#{WEBLOGIC_DOMAIN_HOME}/servers/AdminServer"
WEBLOGIC_MANAGED_SERVER_HOME="#{WEBLOGIC_DOMAIN_HOME}/servers/OSB_Server_1"
