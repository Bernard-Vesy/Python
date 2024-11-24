import csv
import random
from faker import Faker

# Créer une instance de Faker
#fake = Faker()
fake_fr_ch = Faker('fr_CH')
fake_de_ch = Faker('de_CH')
fake_it_ch = Faker('it_CH')

# Créer un fichier CSV avec 20 000 lignes
def generate_clients_csv(filename, num_rows=20000):
    with open(filename, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        # Écrire l'en-tête du CSV
        writer.writerow(['ID', 'Prénom', 'Nom', 'Email', 'Téléphone', 'Adresse', 'Ville', 'Pays'])
        
        # Générer des lignes de clients
        for i in range(1, num_rows + 1):
            # Déterminer la région en fonction des pourcentages
            region = random.choices(['fr', 'de', 'it'], weights=[30, 60, 10], k=1)[0]
            if region == 'fr':
                fake_locale = fake_fr_ch
            elif region == 'de':
                fake_locale = fake_de_ch
            else:
                fake_locale = fake_it_ch
            prenom = fake_locale.first_name()
            nom = fake_locale.last_name()
            email = fake_locale.email()
            telephone = fake_locale.phone_number()
            adresse = fake_locale.street_address()
            ville = fake_locale.city()
            pays = 'Switzerland'
            
            # Écrire la ligne dans le fichier CSV
            writer.writerow([i, prenom, nom, email, telephone, adresse, ville, pays])

# Générer le fichier clients.csv
generate_clients_csv('C:/Users/berna/GitHub/Python/Generate Clients CSV/clients.csv')
print("Fichier 'clients.csv' généré avec succès.")
