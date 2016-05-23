#!/bin/bash

set -e

SCRIPT=$(readlink -f $0)
SCRIPT_PATH=$(dirname $SCRIPT)

source ${SCRIPT_PATH}/osb_set_environment_variables.sh

create_basic_domain() {
	${FUSION_MIDDLEWARE_HOME}/common/bin/wlst.sh -loadProperties ${SCRIPT_PATH}/osb_environment.properties ${SCRIPT_PATH}/osb_create_basic_domain.py
}

change_memory_settings() {

	echo '[INFO] Change DERBY flag'
	sed -i -e '/DERBY_FLAG="true"/ s:DERBY_FLAG="true":DERBY_FLAG="false":' ${DOMAIN_CONFIGURATION_HOME}/bin/setDomainEnv.sh

}

create_basic_domain

change_memory_settings
