import pandas as pd

original_data = pd.read_csv('../data/Milwaukee_county_records - milwaukee_county_records.csv - actual drug deaths.csv')
raven_compliant = pd.read_csv('../data/Target-MDI-To-EDRS-Template.csv')


# Some mappings of Milwaukee column name : raven csv column name
# To be completed with all the Milwaukee columns
COLMAP = {
    'CaseIdentifier': 'BASEFHIRID',
    'CaseNum': 'MDICASEID',
    'Age': 'AGE',
    'Race': 'RACE',
    'Sex': 'GENDER',
    'Mode': 'MANNER',
    'CauseA': 'CAUSEA',
    'CauseB': 'CAUSEB',
}

# This is just a summary of how we can do this
# We map the correct columns from the original data to the raven compliant csv
# When we finish the mapping in COLMAP, we can just iterate over the COLMAP and map the columns
raven_compliant['BASEFHIRID'] = original_data['CaseIdentifier']
print(raven_compliant.head())
