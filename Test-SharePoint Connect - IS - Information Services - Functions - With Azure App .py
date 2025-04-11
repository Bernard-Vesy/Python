import msal
import requests

# ---------- CONFIG ----------
import os
from dotenv import load_dotenv
load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")  # Remplace avec ton Client ID
TENANT_ID = os.getenv("TENANT_ID")  # Ou ton tenant spécifique
CLIENT_SECRET = os.getenv("CLIENT_SECRET")  # Remplace avec ton Client Secret


AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]
GRAPH_BASE = "https://graph.microsoft.com/v1.0"

# ---------- AUTH ----------
def get_token():
    app = msal.ConfidentialClientApplication(
        client_id=CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET
    )
    result = app.acquire_token_for_client(scopes=SCOPES)
    return result.get("access_token")

# ---------- API CALLS ----------
def get_site_id(access_token, site_path):
    url = f"{GRAPH_BASE}/sites/{site_path}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["id"]

def list_libraries(access_token, site_id):
    url = f"{GRAPH_BASE}/sites/{site_id}/drives"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["value"]

def list_files_in_library(access_token, drive_id):
    url = f"{GRAPH_BASE}/drives/{drive_id}/root/children"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["value"]


# ---------- MAIN ----------
if __name__ == "__main__":
    token = get_token()

    if token:
        site_path = "lemo.sharepoint.com:/sites/LEGR-IS"
        site_id = get_site_id(token, site_path)
        libraries = list_libraries(token, site_id)

        print("\n📚 Bibliothèques disponibles :")
        for lib in libraries:
            print(f"- {lib['name']} (id: {lib['id']})")

            print("  Contenu :")
            files = list_files_in_library(token, lib["id"])
            for f in files:
                print(f"    • {f['name']} - {f['webUrl']}")
    else:
        print("❌ Échec de l'authentification.")
