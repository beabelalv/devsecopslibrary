def call(Map config = [:]) {
    loadLinuxScript(name: 'hello-world.sh')
    python "./html_generator.py ${config.json}"
}