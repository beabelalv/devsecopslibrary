# Modifying the existing Python code to include the new plots

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
images_path = './bandit/images/'
os.makedirs(images_path, exist_ok=True)  # Create the directory if it doesn't exist

def get_image_as_data_url(image_path):
    with open(image_path, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()
    return f"data:image/png;base64,{encoded_image}"

def parse_json(data):
    df = pd.json_normalize(data['results'], meta=['filename'], errors='ignore')
    return df

def load_and_parse(file_path):
    with open(file_path) as f:
        data = json.load(f)
    df = parse_json(data)
    return df

def generate_severity_plot(df):
    severity_counts = df['issue_severity'].value_counts()
    severity_palette = {
        'LOW': "#FFEB3B",
        'MEDIUM': "#FF9800",
        'HIGH': "#F44336"
    }
    plt.figure(figsize=(20, 12))
    plt.rcParams.update({'font.size': 18})
    bars = plt.bar(severity_counts.index, severity_counts.values, color=[severity_palette[severity] for severity in severity_counts.index])
    plt.title('Number of Issues per Severity Level')
    plt.xlabel('Severity Level')
    plt.ylabel('Number of Issues')
    plt.tight_layout()
    plt.savefig(os.path.join(images_path, 'severity_counts.png'), dpi=300)

def generate_file_plot(df):
    file_counts = df['filename'].value_counts()
    plt.figure(figsize=(20, 12))
    plt.rcParams.update({'font.size': 18})
    sns.barplot(y=file_counts.index[:10], x=file_counts.values[:10], palette=sns.color_palette(["#757575", "#BDBDBD"]), orient='h')
    plt.title('Number of Issues per File (Top 10)')
    plt.xlabel('Number of Issues')
    plt.ylabel('File')
    plt.tight_layout()
    plt.savefig(os.path.join(images_path, 'file_counts.png'), dpi=300)

# New function to generate confidence level plot (Plot 4)
def generate_confidence_plot(df):
    confidence_counts = df['issue_confidence'].value_counts()
    plt.figure(figsize=(20, 12))
    plt.rcParams.update({'font.size': 18})
    sns.barplot(x=confidence_counts.index, y=confidence_counts.values, palette='viridis')
    plt.title('Distribution of Confidence Levels')
    plt.xlabel('Confidence Level')
    plt.ylabel('Number of Issues')
    plt.tight_layout()
    plt.savefig(os.path.join(images_path, 'confidence_counts.png'), dpi=300)

# New function to generate CWE ID plot (Plot 7)
def generate_cwe_plot(df):
    cwe_counts = df['issue_cwe.id'].value_counts().head(10) # Taking top 10 CWE IDs
    plt.figure(figsize=(20, 12))
    plt.rcParams.update({'font.size': 18})
    sns.barplot(x=cwe_counts.index, y=cwe_counts.values, palette='coolwarm')
    plt.title('Distribution of CWE IDs (Top 10)')
    plt.xlabel('CWE ID')
    plt.ylabel('Number of Issues')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(images_path, 'cwe_counts.png'), dpi=300)

def generate_all_plots(file_path):
    df = load_and_parse(file_path)
    generate_severity_plot(df)
    generate_file_plot(df)
    generate_confidence_plot(df) # Generating Plot 4
    generate_cwe_plot(df)       # Generating Plot 7

# Main
df = load_and_parse(file_path)
generate_all_plots(file_path)

# Convert the images to data URLs
severity_plot_data_url = get_image_as_data_url(os.path.join(images_path, 'severity_counts.png'))
file_plot_data_url = get_image_as_data_url(os.path.join(images_path, 'file_counts.png'))
confidence_plot_data_url = get_image_as_data_url(os.path.join(images_path, 'confidence_counts.png')) # Data URL for Plot 4
cwe_plot_data_url = get_image_as_data_url(os.path.join(images_path, 'cwe_counts.png'))             # Data URL for Plot 7

env = Environment(loader=FileSystemLoader('./'))
template = env.get_template(template_path)

print("Rendering template...")
html_content = template.render(
    data=df,
    severity_plot=severity_plot_data_url,
    file_plot=file_plot_data_url,
    confidence_plot=confidence_plot_data_url, # Including Plot 4 in the rendered HTML
    cwe_plot=cwe_plot_data_url                # Including Plot 7 in the rendered HTML
)

print("Writing HTML content to file...")
with open('./bandit/bandit-report.html', 'w') as f:
    f.write(html_content)

print("Finished writing file.")