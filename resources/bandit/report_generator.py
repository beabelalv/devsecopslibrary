from parser import load_and_parse
from graphics_generator import generate_severity_plot, generate_file_plot
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

def generate_report(df, severity_plot_path, file_plot_path, template_path, output_path):
    # Load the Jinja2 template
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(template_path)

    # Render the template with the data
    rendered_template = template.render(
        data=df,
        severity_plot=severity_plot_path,
        file_plot=file_plot_path
    )

    # Convert the rendered template to a PDF
    HTML(string=rendered_template).write_pdf(output_path)

def main():
    # Load and parse the JSON data
    df = load_and_parse('./reports/bandit-results.json')

    # Generate the graphics
    severity_plot_path = generate_severity_plot(df)
    file_plot_path = generate_file_plot(df)

    # Generate the report
    generate_report(df, severity_plot_path, file_plot_path, './bandit/report_template.html', './bandit/report.pdf')

if __name__ == "__main__":
    main()
