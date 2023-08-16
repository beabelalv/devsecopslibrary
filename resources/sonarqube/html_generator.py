import argparse
import json
import os
import base64
from jinja2 import Environment, FileSystemLoader
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Argument parsing for SonarQube report generation
parser = argparse.ArgumentParser(description='Process the JSON files for SonarQube and HTML template.')
parser.add_argument('issues_file_path', type=str, help='Path to the SonarQube issues JSON file')
parser.add_argument('hotspots_file_path', type=str, help='Path to the SonarQube hotspots JSON file')
parser.add_argument('template_path', type=str, help='Path to the HTML template file')
args = parser.parse_args()
issues_file_path = args.issues_file_path
hotspots_file_path = args.hotspots_file_path
template_path = args.template_path

# Define the path for images
images_path = './sonarqube/images/'
os.makedirs(images_path, exist_ok=True)

def get_image_as_data_url(image_path):
    with open(image_path, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()
    return f"data:image/png;base64,{encoded_image}"

def load_json_issues(file_path):
    with open(file_path) as f:
        data = json.load(f)
    return pd.json_normalize(data['issues'])

def load_json_hotspots(file_path):
    with open(file_path) as f:
        data = json.load(f)
    return pd.json_normalize(data['hotspots'])

# Functions to generate plots
def generate_severity_plot(df):
    plt.figure(figsize=(10, 5))
    sns.countplot(data=df, x='severity', order=['BLOCKER', 'CRITICAL', 'MAJOR', 'MINOR', 'INFO'])
    plt.title('Number of Issues per Severity Level')
    plt.xlabel('Severity Level')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig(os.path.join(images_path, 'severity_counts.png'))

def generate_file_plot(df):
    plt.figure(figsize=(10, 5))
    file_counts = df['component'].value_counts().head(10)
    file_counts.plot(kind='barh', color='skyblue')
    plt.title('Top 10 Components with Most Issues')
    plt.xlabel('Count')
    plt.ylabel('Component')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(os.path.join(images_path, 'file_counts.png'))

def generate_issue_type_hotspot_plot(df_issues, total_hotspots):
    plt.figure(figsize=(10, 5))
    types = df_issues['type'].value_counts()
    types['SECURITY_HOTSPOT'] = total_hotspots
    types.plot(kind='pie', autopct='%1.1f%%')
    plt.title('Distribution of Issue Types and Total Security Hotspots')
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig(os.path.join(images_path, 'issue_type_counts.png'))

def generate_category_plot(df):
    plt.figure(figsize=(10, 5))
    df['category'].value_counts().plot(kind='pie', autopct='%1.1f%%')
    plt.title('Number of Hotspots per Security Category')
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig(os.path.join(images_path, 'category_counts.png'))

def generate_vulnerability_prob_plot(df):
    plt.figure(figsize=(10, 5))
    df['vulnerabilityProbability'].value_counts().plot(kind='pie', autopct='%1.1f%%')
    plt.title('Distribution of Hotspots by Vulnerability Probability')
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig(os.path.join(images_path, 'vulnerability_prob_counts.png'))

def generate_hotspot_file_plot(df):
    plt.figure(figsize=(10, 5))
    hotspot_counts = df['component'].value_counts().head(10)
    hotspot_counts.plot(kind='barh', color='lightcoral')
    plt.title('Top 10 Components with Most Hotspots')
    plt.xlabel('Count')
    plt.ylabel('Component')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(os.path.join(images_path, 'hotspot_file_counts.png'))

# Main
df_issues = load_json_issues(issues_file_path)
df_hotspots = load_json_hotspots(hotspots_file_path)

# Generate all plots
generate_severity_plot(df_issues)
generate_file_plot(df_issues)
generate_issue_type_hotspot_plot(df_issues, len(df_hotspots))
generate_category_plot(df_hotspots)
generate_vulnerability_prob_plot(df_hotspots)
generate_hotspot_file_plot(df_hotspots)

# Convert the images to data URLs
severity_plot_data_url = get_image_as_data_url(os.path.join(images_path, 'severity_counts.png'))
file_plot_data_url = get_image_as_data_url(os.path.join(images_path, 'file_counts.png'))
issue_type_plot_data_url = get_image_as_data_url(os.path.join(images_path, 'issue_type_counts.png'))
category_plot_data_url = get_image_as_data_url(os.path.join(images_path, 'category_counts.png'))
vulnerability_prob_plot_data_url = get_image_as_data_url(os.path.join(images_path, 'vulnerability_prob_counts.png'))
hotspot_file_plot_data_url = get_image_as_data_url(os.path.join(images_path, 'hotspot_file_counts.png'))

# Render the HTML template
env = Environment(loader=FileSystemLoader('./'))
template = env.get_template(template_path)
html_content = template.render(
    issues_data=df_issues,
    hotspots_data=df_hotspots,
    severity_plot=severity_plot_data_url,
    file_plot=file_plot_data_url,
    issue_type_plot=issue_type_plot_data_url,
    category_plot=category_plot_data_url,
    vulnerability_prob_plot=vulnerability_prob_plot_data_url,
    hotspot_file_plot=hotspot_file_plot_data_url
)

# Save the rendered content to an HTML file
with open('./sonarqube/sonarqube-report.html', 'w') as f:
    f.write(html_content)

print("Finished writing file.")
