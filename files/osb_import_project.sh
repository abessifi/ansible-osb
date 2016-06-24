#!/bin/bash

set -e

SCRIPT=$(readlink -f $0)
SCRIPT_PATH=$(dirname $SCRIPT)

# Set environement variables
source ${SCRIPT_PATH}/osb_set_environment_variables.sh
source ${OSB_HOME}/tools/configjar/setenv.sh

${OSB_HOME}/tools/configjar/wlst.sh \
  -loadProperties ${SCRIPT_PATH}/../config/osb_environment.properties \
  ${SCRIPT_PATH}/osb_import_project.py
