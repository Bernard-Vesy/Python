# Variable d'environnement : CLIENT_ID, TENANT_ID, AUTHORITY, SCOPES
import os
from dotenv import load_dotenv

import msal
import requests
from office365.sharepoint.client_context import ClientContext
import msal # Importer la bibliothèque MSAL pour l'authentification Azure AD (Microsoft Authentication Library)

# Paramètres Azure AD
CLIENT_ID = os.getenv("CLIENT_ID")  # Remplace avec ton Client ID
TENANT_ID = os.getenv("TENANT_ID")  # Ou ton tenant spécifique
CLIENT_SECRET = os.getenv("CLIENT_SECRET")  # Remplace avec ton Client Secret

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]  # Accès à Microsoft Graph

app = msal.ConfidentialClientApplication(
    CLIENT_ID,
    authority=AUTHORITY,
    client_credential=CLIENT_SECRET
)

result = app.acquire_token_for_client(scopes=SCOPES)

if "access_token" in result:
    print("Authentification réussie !")
    access_token = result["access_token"]

    
        # Exemple : accès à un site SharePoint
    site_url = "https://graph.microsoft.com/v1.0/sites/root"

    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get(site_url, headers=headers)

    print(response.status_code)
    print(response.json())

else:
    print("Erreur d'authentification :", result.get("error_description"))    
