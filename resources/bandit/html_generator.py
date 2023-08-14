import argparse
import json
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

# Functions
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
    plt.savefig('./bandit/images/severity_counts.png', dpi=300)

def generate_file_plot(df):
    file_counts = df['filename'].value_counts()
    plt.figure(figsize=(20, 12))
    plt.rcParams.update({'font.size': 18})
    sns.barplot(y=file_counts.index[:10], x=file_counts.values[:10], palette=sns.color_palette(["#757575", "#BDBDBD"]), orient='h')
    plt.title('Number of Issues per File (Top 10)')
    plt.xlabel('Number of Issues')
    plt.ylabel('File')
    plt.tight_layout()
    plt.savefig('./bandit/images/file_counts.png', dpi=300)

def generate_all_plots(file_path):
    df = load_and_parse(file_path)
    generate_severity_plot(df)
    generate_file_plot(df)

# Main
df = load_and_parse(file_path)
generate_all_plots(file_path)

env = Environment(loader=FileSystemLoader('./'))
template = env.get_template(template_path)

print("Rendering template...")
html_content = template.render(
    data=df,
    severity_plot='./bandit/images/severity_counts.png',
    file_plot='./bandit/images/file_counts.png'
)

print("Writing HTML content to file...")
with open('./bandit/report.html', 'w') as f:
    f.write(html_content)

print("Finished writing file.")