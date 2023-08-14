def call(String jsonReportPath) {
    // Load the loadScript.groovy file
    def loadScript = load 'path/to/loadScript.groovy'

    // Use the call function to run the specific script with the JSON report path as an argument
    loadScript.call('bandit/html_generator.py', jsonReportPath)
}