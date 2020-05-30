# Can be used to search Active Directory or other directory services that can be accessed via LDAP.
# In this example, we are searching the directory for all objects of the "user" class that are categorized as a "person"
# For each of those objects, we will receive the attributes lsited in the "searchattributes" list below.

import ldap3, json
ADdomain = 'domain.local'
ADusername = 'accountwithADaccess'
ADuserpass = 'accountpassword'

searchparams = {
    'objectClass':'user',
    'objectCategory':'person'
}

searchattributes = [
    'objectGUID',           #unique account ID
    'mail',                 #email
    'userPrincipalName',    #logon
    'givenName',
    'initials',
    'sn',                   #surname
    'employeeNumber',       
    'l',                    #location
]

def main():

    ADserver = ldap3.Server(ADdomain, use_ssl=False) # NOTE: PLEASE GET SECURE LDAP RUNNING ON THE DOMAIN CONTROLLER, THEN CHANGE use_ssl TO True
    ADconnection = ldap3.Connection(ADserver, user=ADdomain+"\\"+ADusername, password=ADuserpass, authentication=ldap3.NTLM, auto_bind=True)

    ADconnection.search('dc=domain,dc=local', '(&({}))'.format(')('.join('{}={}'.format(key, value) for key, value in searchparams.items())), attributes=searchattributes)
    adlist = {}
    for x in ADconnection.entries:
        loaditems = json.loads(x.entry_to_json())['attributes']

        if 'objectGUID' in loaditems:
            f = loaditems['objectGUID'][0]
            adlist[f] = {}
            # print(loaditems.items())
            for y, z in loaditems.items():
                if y == 'objectGUID':
                    continue
                if z == []:
                    adlist[f][y] = ''
                else:
                    adlist[f][y] = z[0]
    for x, y in adlist.items():
        print(str(x)+'  -  '+str(y))
    ADconnection.unbind()

main()
