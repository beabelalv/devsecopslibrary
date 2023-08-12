def call(String jsonReportPath) {
    def scriptPath = libraryResource('bandit/html_generator.py')
    sh "python ${scriptPath} ${jsonReportPath}"
}