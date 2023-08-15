
import argparse
import json
import os
import base64
from jinja2 import Environment, FileSystemLoader
import pandas as pd
import matplotlib.pyplot as plt

# Argument parsing
parser = argparse.ArgumentParser(description='Process the JSON file and HTML template.')
parser.add_argument('file_path', type=str, help='Path to the JSON file')
parser.add_argument('template_path', type=str, help='Path to the HTML template file')
args = parser.parse_args()
file_path = args.file_path
template_path = args.template_path

# Define the path for images
images_path = './safety/images/'
os.makedirs(images_path, exist_ok=True)  # Create the directory if it doesn't exist

def get_image_as_data_url(image_path):
    with open(image_path, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()
    return f"data:image/png;base64,{encoded_image}"

# Functions to parse the safety JSON data and convert it into a pandas DataFrame
def parse_safety_json(data):
    records = []
    for item in data:
        package, affected, installed, advisory, cve, advisory_url = item
        records.append({
            'package_name': package,
            'affected_version': affected,
            'installed_version': installed,
            'advisory': advisory,
            'cve': cve,
            'advisory_url': advisory_url
        })
    df = pd.DataFrame(records)
    return df

def load_and_parse(file_path):
    with open(file_path) as f:
        data = json.load(f)
    df = parse_safety_json(data)
    total_packages = len(df)
    affected_packages = len(df[df['advisory'] != "No known vulnerabilities"])
    safe_packages = total_packages - affected_packages
    safety_data = {
        'total_packages': total_packages,
        'affected_packages': affected_packages,
        'safe_packages': safe_packages
    }
    return df, safety_data

# Functions to generate plots
def generate_vulnerable_vs_safe_pie_plot(df):
    total = len(df)
    vulnerable = len(df[df['advisory'] != "No known vulnerabilities"])
    safe = total - vulnerable
    labels = ['Vulnerable Packages', 'Safe Packages']
    sizes = [vulnerable, safe]
    colors = ['#f44336', '#4CAF50']
    plt.figure(figsize=(10, 6))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title("Vulnerable vs Safe Packages")
    plt.tight_layout()
    plt.savefig(os.path.join(images_path, 'vulnerable_vs_safe_pie.png'), dpi=300)

def generate_all_packages_pie_plot(df):
    labels = df['package_name'].values
    sizes = [1] * len(df)  # Since we want to represent each package equally
    plt.figure(figsize=(10, 6))
    plt.pie(sizes, labels=labels, startangle=90, colors=plt.cm.Paired.colors)
    plt.axis('equal')
    plt.title("All Analyzed Packages")
    plt.tight_layout()
    plt.savefig(os.path.join(images_path, 'all_packages_pie.png'), dpi=300)

def generate_vulnerabilities_per_package_pie_plot(df):
    vulnerable_df = df[df['advisory'] != "No known vulnerabilities"]
    counts = vulnerable_df['package_name'].value_counts()
    labels = counts.index
    sizes = counts.values
    plt.figure(figsize=(10, 6))
    plt.pie(sizes, labels=labels, startangle=90, autopct='%1.1f%%', colors=plt.cm.tab20c.colors)
    plt.axis('equal')
    plt.title("Number of Vulnerabilities per Affected Package")
    plt.tight_layout()
    plt.savefig(os.path.join(images_path, 'vulnerabilities_per_package_pie.png'), dpi=300)

def generate_all_plots_for_safety(file_path):
    df, safety_data = load_and_parse(file_path)
    generate_vulnerable_vs_safe_pie_plot(df)
    generate_all_packages_pie_plot(df)
    generate_vulnerabilities_per_package_pie_plot(df)

# Main Execution
generate_all_plots_for_safety(file_path)

# Convert the images to data URLs
vulnerable_vs_safe_pie_data_url = get_image_as_data_url(os.path.join(images_path, 'vulnerable_vs_safe_pie.png'))
all_packages_pie_data_url = get_image_as_data_url(os.path.join(images_path, 'all_packages_pie.png'))
vulnerabilities_per_package_pie_data_url = get_image_as_data_url(os.path.join(images_path, 'vulnerabilities_per_package_pie.png'))

env = Environment(loader=FileSystemLoader('./'))
template = env.get_template(template_path)

df, safety_data = load_and_parse(file_path)

print("Rendering template...")
html_content = template.render(
    data=df,
    total_packages_pie=all_packages_pie_data_url,
    all_packages_pie=all_packages_pie_data_url,
    vulnerabilities_per_package_pie=vulnerabilities_per_package_pie_data_url
)

print("Writing HTML content to file...")
with open('./safety/safety-report.html', 'w') as f:
    f.write(html_content)

print("Finished writing file.")
