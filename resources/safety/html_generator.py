
import json
import pandas as pd
import matplotlib.pyplot as plt
from jinja2 import Environment, FileSystemLoader

# Constants for plot sizes and styles
FIGSIZE = (6, 4)
COLORS = ["#E63946", "#2A9D8F", "#F4FAFF", "#457B9D", "#1D3557"]

def parse_safety_json(data):
    affected_packages_data = []
    vulnerabilities_mapping = {}
    for vulnerability in data.get('vulnerabilities', []):
        vulnerabilities_mapping.setdefault(vulnerability['package_name'], []).append(vulnerability)

    for package_name, package_details in data['affected_packages'].items():
        vulnerabilities = vulnerabilities_mapping.get(package_name, [])
        for vulnerability in vulnerabilities:
            affected_packages_data.append({
                'package_name': package_name,
                'installed_version': package_details['version'],
                'vulnerability_description': vulnerability.get('description', ''),
                'cve': vulnerability.get('cve', ''),
                'advisory': vulnerability.get('advisory', ''),
                'advisory_url': vulnerability.get('more_info_url', '')
            })
    df = pd.DataFrame(affected_packages_data)
    return df

def generate_vulnerable_vs_safe_pie_plot(df):
    safe = len(df[df['vulnerability_description'] == 'No known vulnerabilities'])
    vulnerable = len(df) - safe
    labels = ['Vulnerable Packages', 'Safe Packages']
    sizes = [vulnerable, safe]
    explode = (0.1, 0)
    plt.figure(figsize=FIGSIZE)
    plt.pie(sizes, explode=explode, labels=labels, colors=COLORS[:2], autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.savefig("/mnt/data/vulnerable_vs_safe_pie_plot.png", bbox_inches='tight')
    plt.close()

def generate_vulnerabilities_per_package_plot(df):
    vulnerabilities_count = df.groupby('package_name').size()
    plt.figure(figsize=FIGSIZE)
    vulnerabilities_count.plot(kind='bar', color=COLORS[3], edgecolor=COLORS[4])
    plt.title('Number of Vulnerabilities per Affected Package')
    plt.ylabel('Number of Vulnerabilities')
    plt.xlabel('Package Name')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    for index, value in enumerate(vulnerabilities_count):
        plt.text(index, value + 0.1, str(value), ha='center')
    plt.savefig("/mnt/data/vulnerabilities_per_package_plot.png", bbox_inches='tight')
    plt.close()

def generate_total_packages_pie_plot(data):
    all_packages = list(data['scanned_packages'].keys())
    plt.figure(figsize=FIGSIZE)
    plt.pie([1]*len(all_packages), labels=all_packages, colors=COLORS, autopct='%1.1f%%')
    plt.axis('equal')
    plt.savefig("/mnt/data/total_packages_pie_plot.png", bbox_inches='tight')
    plt.close()

def generate_all_plots_for_safety(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    df = parse_safety_json(data)
    generate_vulnerable_vs_safe_pie_plot(df)
    generate_vulnerabilities_per_package_plot(df)
    generate_total_packages_pie_plot(data)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print("Usage: python html_generator.py <path_to_safety_results.json> <path_to_html_template>")
        sys.exit(1)
    file_path = sys.argv[1]
    template_path = sys.argv[2]
    generate_all_plots_for_safety(file_path)
    with open(template_path, 'r') as f:
        template_content = f.read()
    env = Environment(loader=FileSystemLoader('.'))
    template = env.from_string(template_content)
    with open("/mnt/data/safety_report.html", "w") as f:
        f.write(template.render(data=df_safety))