def call(Map config = [:]) {
    loadScript(name: 'html_generator.py')
    sh "python ./html_generator.py ${config.json}"
}