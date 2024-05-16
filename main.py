import pandas as pd
from process_ventes import process_ventes
from process_locations import process_locations
from merge_dataframes import merge_dataframes

if __name__ == "__main__":
    ventes_file = "rawfiles/old/ventes.csv"
    locations_file = "rawfiles/old/loyers_2020.csv"
    postal_codes_file = "rawfiles/codes_postaux/base-officielle-des-codes-postaux-en-occitanie.csv"  # Path to the CSV file containing all postal codes
    ventes_delimiter = ','  # Change to the delimiter used in the ventes file
    locations_delimiter = ';'  # Change to the delimiter used in the locations file

    # Process ventes data
    ventes_df = process_ventes(ventes_file, ventes_delimiter, postal_codes_file)

    # Process locations data
    locations_df = process_locations(locations_file, locations_delimiter)

    # Merge the dataframes
    merged_df = merge_dataframes(ventes_df, locations_df)
    merged_df.to_csv("processed_renta_data.csv", index=False, sep=locations_delimiter)

    # Print or save the merged dataframe
    print("Merged DataFrame:")
    print(merged_df)
