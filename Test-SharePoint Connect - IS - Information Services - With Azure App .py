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
    site_url = "https://graph.microsoft.com/v1.0/sites/lemo.sharepoint.com:/sites/LEGR-IS"  # Remplace {site-id} par l'ID de ton site SharePoint

    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get(site_url, headers=headers)

    # Affichage des informations du site SharePoint 
    print(response.status_code)
    print(response.json())
    
    # Affichage de l'ID du site SharePoint 
    print("\n\n",response.json().get("displayName")," => Site ID :" , response.json().get("id"))  # Site ID

    # Etape 2 : Afficher les bibliothèques de documents du site SharePoint
    site_id = response.json().get("id")

    libraries_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives"  # URL pour accéder aux bibliothèques de documents
    libraries_response = requests.get(libraries_url, headers=headers)

    print("\n\n",libraries_response.status_code)
    print(libraries_response.json())    

    # Affichage des bibliothèques de documents
    libraries = libraries_response.json().get("value", [])
    if libraries:
        print("\n\nBibliothèques de documents :")
        for library in libraries:
            print(f"- {library['name']} (ID: {library['id']})")
            #print("\n") 


    # Etape 3 : Afficher les fichiers d'une bibliothèque de documents
    library_id = libraries[0]['id'] if libraries else None  # Prendre la première bibliothèque de documents
    if library_id:
        files_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{library_id}/root/children"  # URL pour accéder aux fichiers
        files_response = requests.get(files_url, headers=headers)

        print("\n\n",files_response.status_code)
        print(files_response.json())    

        # Affichage des fichiers
        files = files_response.json().get("value", [])
        if files:
            print("\n\nFichiers :")
            for file in files:
                print(f"- {file['name']} (ID: {file['id']})")

else:
    print("Erreur d'authentification :", result.get("error_description"))    
