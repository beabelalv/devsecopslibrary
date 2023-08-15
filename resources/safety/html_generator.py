
import pandas as pd
import matplotlib.pyplot as plt
import os
import json
from jinja2 import Environment, FileSystemLoader
import datetime

# Constants
images_path = './safety/images/'

# Functions
def parse_safety_json(data):
    vulnerabilities = []
    for item in data:
        vulnerabilities.append({
            'package_name': item[0],
            'affected_versions': item[1],
            'installed': item[2],
            'advisory': item[3],
            'CVE': item[4],
            'advisory_url': item[5]
        })
    df = pd.DataFrame(vulnerabilities)
    return df

def generate_vulnerable_vs_safe_pie_plot(df):
    vulnerable = len(df[df['advisory'] != 'No known vulnerabilities'])
    safe = len(df[df['advisory'] == 'No known vulnerabilities'])
    labels = ['Vulnerable Packages', 'Safe Packages']
    sizes = [vulnerable, safe]
    colors = ['#FF6347', '#4CAF50']
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.title("Vulnerable vs Safe Packages")
    plt.savefig(os.path.join(images_path, 'vulnerable_vs_safe_pie_plot.png'), dpi=300)

def generate_vulnerabilities_per_affected_package(df):
    vulnerabilities_count = df.groupby('package_name')['CVE'].count().sort_values(ascending=False)
    plt.figure(figsize=(10, 8))
    vulnerabilities_count.plot(kind='bar', color='#FFA07A')
    plt.title('Number of Vulnerabilities per Affected Package')
    plt.xlabel('Package Name')
    plt.ylabel('Number of Vulnerabilities')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.grid(axis='y')
    for index, value in enumerate(vulnerabilities_count):
        plt.text(index, value + 0.1, str(value), ha='center', va='center')
    plt.savefig(os.path.join(images_path, 'vulnerabilities_per_affected_package.png'), dpi=300)

def generate_all_analyzed_packages_pie_plot(df):
    labels = df['package_name']
    sizes = [1] * len(df)
    plt.figure(figsize=(10, 10))
    plt.pie(sizes, labels=labels, autopct='', startangle=90)
    plt.axis('equal')
    plt.title("All Analyzed Packages")
    plt.savefig(os.path.join(images_path, 'all_analyzed_packages_pie_plot.png'), dpi=300)

def generate_all_plots_for_safety(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    df = parse_safety_json(data)
    os.makedirs(images_path, exist_ok=True)
    generate_vulnerable_vs_safe_pie_plot(df)
    generate_all_analyzed_packages_pie_plot(df)
    generate_vulnerabilities_per_affected_package(df)
    return df, data

def generate_html_report(file_path, template_path, output_path, image_path, data):
    env = Environment(loader=FileSystemLoader('/'))
    template = env.get_template(template_path)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html_content = template.render(timestamp=timestamp, image_path=image_path, data=data)
    with open(output_path, 'w') as f:
        f.write(html_content)

# Main execution
if __name__ == '__main__':
    file_path = 'safety-results.json'
    template_path = '/mnt/data/temp_report_template.html'
    output_path = './safety/safety_report.html'
    df, data = generate_all_plots_for_safety(file_path)
    generate_html_report(file_path, template_path, output_path, images_path, df.to_dict(orient="records"))
