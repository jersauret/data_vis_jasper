import pandas as pd

def merge_dataframes(ventes_df, locations_df):

    merged_df = pd.merge(ventes_df, locations_df, left_on='nom_commune', right_on='LIBGEO', how='inner')
    merged_df['price_per_sq_meter'] = merged_df['price_per_sq_meter'].astype(float)
    merged_df = calculate_rentability(merged_df)
    merged_df = classify_rentability(merged_df)
    return calculate_average_by_code_commune(merged_df)
def calculate_average_by_code_commune(merged_df):
    # Filter out non-numeric values in 'LIBGEO' column
    # Group by 'LIBGEO' and calculate the mean of 'price_per_sq_meter' for each group
    avg_price_per_sq_meter = merged_df.groupby('LIBGEO').agg({'rentability_group':'first', 'tx_rentabilite': 'mean','price_per_sq_meter': 'mean','loy_year': 'mean', 'code_postal': 'first', 'code_commune': 'first', 'longitude':'first', 'latitude': 'first'})

    # Reset index to convert the result to a DataFrame
    avg_price_per_sq_meter = avg_price_per_sq_meter.reset_index()

    return avg_price_per_sq_meter

def calculate_rentability(merged_df):
    merged_df['tx_rentabilite'] = merged_df['price_per_sq_meter'] / merged_df['loy_year']
    return merged_df

def classify_rentability(merged_df):
    # Calculate percentiles  chaque groupe représentera 25 % des données. 'Groupe 1' correspondra aux 25 % les plus bas des valeurs, 'Groupe 2' aux 25 % suivants, 'Groupe 3' aux 25 % suivants, et 'Groupe 4' aux 25 % les plus élevés. Vous pouvez ajuster les étiquettes et les quantiles selon vos besoins spécifiques.
    merged_df['rentability_group'] = pd.qcut(merged_df['tx_rentabilite'], q=[0, 0.25, 0.5, 0.75, 1], labels=['Group 1', 'Group 2', 'Group 3', 'Group 4'])

    return merged_df
