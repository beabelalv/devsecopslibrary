
import argparse
import json
import os
import base64
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from jinja2 import Environment, FileSystemLoader

# Argument parsing
parser = argparse.ArgumentParser(description='Process the Safety JSON file and HTML template.')
parser.add_argument('file_path', type=str, help='Path to the Safety JSON file')
parser.add_argument('template_path', type=str, help='Path to the Safety HTML template file')
args = parser.parse_args()
file_path = args.file_path
template_path = args.template_path

# Define the path for images
images_path = './safety/images/'
os.makedirs(images_path, exist_ok=True)

# Function to convert image to data URL
def get_image_as_data_url(image_path):
    with open(image_path, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()
    return f"data:image/png;base64,{encoded_image}"

# Functions for Safety report generation
def parse_safety_json_adjusted(data):
    results = []
    for item in data['issues']:
        results.append(item)
    return pd.DataFrame(results)

def load_and_parse_adjusted(file_path):
    with open(file_path) as f:
        data = json.load(f)
    df = parse_safety_json(data)
    return df, data

def generate_vulnerability_pie_plot(df):
    vulnerability_counts = df['package_name'].value_counts()
    plt.figure(figsize=(12, 8))
    plt.pie(vulnerability_counts, labels=vulnerability_counts.index, autopct='%1.0f%%', startangle=140, colors=sns.color_palette('Set3', len(vulnerability_counts)))
    plt.title('Number of Vulnerabilities per Affected Package', fontsize=15)
    plt.tight_layout()
    plt.gca().xaxis.set_major_formatter(plt.NullFormatter())
    plt.savefig(os.path.join(images_path, 'package_vulnerability_pie.png'), dpi=300)

def generate_all_plots(file_path):
    df, _ = load_and_parse(file_path)
    generate_vulnerability_pie_plot(df)

# Main
df_safety, safety_data = load_and_parse(file_path)
generate_all_plots(file_path)

# Convert the images to data URLs
vulnerability_pie_data_url = get_image_as_data_url(os.path.join(images_path, 'package_vulnerability_pie.png'))

env = Environment(loader=FileSystemLoader('./'))
template = env.get_template(template_path)

print("Rendering template...")
html_content = template.render(
    data=df_safety,
    safety_data=safety_data,
    vulnerability_pie=vulnerability_pie_data_url
)

print("Writing HTML content to file...")
with open('./safety/safety-report.html', 'w') as f:
    f.write(html_content)

print("Finished writing file.")
