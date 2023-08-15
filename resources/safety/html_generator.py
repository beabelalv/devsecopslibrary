
import argparse
import json
import os
import base64
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from jinja2 import Environment, FileSystemLoader

# Argument parsing
parser = argparse.ArgumentParser(description='Process the JSON file and HTML template for Safety.')
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

def load_and_parse_safety(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    return df

def generate_analyzed_packages_pie(df):
    package_counts = df['package_name'].value_counts()
    colors = sns.color_palette("pastel", len(package_counts))
    plt.figure(figsize=(14, 10))
    wedges, texts, autotexts = plt.pie(package_counts.values, labels=package_counts.index, autopct='%1.1f%%', startangle=140, colors=colors, wedgeprops=dict(width=0.3, edgecolor='w'), pctdistance=0.85, textprops=dict(color="black"))
    for text, autotext in zip(texts, autotexts):
        text.set(size=15)
        autotext.set(size=15)
        autotext.set_color('black')
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    plt.title('Distribution of Analyzed Packages', fontsize=24)
    plt.tight_layout()
    plt.savefig(os.path.join(images_path, 'analyzed_packages_pie.png'), dpi=300)

def generate_vulnerable_vs_safe_pie(df):
    affected = len(df[df['vulnerable_versions'] != 'No known vulnerabilities'])
    safe = len(df) - affected
    labels = ['Affected Packages', 'Safe Packages']
    sizes = [affected, safe]
    colors = ['#FF9999', '#66B266']
    plt.figure(figsize=(14, 10))
    wedges, texts, autotexts = plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140, wedgeprops=dict(width=0.3, edgecolor='w'), pctdistance=0.85, textprops=dict(color="black"))
    for text, autotext in zip(texts, autotexts):
        text.set(size=15)
        autotext.set(size=15)
        autotext.set_color('black')
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    plt.title('Vulnerable vs. Safe Packages', fontsize=24)
    plt.tight_layout()
    plt.savefig(os.path.join(images_path, 'vulnerable_vs_safe_pie.png'), dpi=300)

def generate_vulnerabilities_per_package_plot(df):
    affected_df = df[df['vulnerable_versions'] != 'No known vulnerabilities']
    vuln_counts = affected_df['package_name'].value_counts()
    plt.figure(figsize=(14, 10))
    sns.barplot(y=vuln_counts.index, x=vuln_counts.values, palette=sns.color_palette("Reds_r", len(vuln_counts)))
    plt.title('Number of Vulnerabilities per Affected Package', fontsize=24)
    plt.xlabel('Number of Vulnerabilities', fontsize=18)
    plt.ylabel('Package Name', fontsize=18)
    plt.tight_layout()
    plt.savefig(os.path.join(images_path, 'vuln_per_package.png'), dpi=300)

# Main logic
df = load_and_parse_safety(file_path)
generate_analyzed_packages_pie(df)
generate_vulnerable_vs_safe_pie(df)
generate_vulnerabilities_per_package_plot(df)

# Convert the images to data URL
analyzed_packages_plot_data_url = get_image_as_data_url(os.path.join(images_path, 'analyzed_packages_pie.png'))
vulnerable_vs_safe_plot_data_url = get_image_as_data_url(os.path.join(images_path, 'vulnerable_vs_safe_pie.png'))
vuln_per_package_plot_data_url = get_image_as_data_url(os.path.join(images_path, 'vuln_per_package.png'))

env = Environment(loader=FileSystemLoader('./'))
template = env.get_template(template_path)

print("Rendering template...")
html_content = template.render(
    data=df,
    analyzed_packages_plot=analyzed_packages_plot_data_url,
    vulnerable_vs_safe_plot=vulnerable_vs_safe_plot_data_url,
    vuln_per_package_plot=vuln_per_package_plot_data_url
)

print("Writing HTML content to file...")
with open('./safety/safety-report.html', 'w') as f:
    f.write(html_content)

print("Finished writing file.")
