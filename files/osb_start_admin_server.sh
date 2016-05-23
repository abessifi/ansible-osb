#!/bin/bash

set -e

SCRIPT=$(readlink -f $0)
SCRIPT_PATH=$(dirname $SCRIPT)

source ${SCRIPT_PATH}/osb_set_environment_variables.sh

start_admin_server() {
	${FUSION_MIDDLEWARE_HOME}/common/bin/wlst.sh -loadProperties ${SCRIPT_PATH}/osb_environment.properties ${SCRIPT_PATH}/osb_start_admin_server.py
}

start_admin_server
