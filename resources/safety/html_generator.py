
import argparse
import json
import os
import base64
from jinja2 import Environment, FileSystemLoader
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

def parse_safety_json(data):
    return pd.DataFrame(data['vulnerabilities'])

def load_and_parse(file_path):
    with open(file_path) as f:
        data = json.load(f)
    df = parse_safety_json(data)
    return df, data

def generate_total_packages_pie_plot(data):
    total_packages = len(data['scanned_packages'])
    affected_packages = len(data['affected_packages'])
    safe_packages = total_packages - affected_packages
    labels = ['Affected Packages', 'Safe Packages']
    sizes = [affected_packages, safe_packages]
    plt.figure(figsize=(12, 8))
    colors = ['#F57C00', '#66BB6A']
    plt.pie(sizes, labels=labels, autopct='%1.0f%%', startangle=140, colors=colors)
    plt.title('Vulnerable vs. Safe Packages', fontsize=15)
    plt.tight_layout()
    plt.gca().xaxis.set_major_formatter(plt.NullFormatter())
    plt.savefig(os.path.join(images_path, 'total_packages_pie.png'), dpi=300)

def generate_vulnerable_vs_safe_pie_plot(df):
    vulnerabilities = len(df)
    safe = len(df[df['advisory'] == 'No known vulnerabilities'])
    labels = ['Vulnerable', 'Safe']
    sizes = [vulnerabilities, safe]
    plt.figure(figsize=(12, 8))
    colors = ['#FF9999', '#66B2FF']
    plt.pie(sizes, labels=labels, autopct='%1.0f%%', startangle=140, colors=colors)
    plt.title('Vulnerable vs. Safe Packages', fontsize=15)
    plt.tight_layout()
    plt.gca().xaxis.set_major_formatter(plt.NullFormatter())
    plt.savefig(os.path.join(images_path, 'vulnerable_vs_safe_pie.png'), dpi=300)

def generate_vulnerabilities_per_package_plot(df):
    vulnerability_counts = df['package_name'].value_counts()
    plt.figure(figsize=(12, 8))
    colors = sns.color_palette('Set3', len(vulnerability_counts))
    patches, texts, autotexts = plt.pie(vulnerability_counts, labels=vulnerability_counts.index, autopct=lambda p: '{:.0f}'.format(p * sum(vulnerability_counts) / 100), startangle=140, colors=colors)
    for text in texts:
        text.set(color='black')
    for autotext in autotexts:
        autotext.set(color='black', weight='bold')
    plt.title('Number of Vulnerabilities per Affected Package', fontsize=15)
    plt.tight_layout()
    plt.gca().xaxis.set_major_formatter(plt.NullFormatter())
    plt.savefig(os.path.join(images_path, 'vulnerabilities_per_package_pie.png'), dpi=300)

def generate_all_plots_for_safety(file_path):
    df, data = load_and_parse(file_path)
    generate_total_packages_pie_plot(data)
    generate_vulnerable_vs_safe_pie_plot(df)
    generate_vulnerabilities_per_package_plot(df)

# Generate the plots
generate_all_plots_for_safety(file_path)

# Convert the images to data URLs
total_packages_pie_data_url = get_image_as_data_url(os.path.join(images_path, 'total_packages_pie.png'))
vulnerable_vs_safe_pie_data_url = get_image_as_data_url(os.path.join(images_path, 'vulnerable_vs_safe_pie.png'))
vulnerabilities_per_package_pie_data_url = get_image_as_data_url(os.path.join(images_path, 'vulnerabilities_per_package_pie.png'))

env = Environment(loader=FileSystemLoader('./'))
template = env.get_template(template_path)

print("Rendering template...")
html_content = template.render(
    data=df,
    total_packages_pie=total_packages_pie_data_url,
    vulnerable_vs_safe_pie=vulnerable_vs_safe_pie_data_url,
    vulnerabilities_per_package_pie=vulnerabilities_per_package_pie_data_url
)

print("Writing HTML content to file...")
with open('./safety/safety-report.html', 'w') as f:
    f.write(html_content)

print("Finished writing file.")
