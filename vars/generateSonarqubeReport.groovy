def call(Map config = [:]) {
    // Default values
    def issuesJson = config.issuesJson ?: 'sonarqube_open_issues.json'
    def hotspotsJson = config.hotspotsJson ?: 'sonarqube_open_hotspots.json'
    def scriptPath = config.scriptPath ?: 'sonarqube/html_generator.py'

    // Load the Python script
    loadScript(name: 'html_generator.py', path: scriptPath)
    
    // Call the Python script with the JSON file paths
    sh "python ./html_generator.py ${issuesJson} ${hotspotsJson}"
}
