def call(String jsonReportPath) {
    def scriptPath = libraryResource('bandit/html_generator.py')
    echo "Script Path: ${scriptPath}"
    sh "python ${scriptPath} ${jsonReportPath}"
}