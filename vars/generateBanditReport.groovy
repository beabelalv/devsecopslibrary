def call(String jsonReportPath) {
    sh "python resources/bandit/html_generator.py ${jsonReportPath}"
}