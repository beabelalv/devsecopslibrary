import argparse
import json
import os
import base64
import pandas as pd
import matplotlib.pyplot as plt

# Argument parsing
parser = argparse.ArgumentParser(description='Process the JSON file and HTML template.')
parser.add_argument('file_path', type=str, help='Path to the JSON file')
parser.add_argument('template_path', type=str, help='Path to the HTML template file')
args = parser.parse_args()
file_path = args.file_path
template_path = args.template_path

# Functions
def parse_safety_json(data):
    results = []
    for item in data['issues']:
        package, affected, installed, advisory, cve, advisory_url = item
        results.append({
            'package_name': package,
            'affected_version': affected,
            'installed_version': installed,
            'vulnerability_description': advisory,
            'cve': cve,
            'advisory_url': advisory_url
        })
    df = pd.DataFrame(results)
    return df

def get_image_as_data_url(image_path):
    with open(image_path, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()
    return f"data:image/png;base64,{encoded_image}"

def generate_vulnerable_vs_safe_pie_plot(df):
    safe = len(df[df['vulnerability_description'] == 'No known vulnerabilities'])
    vulnerable = len(df) - safe
    labels = ['Vulnerable', 'Safe']
    sizes = [vulnerable, safe]
    colors = ['#ff9999','#66b2ff']
    explode = (0.1, 0)
    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.0f%%', startangle=140)
    ax.axis('equal')
    plt.title("Vulnerable vs Safe Packages")
    plt.savefig("vulnerable_vs_safe_pie_plot.png", bbox_inches='tight', dpi=150)
    plt.close()

def generate_vulnerabilities_per_package_plot(df):
    vulnerability_counts = df['package_name'].value_counts()
    fig, ax = plt.subplots()
    vulnerability_counts.plot(kind='bar', ax=ax, color='#ff9999')
    plt.title("Number of Vulnerabilities Per Affected Package")
    plt.ylabel("Number of Vulnerabilities")
    plt.xlabel("Package Name")
    for p in ax.patches:
        ax.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points')
    plt.tight_layout()
    plt.savefig("vulnerabilities_per_package_plot.png", bbox_inches='tight', dpi=150)
    plt.close()

def generate_total_packages_pie_plot(data):
    labels = list(data['scanned_packages'].keys())
    sizes = [1] * len(labels)
    colors = plt.cm.Paired.colors
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.0f%%', startangle=140)
    ax.axis('equal')
    plt.title("Total Analyzed Packages")
    plt.savefig("total_packages_pie_plot.png", bbox_inches='tight', dpi=150)
    plt.close()

def load_and_parse(file_path):
    with open(file_path) as f:
        data = json.load(f)
    df = parse_safety_json(data)
    return df, data

def generate_all_plots_for_safety(file_path):
    df, data = load_and_parse(file_path)
    generate_vulnerable_vs_safe_pie_plot(df)
    generate_vulnerabilities_per_package_plot(df)
    generate_total_packages_pie_plot(data)
    return df, data

from jinja2 import Environment, FileSystemLoader

df, data = generate_all_plots_for_safety(file_path)

env = Environment(loader=FileSystemLoader('./'))
template = env.get_template(template_path)

total_packages_plot_data_url = get_image_as_data_url("total_packages_pie_plot.png")
vulnerable_vs_safe_plot_data_url = get_image_as_data_url("vulnerable_vs_safe_pie_plot.png")
vulnerabilities_per_package_plot_data_url = get_image_as_data_url("vulnerabilities_per_package_plot.png")

html_content = template.render(
    data=df,
    total_packages_plot=total_packages_plot_data_url,
    vulnerable_vs_safe_plot=vulnerable_vs_safe_plot_data_url,
    vulnerabilities_per_package_plot=vulnerabilities_per_package_plot_data_url
)

with open('safety_report.html', 'w') as f:
    f.write(html_content)
