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


def list_all_files_recursive(access_token, drive_id, item_path=None, indent=0):
    headers = {"Authorization": f"Bearer {access_token}"}

    if item_path is None or item_path == "/":
        url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root/children"
    else:
        url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root:/{item_path}:/children"

    while url:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        for item in data.get("value", ['name']):
            prefix = "    " * indent
            #print(f"{prefix}- {item['name']} ({item['webUrl']})")
            print(f"{prefix}- {item['name']} ")

            if item.get("folder"):
                sub_path = f"{item_path}/{item['name']}" if item_path else item['name']
                list_all_files_recursive(access_token, drive_id, sub_path, indent + 1)

        url = data.get("@odata.nextLink")  # ⬅️ pagination ici


def get_file_versions_count(access_token, drive_id, item_id):
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{item_id}/versions"

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    versions = response.json().get("value", [])

    return len(versions)



def collect_all_files_with_versions(access_token, drive_id, item_path=None, results=None):
    if results is None:
        results = []

    headers = {"Authorization": f"Bearer {access_token}"}

    if item_path is None or item_path == "/":
        url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root/children"
    else:
        url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root:/{item_path}:/children"

    while url:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        for item in data.get("value", []):
            is_folder = item.get("folder") is not None
            file_info = {
                "name": item["name"],
                "url": item["webUrl"],
                "path": item_path or "/",
                "type": "folder" if is_folder else "file",
                "versions": None
            }

            if not is_folder:
                # 🧮 Récupérer le nombre de versions
                file_info["versions"] = get_file_versions_count(access_token, drive_id, item["id"])
                if file_info["versions"] > 0:
                    print(f"  - {file_info['name']} - Versions : {file_info['versions']}")
                

            results.append(file_info)

            if is_folder:
                sub_path = f"{item_path}/{item['name']}" if item_path else item['name']
                collect_all_files_with_versions(access_token, drive_id, sub_path, results)

        url = data.get("@odata.nextLink")

    return results





# ---------- MAIN ----------
if __name__ == "__main__":
    token = get_token()

    if token:
        site_path = "lemo.sharepoint.com:/sites/LEGR-IS/"
        site_id = get_site_id(token, site_path)
        libraries = list_libraries(token, site_id)

        print("\n📚 Bibliothèques disponibles :")
        for lib in libraries:
            print(f"- {lib['name']} (id: {lib['id']})")

            print("  Contenu :")
            files = list_files_in_library(token, lib["id"])
            # Exemple d'affichage des fichiers dans la bibliothèque (mais pas récursif)
            #for f in files:
            #    print(f"    • {f['name']} - {f['webUrl']}")
            print("  📁 Contenu complet de la bibliothèque :")
            #list_all_files_recursive(token, lib["id"])

            collect_all_files_with_versions(token, lib["id"])
            print("  📁 Contenu complet de la bibliothèque avec versions :")    
            results = collect_all_files_with_versions(token, lib["id"])
            for item in results:
                if item["versions"] is not None:
                    print(f"    • {item['name']} - {item['url']} - Versions : {item['versions']}")
                else:
                    print(f"    • {item['name']} - {item['url']}")

        


    else:
        print("❌ Échec de l'authentification.")
