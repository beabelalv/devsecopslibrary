def call(String jsonReportPath) {
    // Load the loadScript.groovy file
    def loadScript = load 'loadScript.groovy' // Remove 'vars/' from the path

    // Use the call function to run the specific script with the JSON report path as an argument
    loadScript.call('resources/bandit/html_generator.py', jsonReportPath)
}