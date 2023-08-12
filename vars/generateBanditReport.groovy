def call(String jsonReportPath) {
    def scriptPath = libraryResource('bandit/html_generator.py')
    sh "python html_generator.py ${jsonReportPath}"
}