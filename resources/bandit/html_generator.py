from jinja2 import Environment, FileSystemLoader
import pandas as pd
#from .parser import parse_json, load_and_parse
from graphics_generator import generate_all_plots  # Import the new function

#FUNCTIONS#
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


# Parse JSON data to create df
df = load_and_parse('./reports/bandit-results.json')

# Generate plots
generate_all_plots()  # Call the new function

# Set up the environment for Jinja2
env = Environment(loader=FileSystemLoader('./'))

# Load the HTML template
template = env.get_template('./bandit/report_template.html')

print("Rendering template...")
html_content = template.render(
    data=df,
    severity_plot='./images/severity_counts.png',
    file_plot='./images/file_counts.png'
)

print("Writing HTML content to file...")
with open('./bandit/report.html', 'w') as f:
    f.write(html_content)

print("Finished writing file.")