def call(Map config = [:]) {
    loadScript(name: 'html_generator.py')
    python "./html_generator.py ${config.json}"
}