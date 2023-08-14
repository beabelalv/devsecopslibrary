def call(String scriptPath, String args = '') {
    // Retrieve the content of the Python script
    def scriptContent = libraryResource(scriptPath)

    // Create a temporary file to hold the script
    def tempScriptFile = "temp_script.py"
    writeFile file: tempScriptFile, text: scriptContent

    // Now execute the temporary file
    sh "python ${tempScriptFile} ${args}"

    // Optionally, you can delete the temporary file afterward
    sh "rm ${tempScriptFile}"
}