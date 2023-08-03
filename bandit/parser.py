import json
import pandas as pd

def parse_json(data):
    # Convert to DataFrame
    df = pd.json_normalize(data['results'], 
                           meta=['filename'], errors='ignore')

    return df

def load_and_parse(file_path):
    # Load JSON data
    with open(file_path) as f:
        data = json.load(f)

    # Parse data into DataFrame
    df = parse_json(data)
    #print(df.head())
    return df

load_and_parse('./reports/bandit-results.json')