# mobileironAPI
Small and handy collection of script, which allows to interact with MobileIron 


Prerequisites:
- Python 3.7.2 installed
- Local MobileIron-Admin-User on Core:
  1. From the Admin Portal, select Admin > Admins.
  2. Select a user from the list of users.
  3. Select Actions > Edit Roles.
  4. Select the ‘API’ role, which is listed under Others.
  5. Click Save.
  
  Username/Password
      The web service requires authentication via username and password:
      Username: Username of any local or LDAP user who has the ‘API’ role.
      Password: The same password used to login to MobileIron Core the Admin Portal.
      
      
  Usage:
    userAPI.py -h 
    
    
    usage: userAPI.py [-h] mobileironUrl username password userId

    Retrieves various information about user and related devices from MobileIron
    API

    positional arguments:
      mobileironUrl  URL of your MobileIron-Core
      username       Username for BasicAuth
      password       Password for BasicAuth
      userId         User ID

    optional arguments:
      -h, --help     show this help message and exit
    
      
