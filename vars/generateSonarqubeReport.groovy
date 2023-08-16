def call() {
    // Load the Python script
    loadScript(name: 'html_generator.py', path: 'sonarqube/html_generator.py')
    
    // Call the Python script with the JSON file paths
    sh "python ./html_generator.py sonarqube_open_issues.json sonarqube_open_hotspots.json"
}