def call(Map config = [:]) {
    loadScript(name: 'hello-world.sh')
    python "./html_generator.py ${config.json}"
}