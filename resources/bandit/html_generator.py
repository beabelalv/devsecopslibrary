from jinja2 import Environment, FileSystemLoader
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from parser import load_and_parse


#Functions:#
def parse_json(data):
    # Convert to DataFrame
    df = pd.json_normalize(data['results'], 
                           meta=['filename'], errors='ignore')

    return df

def load_and_parse(file_path):
    # Load JSON data
    with open(file_path) as f:
        data = json.load(f)

    # Parse data into DataFrame
    df = parse_json(data)
    #print(df.head())
    return df

#Graphics:

def generate_severity_plot(df):
    # Count the number of issues per severity level
    severity_counts = df['issue_severity'].value_counts()

    # Define color palette based on severity
    severity_palette = {
        'LOW': "#FFEB3B",
        'MEDIUM': "#FF9800",
        'HIGH': "#F44336"
    }

    # Plot the number of issues per severity level
    plt.figure(figsize=(20, 12))  # Make the image larger
    plt.rcParams.update({'font.size': 18})  # Increase font size
    bars = plt.bar(severity_counts.index, severity_counts.values, color=[severity_palette[severity] for severity in severity_counts.index])
    plt.title('Number of Issues per Severity Level')
    plt.xlabel('Severity Level')
    plt.ylabel('Number of Issues')
    plt.tight_layout()  # This will prevent the labels from being cut off
    plt.savefig('./bandit/images/severity_counts.png', dpi=300)  # Increase DPI

def generate_file_plot(df):
    # Count the number of issues per file
    file_counts = df['filename'].value_counts()

    # Plot the number of issues per file (for the top 10 files with the most issues)
    plt.figure(figsize=(20, 12))  # Make the image larger
    plt.rcParams.update({'font.size': 18})  # Increase font size
    sns.barplot(y=file_counts.index[:10], x=file_counts.values[:10], palette=sns.color_palette(["#757575", "#BDBDBD"]), orient='h')  # Two shades of grey
    plt.title('Number of Issues per File (Top 10)')
    plt.xlabel('Number of Issues')
    plt.ylabel('File')
    plt.tight_layout()  # This will prevent the labels from being cut off
    plt.savefig('./bandit/images/file_counts.png', dpi=300)  # Increase DPI

def generate_all_plots():
    # Parse JSON data
    df = load_and_parse('./reports/bandit-results.json')

    # Generate plots
    generate_severity_plot(df)
    generate_file_plot(df)

###########################      MAIN      ###########################

# Parse JSON data to create df
df = load_and_parse('./reports/bandit-results.json')

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
with open('./bandit/report.html', 'w') as f:
    f.write(html_content)

print("Finished writing file.")