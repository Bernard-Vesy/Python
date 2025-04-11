import os
from dotenv import load_dotenv

from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.client_credential import ClientCredential

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
tenant_id = os.getenv("TENANT_ID")


print(f"CLIENT_ID     : {client_id}")
print(f"CLIENT_SECRET : {client_secret}")
print(f"TENANT_ID     : {tenant_id}")

# URL du site SharePoint et de la liste
SHAREPOINT_SITE_URL = "https://lemo.sharepoint.com/sites/LEGR-IS"
LIST_NAME = "DAM - Activities"

# Connexion au site SharePoint
ctx = ClientContext(SHAREPOINT_SITE_URL).with_credentials(ClientCredential(client_id, client_secret))

# Récupérer la liste
target_list = ctx.web.lists.get_by_title(LIST_NAME)

# Récupérer les éléments de la liste
# On error Record the application (SharepointDAM on the site) // https://lemo.sharepoint.com/sites/LEGR-IS/_layouts/15/appinv.aspx
items = target_list.items.get().execute_query() 

# Afficher les valeurs du champ "Titre"
for item in items:
    print(item.properties["Title"], item.properties["FileName"])