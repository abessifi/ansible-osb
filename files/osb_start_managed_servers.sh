#!/bin/bash

set -e

SCRIPT=$(readlink -f $0)
SCRIPT_PATH=$(dirname $SCRIPT)

source ${SCRIPT_PATH}/osb_set_environment_variables.sh

start_managed_servers() {
	${FUSION_MIDDLEWARE_HOME}/common/bin/wlst.sh -loadProperties ${SCRIPT_PATH}/osb_environment.properties ${SCRIPT_PATH}/osb_start_managed_servers.py
}

start_managed_servers
