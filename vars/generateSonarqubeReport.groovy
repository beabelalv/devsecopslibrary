def call(Map config = [:]) {
    // Load the Python script
    loadScript(name: 'sonarqube_html_generator.py', path: 'sonarqube/sonarqube_html_generator.py')
    
    // Load the HTML template
    def tempTemplateFile = 'temp_sonarqube_report_template.html'
    loadScript(name: tempTemplateFile, path: 'sonarqube/sonarqube_report_template.html')
    
    // Call the Python script with the JSON files and temporary HTML template file paths
    sh "python ./sonarqube_html_generator.py ${config.issues_json} ${config.hotspots_json} ${tempTemplateFile}"
}
