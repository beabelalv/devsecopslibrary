from jinja2 import Environment, FileSystemLoader
from parser import parse_json, load_and_parse
from graphics_generator import generate_all_plots  # Import the new function
import sys  # Import sys to work with command-line arguments

# Check if a command-line argument was passed, else use the default path
json_report_path = sys.argv[1] if len(sys.argv) > 1 else './reports/bandit-results.json'

# Parse JSON data to create df using the variable json_report_path
df = load_and_parse(json_report_path)

# Generate plots
generate_all_plots()  # Call the new function

# Set up the environment for Jinja2
env = Environment(loader=FileSystemLoader('./'))

# Load the HTML template
template = env.get_template('./bandit/report_template.html')

print("Rendering template...")
html_content = template.render(
    data=df,
    severity_plot='./images/severity_counts.png',
    file_plot='./images/file_counts.png'
)

print("Writing HTML content to file...")
with open('./bandit/bandit-report.html', 'w') as f:
    f.write(html_content)

print("Finished writing file.")
