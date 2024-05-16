import pandas as pd

def process_ventes(ventes_file, ventes_delimiter, postal_codes_file):
    # Columns to retain from the ventes file
    columns_to_retain = ['nature_mutation',
                         'valeur_fonciere', 'adresse_numero', 'code_postal', 'code_commune',
                         'nom_commune', 'code_departement', 'type_local',
                         'surface_reelle_bati', 'nombre_pieces_principales', 'surface_terrain',
                         'longitude', 'latitude']

    # Read the ventes file with specified delimiter and only retain the specified columns
    ventes_df = pd.read_csv(ventes_file, delimiter=ventes_delimiter, encoding='utf-8',
                            usecols=columns_to_retain, low_memory=False)

    # Filter rows where nature_mutation is equal to 'Vente'
    ventes_df = ventes_df[ventes_df['nature_mutation'] == 'Vente']

    # Filter rows where type_local is equal to "Appartement"
    ventes_df = ventes_df[ventes_df['type_local'] == 'Appartement']

    # Read postal codes file
    postal_codes_df = pd.read_csv(postal_codes_file, delimiter=';', encoding='utf-8')

    # Get postal codes for Occitanie region
    occitanie_postal_codes = postal_codes_df[postal_codes_df['Nom Officiel Région'] == 'Occitanie']['Code_postal'].tolist()

    # Filter rows where code_postal is included in Occitanie postal codes
    ventes_df = ventes_df[ventes_df['code_postal'].isin(occitanie_postal_codes)]

    ventes_df['price_per_sq_meter'] = ventes_df['valeur_fonciere'] / ventes_df['surface_reelle_bati']
    ventes_df = ventes_df.drop_duplicates()
    # Group by code_commune and calculate average valeur_fonciere for each group
    avg_price_per_sq_meter = ventes_df.groupby('nom_commune')['price_per_sq_meter'].mean().reset_index()

    # Print or save the resulting DataFrame
    # print("Average valeur_fonciere grouped by code_commune:")
    # print(avg_price_per_sq_meter)
    return ventes_df[['code_postal', 'code_commune', 'nom_commune', 'code_departement', 'price_per_sq_meter', 'longitude', 'latitude']]