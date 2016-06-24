import sys
from java.io import FileInputStream
from com.bea.wli.config.customization import Customization
from com.bea.wli.sb.management.importexport import ALSBImportOperation
from com.bea.wli.sb.management.configuration import ALSBConfigurationMBean
from com.bea.wli.sb.management.configuration import SessionManagementMBean
from com.bea.wli.sb.util import Refs

# Set parameters from environment variables and the sourced property file passed
# as argument to the script.
print '[INFO] Setting parameters..'
domain_configuration_home = os.getenv('DOMAIN_CONFIGURATION_HOME')
admin_server_url = 't3://' + admin_server_listen_address + ':' + admin_server_listen_port
admin_server_config_file = domain_configuration_home + '/admin_server_config_file.properties'
admin_server_key_file = domain_configuration_home + '/admin_server_key_file.properties'

def readBinaryFile(fileName):
    file = open(fileName, 'rb')
    bytes = file.read()
    return bytes

def printOpsMap(map):
    """
    Utility function to print the list of operations
    """
    ops_set = map.entrySet()
    for entry in ops_set:
        print "%s %s" % (entry.getValue().getOperation(), entry.getKey())

def printDiagMap(map):
   """
   Utility function to print the diagnostics
   """
   diag_set = map.entrySet()
   for entry in diag_set:
       print entry.getValue().toString()

def importSBConfigFile(config_mbean):

    print "[DEBUG] Read SBConfig file '%s'", sbconfig_jar_file
    theBytes = readBinaryFile(sbconfig_jar_file)
    print "[INFO] Loading SBConfig JAR file"
    config_mbean.uploadJarFile(theBytes)
    print "[INFO] SBConfig JAR loaded"

    if not sbconfig_project:
        print "[WARN] No project specified, additive deployment performed"
        alsbJarInfo = config_mbean.getImportJarInfo()
        alsbImportPlan = alsbJarInfo.getDefaultImportPlan()
        alsbImportPlan.setPassphrase(passphrase)
        alsbImportPlan.setPreserveExistingEnvValues(true)
        importResult = config_mbean.importUploaded(alsbImportPlan)
    else:
        print "[INFO] OSB project '%s' will get overlaid" % sbconfig_project
        alsbJarInfo = config_mbean.getImportJarInfo()
        print "[INFO] Use default import plan"
        alsbImportPlan = alsbJarInfo.getDefaultImportPlan()
        #alsbImportPlan.setPassphrase(passphrase)
        operationMap=HashMap()
        operationMap = alsbImportPlan.getOperations()
        print "[DEBUG] Show import operations"
        printOpsMap(operationMap)
        ops_set = operationMap.entrySet()
        alsbImportPlan.setPreserveExistingEnvValues(true)

        # Use a flag to check importation status
        abort = false
        # List of created refs
        createdRef = ArrayList()

        for item in ops_set:
            ref = item.getKey()
            op = item.getValue()
            # Set different logic based on the resource type
            ref_type = ref.getTypeId
            if ref_type == Refs.SERVICE_ACCOUNT_TYPE or ref_type == Refs.SERVICE_PROVIDER_TYPE:
                if op.getOperation() == ALSBImportOperation.Operation.Create:
                    print "[WARN] Unable to import a service account or a service provider on a target system", ref
                    abort = true
            elif op.getOperation() == ALSBImportOperation.Operation.Create:
                # Keep the list of created resources
                createdRef.add(ref)

        if abort:
            raise

        importResult = config_mbean.importUploaded(alsbImportPlan)

        print "[DEBUG] Show import diagnostics"
        printDiagMap(importResult.getImportDiagnostics())

        if not importResult.getFailed().isEmpty():
            print "[ERROR] One or more resources could not be imported properly"
            raise

def applyCustomizationFile(config_mbean):
    print "[INFO] Loading customization file '%s'" % sbconfig_customization_file
    iStream = FileInputStream(sbconfig_customization_file)
    customizationList = Customization.fromXML(iStream)
    config_mbean.customize(customizationList)

def main():
    SessionMBean = None
    try:
        # Connect to AdminServer to issue commands and control the Managed Servers
        print "[INFO] Connecting to AdminServer.."
        if os.path.isfile(admin_server_config_file) and os.path.isfile(admin_server_key_file):
            print "[INFO] Authentication type: 'key_file'"
            connect(userConfigFile=admin_server_config_file, userKeyFile=admin_server_key_file, \
                    url=admin_server_url)
        else:
            print "[INFO] Authentication type: 'login/password'"
            connect(admin_username, admin_password, admin_server_url)

        # Create a configuration session
        domainRuntime()
        sessionName = String("Customization" + Long(System.currentTimeMillis()).toString())
        SessionMBean = findService("SessionManagement", "com.bea.wli.sb.management.configuration.SessionManagementMBean")
        SessionMBean.createSession(sessionName)
        OSBConfigurationMBean = findService(String("ALSBConfiguration.").concat(sessionName), "com.bea.wli.sb.management.configuration.ALSBConfigurationMBean")
        # Import OSB project(s) from an SB jar file
        try:
            importSBConfigFile(OSBConfigurationMBean)
            # Apply XML customization file
            applyCustomizationFile(OSBConfigurationMBean)
            # Apply changes and save the configuration session
            SessionMBean.activateSession(sessionName, "Import OSB project")
            print "[INFO] Successfully Completed importation and customization"
        except Exception, error:
	    print error
            print "[ERROR] This jar must be imported manually to resolve references and ressources dependencies"
            # Quit the MBean configuration session
            SessionMBean.discardSession(sessionName)
            # Exit the WLST session with exitcode=1
            exit(defaultAnswer='y', exitcode=1)

        # Disconnect from the WLST session
        disconnect()

    except:
        print "[ERROR] Unexpected error:", sys.exc_info()[0]
        if SessionMBean != None:
            SessionMBean.discardSession(sessionName)
        raise

main()
