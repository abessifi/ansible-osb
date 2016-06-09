#!/bin/bash

set -e

# Set environement variables
source ~/scripts/osb_set_environment_variables.sh

export JAVA_OPTIONS=-Djava.security.egd=file:///dev/urandom
export PATH=${DOMAIN_CONFIGURATION_HOME}/bin/:$PATH

# Check if the Nodemanager is running and start it if not.
if [ $(pgrep -c -f -u oracle weblogic.NodeManager) -eq 0 ]; then
    startNodeManager.sh
fi
