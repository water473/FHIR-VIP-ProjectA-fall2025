import json
import pandas as pd
from datetime import datetime

def convert_record_to_fhir(record):
    death_date = record.get("DeathDate")
    deceased_datetime = None

    if isinstance(death_date, (int, float)) and death_date > 0:
        try:
            deceased_datetime = datetime.utcfromtimestamp(death_date / 1000).isoformat()
        except (OSError, ValueError):
            deceased_datetime = None
    elif isinstance(death_date, str) and death_date.strip():
        try:
            deceased_datetime = datetime.strptime(death_date, "%Y-%m-%d %H:%M:%S").isoformat()
        except ValueError:
            try:
                deceased_datetime = datetime.strptime(death_date, "%m/%d/%Y %H:%M").isoformat()
            except ValueError:
                deceased_datetime = None

    gender = record.get("Gender") or record.get("Sex")
    if isinstance(gender, str):
        if gender not in ['male', 'female']:
            if gender == 'm':
                gender = 'male'
            elif gender == 'f':
                gender = 'female'
            else:
                gender = 'other'
    else:
        gender = "unknown"

    postal_code = str(int(record["DeathZip"])) if isinstance(record.get("DeathZip"), (int, float)) else record.get("DeathZip")

    patient_id = f"pat-{record['CaseIdentifier']}"
    observation_id = f"obs-{record['CaseIdentifier']}"

    patient = {
        "resourceType": "Patient",
        "id": patient_id,
        "identifier": [{"value": record["CaseNum"]}],
        "gender": gender,
        "birthDate": (
            f"{datetime.fromisoformat(deceased_datetime).year - int(record['Age'].split()[0])}-01-01"
            if deceased_datetime and isinstance(record.get("Age"), str) and "Years" in record["Age"] else None
        ),
        "deceasedDateTime": deceased_datetime,
        "address": [{
            "line": [record["DeathAddr"]] if record.get("DeathAddr") else None,
            "city": record["DeathCity"] if record.get("DeathCity") else None,
            "postalCode": postal_code,
            "state": record["DeathState"] if record.get("DeathState") else None
        }]
    }

    death_observation = {
        "resourceType": "Observation",
        "id": observation_id,
        "status": "final",
        "code": {"text": "Death Record"},
        "subject": {"reference": f"Patient/{patient_id}"},
        "effectiveDateTime": deceased_datetime,
        "valueString": record.get("Mode", "Unknown")
    }

    return [
        {
            "resource": patient,
            "request": {
                "method": "PUT",
                "url": f"Patient/{patient_id}"
            }
        },
        {
            "resource": death_observation,
            "request": {
                "method": "PUT",
                "url": f"Observation/{observation_id}"
            }
        }
    ]


def convert_to_fhir(file_path, filter_drug_related=True):
    fhir_bundle = {
        "resourceType": "Bundle",
        "type": "transaction",
        "entry": []
    }

    if file_path.endswith(".jsonl"):
        with open(file_path, "r") as f:
            for line in f:
                record = json.loads(line)
                if not filter_drug_related or record.get("DeathType") == "Drug Related":
                    fhir_bundle["entry"].extend(convert_record_to_fhir(record))

    elif file_path.endswith(".csv"):
        df = pd.read_csv(file_path, low_memory=False)
        df.fillna("", inplace=True)

        if filter_drug_related:
            df = df[df["DeathType"] == "Drug Related"]

        for _, row in df.iterrows():
            record = row.to_dict()
            fhir_bundle["entry"].extend(convert_record_to_fhir(record))

    return fhir_bundle


# JSON
file_path = "./input/JSON/milwaukee_county_records.jsonl"
output_path = "./output/FilteredFromJSON.json"

fhir_data = convert_to_fhir(file_path, filter_drug_related=True)

with open(output_path, "w") as f:
    json.dump(fhir_data, f, indent=4)

# CSV
file_path = "./input/CSV/milwaukee_county_records.csv"
output_path = "./output/FilteredFromCSV.json"

fhir_data = convert_to_fhir(file_path, filter_drug_related=True)

with open(output_path, "w") as f:
    json.dump(fhir_data, f, indent=4)
