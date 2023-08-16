
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

def load_json(file_path):
    with open(file_path) as f:
        data = json.load(f)
    return pd.json_normalize(data['issues'])

# Functions to generate plots
def generate_severity_plot(df):
    # ... [Code for generating plot: Number of Issues per Severity Level]
    plt.savefig(os.path.join(images_path, 'severity_counts.png'))

def generate_file_plot(df):
    # ... [Code for generating plot: Top 10 Components with Most Issues]
    plt.savefig(os.path.join(images_path, 'file_counts.png'))

def generate_issue_type_plot(df):
    # ... [Code for generating plot: Distribution of Issue Types]
    plt.savefig(os.path.join(images_path, 'issue_type_counts.png'))

def generate_category_plot(df):
    # ... [Code for generating plot: Number of Hotspots per Security Category]
    plt.savefig(os.path.join(images_path, 'category_counts.png'))

def generate_vulnerability_prob_plot(df):
    # ... [Code for generating plot: Distribution of Hotspots by Vulnerability Probability]
    plt.savefig(os.path.join(images_path, 'vulnerability_prob_counts.png'))

def generate_hotspot_file_plot(df):
    # ... [Code for generating plot: Top 10 Components with Most Hotspots]
    plt.savefig(os.path.join(images_path, 'hotspot_file_counts.png'))

# Main
df_issues = load_json(issues_file_path)
df_hotspots = load_json(hotspots_file_path)

# Generate all plots
generate_severity_plot(df_issues)
generate_file_plot(df_issues)
generate_issue_type_plot(df_issues)
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