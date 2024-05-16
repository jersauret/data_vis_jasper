import pandas as pd

def process_locations(locations_file, locations_delimiter):
    # Columns to retain from the locations file
    columns_to_retain = ['id_zone', 'INSEE', 'LIBGEO', 'DEP', 'REG', 'loypredm2']

    # Read the locations file with specified delimiter
    locations_df = pd.read_csv(locations_file, delimiter=locations_delimiter, encoding='latin1',
                               usecols=columns_to_retain)

    # Filter rows where REG is equal to 76
    locations_df = locations_df[locations_df['REG'] == 76]
    locations_df['loypredm2'] = locations_df['loypredm2'].str.replace(',', '.')

    locations_df['loypredm2'] = pd.to_numeric(locations_df['loypredm2'], errors='coerce')

    # Calculate 'loy_year' by multiplying 'loypredm2' by 12
    locations_df['loy_year'] = locations_df['loypredm2'] * 12
    locations_df = locations_df.drop_duplicates()
    # Print column names
    #print("Column Names in locations file:")
    #print(locations_df.columns)

    # Print first few rows of the DataFrame
    #print("First few rows of the locations DataFrame:")
    #print(locations_df.head())

    # Write to CSV
    locations_df.to_csv("processed_locations.csv", index=False, sep=locations_delimiter)

    # Return the modified DataFrame
    return locations_df[['id_zone', 'INSEE', 'LIBGEO', 'loy_year']]