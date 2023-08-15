
def call(Map config = [:]) {
    // Load the Python script for Safety report generation
    loadScript(name: 'safety_html_generator.py', path: 'safety/safety_html_generator.py')
    
    // Load the HTML template for Safety report
    def tempTemplateFile = 'temp_safety_report_template.html'
    loadScript(name: tempTemplateFile, path: 'safety/safety_report_template.html')
    
    // Call the Python script with the JSON file and temporary HTML template file
    sh "python ./safety_html_generator.py ${config.json} ${tempTemplateFile}"
}