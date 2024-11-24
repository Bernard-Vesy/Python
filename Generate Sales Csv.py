import csv
import random
from faker import Faker
import pandas as pd
import numpy as np

# Charger le fichier clients existant
clients_file_path = 'C:/Users/berna/GitHub/Python/Generate Clients CSV/clients.csv'
clients_df = pd.read_csv(clients_file_path)

# Générer un fichier CSV avec 100 000 lignes de ventes aléatoires sur 10 000 produits différents
def generate_sales_csv_optimized(clients_df, filename, num_rows=100000, num_products=10000):
    fake = Faker()
    products = [f"Produit_{i}" for i in range(1, num_products + 1)]
    
    # Préparer des données aléatoires en utilisant numpy pour améliorer les performances
    client_ids = np.random.choice(clients_df['ID'].values, num_rows)
    produits = np.random.choice(products, num_rows)
    quantites = np.random.randint(1, 11, num_rows)
    prix_unitaires = np.round(np.random.uniform(10, 1000, num_rows), 2)
    dates_ventes = [fake.date_between(start_date='-1y', end_date='today') for _ in range(num_rows)]
    
    # Créer un DataFrame avec les données générées
    sales_data = {
        'Vente_ID': np.arange(1, num_rows + 1),
        'Client_ID': client_ids,
        'Produit': produits,
        'Quantité': quantites,
        'Prix_Unitaire': prix_unitaires,
        'Date_Vente': dates_ventes
    }
    sales_df = pd.DataFrame(sales_data)
    
    # Sauvegarder le DataFrame dans un fichier CSV
    sales_df.to_csv(filename, index=False, encoding='utf-8-sig')

# Générer le fichier sales.csv
sales_file_path = 'C:/Users/berna/GitHub/Python/Generate Clients CSV/Sales.csv'
generate_sales_csv_optimized(clients_df, sales_file_path)
print("Fichier 'sales.csv' généré avec succès.")