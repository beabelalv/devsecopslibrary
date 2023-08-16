
import json
import os
import base64
import argparse
from jinja2 import Environment, FileSystemLoader

# Argument parsing
parser = argparse.ArgumentParser(description='Process SonarQube JSON files.')
parser.add_argument('issues_json_path', type=str, help='Path to the SonarQube issues JSON file')
parser.add_argument('hotspots_json_path', type=str, help='Path to the SonarQube hotspots JSON file')
args = parser.parse_args()

# Constants
SONARQUBE_ISSUES_JSON = args.issues_json_path
SONARQUBE_HOTSPOTS_JSON = args.hotspots_json_path
TEMPLATE_PATH = 'report_template.html'
IMAGES_PATH = './sonarqube/images/'

# Convert images to data URLs
def get_image_as_data_url(image_path):
    with open(image_path, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()
    return f"data:image/png;base64,{encoded_image}"

# Convert plots to data URLs
severity_plot_data_url = get_image_as_data_url(os.path.join(IMAGES_PATH, 'sonarqube_severity_counts_integer.png'))
component_plot_data_url = get_image_as_data_url(os.path.join(IMAGES_PATH, 'sonarqube_component_counts.png'))
type_distribution_plot_data_url = get_image_as_data_url(os.path.join(IMAGES_PATH, 'issues_and_hotspots_type_distribution_fixed.png'))
security_category_plot_data_url = get_image_as_data_url(os.path.join(IMAGES_PATH, 'sonarqube_security_category_counts_integer.png'))
vulnerability_distribution_plot_data_url = get_image_as_data_url(os.path.join(IMAGES_PATH, 'hotspots_vulnerability_distribution_integer.png'))
component_hotspots_plot_data_url = get_image_as_data_url(os.path.join(IMAGES_PATH, 'sonarqube_component_hotspots_counts.png'))

# Render HTML report using the template
env = Environment(loader=FileSystemLoader('./'))
template = env.get_template(TEMPLATE_PATH)

html_content = template.render(
    severity_plot=severity_plot_data_url,
    component_plot=component_plot_data_url,
    type_distribution_plot=type_distribution_plot_data_url,
    security_category_plot=security_category_plot_data_url,
    vulnerability_distribution_plot=vulnerability_distribution_plot_data_url,
    component_hotspots_plot=component_hotspots_plot_data_url
)

# Save the generated HTML report
with open('./sonarqube/sonarqube-report.html', 'w') as f:
    f.write(html_content)

print("SonarQube report generated successfully!")
