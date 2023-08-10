def generateBanditReport(String jsonReportPath = 'reports/bandit-results.json') {
    def scriptPath = libraryResource('bandit/html_generator.py')
    sh "cp ${scriptPath} ."
    sh "python html_generator.py ${jsonReportPath}"
}