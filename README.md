

*****
  # DATABRICKS(python) Connect to PowerBI DataSet linked to DrectQuery to Azure Analysis Server(ssas_dax.py)
  
*****

I wanted to describe the steps & sample python script  to connect from Databricks to an Azure Analysis Server using the Power BI API .
prerequisite :-
1. Create a Live (Direct Query Mode) dataset in Power BI which connect to Azure Analysis server .
2. Create a Service Princple & Secret usering Azure App Resistration process .
3. Set Power BI Service API "Delegated" permission like Dataset.ReadWrite.All,Report.Read.All,Report.Readwrite.All  for this Service princple .

In databricks , you can  keep all the below details in key vault and read the secert directly from key vault .

tenant_id , client_id, client_secret, username, password

## Get the Access Token 
There are multiple way to get the access token 
 * Intereactive browser credential .
 * Client Credential
 * password along with client credential .

For Power BI Dataset having Direct Query only works with "password along with client credential", for this you need client_id,client_secret,tenant_id,username,password .
Please make sure username having access to read Azure Analysis server data .

  ```python
def get_powerbi_token(tenant_id , client_id, client_secret, username, password):
     import requests
     auth_url = 'https://login.microsoftonline.com/{0}/oauth2/token'.format(tenant_id)
     headers = {
     "Content-Type": "application/x-www-form-urlencoded"  
    }

    resource = "https://analysis.windows.net/powerbi/api"
    data = {
      'grant_type': 'password' ,
      'client_id': client_id,
      'client_secret': client_secret,
      'username': username,
      'password': password
   }

   auth_response = requests.post(auth_url, headers=headers, data=data)
   if auth_response.status_code == 200:
      return auth_response.json()["access_token"]
   else:
      raise Exception(f"faliure for access token, status_code:{auth_response.status_code},{auth_response.text} ")

```
## User Above Access Token @@access_token to read data from PowerBI DataSet connected to DirectQuery to Azure Analysis Server Model 

```python
import requests
api_url = 'https://api.powerbi.com/v1.0/myorg/datasets/{datasetId}/executeQueries' #please replace respective datasetID
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer {0}'.format(access_token)
}
dax_query = 'EVALUATE tableName'
post_dax = {
    'queries': [
        {
            'query': dax_query
        }
    ]
}

res = requests.post(api_url, headers=headers, json=post_dax)
rslt = res.json()["results"][0]["tables"][0]["rows"]
display(rslt)  #  display is databricks command to show in table format 
```

  All abpove steps will work seamlessly if there is no restriction related to Networking and no other permission issue .
  you may face some issues like MFA for username you are using and api call not wokring as expected
  so make sure you are using related proxies to allow the connection to be established . 


*****
  # DATABRICKS(python) Connect to Extract based PowerBI DataSet(powerbi_dax.py)
  
*****

  User context not required for extract based PowerBI DataSet , only client_credential will work with proper access granted .

 
 ```python
   def get_powerbi_token(tenant_id , client_id, client_secret):
     import requests
     auth_url = 'https://login.microsoftonline.com/{0}/oauth2/token'.format(tenant_id)
     headers = {
     "Content-Type": "application/x-www-form-urlencoded"  
    }

    resource = "https://analysis.windows.net/powerbi/api"
    data = {
      'grant_type': 'client_credentials',
      'client_id': client_id ,
      'client_secret': client_secret
   }

   auth_response = requests.post(auth_url, headers=headers, data=data)
   if auth_response.status_code == 200:
      return auth_response.json()["access_token"]
   else:
      raise Exception(f"faliure for access token, status_code:{auth_response.status_code},{auth_response.text} ")

```

## User Above Access Token @@access_token to read data from PowerBI DataSet 

```python
import requests
api_url = 'https://api.powerbi.com/v1.0/myorg/datasets/{datasetId}/executeQueries' #please replace respective datasetID
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer {0}'.format(access_token)
}
dax_query = 'EVALUATE tableName'
post_dax = {
    'queries': [
        {
            'query': dax_query
        }
    ]
}

res = requests.post(api_url, headers=headers, json=post_dax)
rslt = res.json()["results"][0]["tables"][0]["rows"]
display(rslt)  #  display is databricks command to show in table format 
```


  







