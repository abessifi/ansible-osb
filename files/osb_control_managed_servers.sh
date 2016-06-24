#!/bin/bash

set -e

SCRIPT=$(readlink -f $0)
SCRIPT_PATH=$(dirname $SCRIPT)
SUPPORTED_CONTROL_ACTIONS=(stop start)

usage(){
	echo "[ERROR] Usage: $0 {stop|start}"
	exit 1
}

control_managed_servers() {
	${FUSION_MIDDLEWARE_HOME}/common/bin/wlst.sh \
		-loadProperties ${SCRIPT_PATH}/../config/osb_environment.properties \
		${SCRIPT_PATH}/osb_control_managed_servers.py $CONTROL_ACTION
}

if [ $# -ne 1 ]; then
	usage
fi

if [[ ! ${SUPPORTED_CONTROL_ACTIONS[*]} =~ "$1" ]]; then
	usage
else
	CONTROL_ACTION="$1"
fi

source ${SCRIPT_PATH}/osb_set_environment_variables.sh

control_managed_servers
