
def get_powerbi_token(tenant_id , client_id, client_secret):
   import requests
   auth_url = 'https://login.microsoftonline.com/{0}/oauth2/token'.format(tenant_id)
   headers = {
   "Content-Type": "application/x-www-form-urlencoded"  
  }

  resource = "https://analysis.windows.net/powerbi/api"
  data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret
 }

 auth_response = requests.post(auth_url, headers=headers, data=data)
 if auth_response.status_code == 200:
    return auth_response.json()["access_token"]
 else:
    raise Exception(f"faliure for access token, status_code:{auth_response.status_code},{auth_response.text} ")

access_token = get_powerbi_token(tenant_id , client_id, client_secret)

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
