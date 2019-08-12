import os
import shlex
import subprocess
import configparser

config = configparser.ConfigParser()
config.read('networker_fs.conf')
#check = config.sections()  #Will display headers in conf/ini file
#print(config['Client']['ClientName'])

#check if the parameters are being read correctly. rewritten: config['client']['ClientName']
checkClientName = config.get('Client','ClientName', fallback = 'Client name is invalid')
print(checkClientName)


#variables from conf file
clientName = config['Client']['ClientName']
protectionGroup = config['ProtectionGroup']['protectionGroupName']
workflowName = config['workflow']['workflowName']
policy = config['policy']['policyName']

#Checking if policy, workflow and protection group already exists


#Checking if the policy Exists
def checkPolicyName():
    cmd = 'nsrpolicy policy list'
    command = shlex.split(cmd)
    listOfPolicies = subprocess.Popen(command)
    if policy in listOfPolicies:
        return policy + ' exists'
    else:
        cmd = 'nsrpolicy policy create -p ' + policy
        command = shlex.split(cmd)
        subprocess.Popen(command)
        return policy + ' could not be found and it was created'

#Checking if the protection group Exists

def checkProtectionGroup():
    cmd = 'nsrpolicy group display -g ' + protectionGroup
    command = shlex.split(cmd)
    listOfGroups = subprocess.Popen()
    if protectionGroup in listOfGroups:
        return protectionGroup + ' exists'
    else:
        cmd = 'nsrpolicy group create -g ' + protectionGroup
        command = shlex.split(cmd)
        subprocess.Popen(command)
        return protectionGroup + ' could not be found and it was created'

#Checking if the workflow is already created
def checkWorkflowName():
    cmd = 'nsrpolicy workflow display -p ' + policy + ' -w ' + workflowName
    command = shlex.split(cmd)
    listOfWorkflows = subprocess.Popen(command)
    if workflowName in listOfWorkflows:
        return workflowName + ' exists'
    else:
        cmd = 'nsrpolicy workflow create -p ' + policy + ' -w ' + workflowName + ' -S ' +
               config['workflow']['workflowStartTime'] + ' -i ' + config['workflow']['workflowInterval'] +
               ' -u Yes -E Yes' + ' -g ' + config['ProtectionGroup']['protectionGroupName']
        command = shlex.split(cmd)
        subprocess.Popen(command)
        return policy + ' could not be found and it was created'


###### TO DO:
'''
1.Check if a policy/workflow/group does not exist, if it will be shown as available from the error message of nsrpolicy then it needs to be treated.
2. Create the backup action: nsrpolicy action create backup traditional -p policy -w workflow -A actionName/backup -e yes -t actionActivitySchedule -O actionOverride -P actionPeriod -r actionRetention -o actionPoolName -g protectionGroupName -y actionClientCanOverride
'''
