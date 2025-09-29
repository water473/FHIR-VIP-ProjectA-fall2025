import pandas as pd
from datetime import date
import os


# Source files
original_file_loc = '../data/Milwaukee_county_records - milwaukee_county_records.csv - actual drug deaths.csv'
raven_template_loc = '../data/Target-MDI-To-EDRS-Template.csv'

# Resulting csv output file
file_runtime = date.today().strftime("%Y-%m-%d")
output_file = f'MILWAUKEE_TO_RAVEN_{file_runtime}.csv'
output_path = '../results/'

# Duplicate Dict Keys? CDEATHTIME and CDEATHDATE. Removed dups for now JST 9-29-25
RAVEN_MAP = {
    "BASEFHIRID": "CaseIdentifier",
    "SYSTEMID": None,
    "MDICASEID": "CaseNum",
    "EDRSCASEID": None,
    "FIRSTNAME": None,
    "MIDNAME": None,
    "LASTNAME": None,
    "AGE": "Age",
    "AGEUNIT": None,
    "RACE": "Race",
    "GENDER": "Sex",
    "ETHNICITY": None,
    "BIRTHDATE": None,
    "MRNNUMBER": None,
    "JOBTITLE": None,
    "INDUSTRY": None,
    "LANGUAGE": None,
    "MARITAL": None,
    "POSSIBLEID": None,
    "CAUSEA": "CauseA",
    "CAUSEB": "CauseB",
    "CAUSEC": "CauseOther",
    "CAUSED": None,
    "OSCOND": None,
    "MANNER": "Mode",
    "DISPMETHOD": None,
    "CHOWNINJURY": None,
    "DURATIONA": None,
    "DURATIONB": None,
    "DURATIONC": None,
    "DURACTIOND": None,
    "CASENOTES": None,
    "ATWORK": None,
    "JOBRELATED": None,
    "REPORTDATE": None,
    "REPORTTIME": None,
    "FOUNDDATE": None,
    "FOUNDTIME": None,
    "CDEATHDATE": "DeathDate",
    "EVENTDATE": "EventDate",
    "EVENTTIME": None,
    "PRNDATE": None,
    "PRNTIME": None,
    "EXAMDATE": None,
    "CINJDATE": None,
    "CINJTIME": None,
    "CINJDATEEARLY": None,
    "CINJDATELATE": None,
    "CDEATHESTABLISHEMENTMETHOD": None,
    "CIDATEFLAG": None,
    "CDEATHFLAG": None,
    "CDEATHTIME": None,
    "LKADATE": None,
    "LKATIME": None,
    "CASEYEAR": "death_year",
    "ATHOSPDATE": None,
    "ATHOSPTIME": None,
    "RESSTRET": None,
    "RESCITY": "DeathCity",
    "RESCOUNTY": None,
    "RESSTATE": "DeathState",
    "RESZIP": "DeathZip",
    "RESCOUNTRY": None,
    "DEATHLOCATION": "DeathAddr",
    "DEATHLOCATIONTYPE": None,
    "INJURYLOCATION": None,
    "FOUNDADDR_STREET": None,
    "FOUNDADDR_CITY": None,
    "FOUNDADDR_COUNTY": None,
    "FOUNDADDR_STATE": None,
    "FOUNDADDR_ZIP": None,
    "EVENTPLACE": None,
    "EVEENTADDR_STREET": None,
    "EVENTADDR_CITY": None,
    "EVENTADDR_COUNTY": None,
    "EVENT_ADDR_STATE": None,
    "EVENTADDR_ZIP": None,
    "PRNPLACE": None,
    "PRNSTREET": None,
    "PRNCITY": None,
    "PRNCOUNTY": None,
    "PRNSTATE": None,
    "PRNZIP": None,
    "DISP_PLACE": None,
    "DISP_STREET": None,
    "DISP_CITY": None,
    "DISP_STATE": None,
    "DISP_ZIP": None,
    "CINJPLACE": None,
    "CINJSTREET": None,
    "CINJCITY": None,
    "CINJCOUNTY": None,
    "CINJSTATE": None,
    "CINJZIP": None,
    "RESNAME": None,
    "LKAWHERE": None,
    "HOSPNAME": None,
    "SCENEADDR_STREET": None,
    "SCENEADDR_CITY": None,
    "SCENEADDR_COUNTY": None,
    "SCENEADDR_STATE": None,
    "SCENEADDR_ZIP": None,
    "CERTIFIER_NAME": None,
    "CERTIFIER_TYPE": None,
    "SURGERY": None,
    "SURGDATE": None,
    "SURGREASON": None,
    "HCPROVIDER": None,
    "AUTOPSYPERFORMED": None,
    "AUTOPSYRESULTSAVAILABLE": None,
    "AUTOPSY_OFFICENAME": None,
    "AUTOPSY_STREET": None,
    "AUTOPSY_CITY": None,
    "AUTOPSY_COUNTY": None,
    "AUTOPSY_STATE": None,
    "AUTOPSY_ZIP": None,
    "CUSTODY": None,
    "PREGNANT": None,
    "TOBACCO": None,
    "CAUTOPSY": None,
    "TRANSPORTATION": None,
    "MENAME": None,
    "MEPHONE": None,
    "MELICENSE": None,
    "ME_STREET": None,
    "ME_CITY": None,
    "ME_COUNTY": None,
    "ME_STATE": None,
    "ME_ZIP": None,
    "AUTOPUSED": None,
    "PRONOUNCERNAME": None,
    "CERTIFIER_IDENTIFIER": None,
    "CERTIFIER_IDENTIFIER_SYSTEM": None
}


# Method to transform CSV file into Raven MDI format based on specified mapping
def format_csv_to_raven(csv_file, raven_file, mapping, output_loc):

    # Convert to pandas dataframes
    source_df = pd.read_csv(csv_file)
    raven_df = pd.read_csv(raven_file)

    # Map columns
    for target_col in raven_df.columns:
        source_col = mapping.get(target_col)
        if source_col and source_col in source_df.columns:
            raven_df[target_col] = source_df[source_col]
        else:
            raven_df[target_col] = None

    # Export as csv
    raven_df.to_csv(output_loc, index=False)


# ********* Main Driver *****************
try:
    os.makedirs(output_path, exist_ok=True)
    format_csv_to_raven(original_file_loc, raven_template_loc, RAVEN_MAP, f'{output_path}{output_file}')
    print(f'File Created: {output_file}')
except Exception as e:
    print(f'File Creation Error: {e}')
