pipeline {
    agent any

    stages {

        stage('Safety Check') {
            steps {
                script {
                    def vulnerabilities = sh(
                        returnStdout: true,
                        script: '''
                            pip install safety
                            cd Yolo5 && safety check --file requirements.txt --json
                        '''
                    ).trim()

                    def json = readJSON text: vulnerabilities

                    // Fail the build if any vulnerabilities are found
                    if (json.vulnerabilities) {
                        error("Security vulnerabilities found. Failing the build.")
                    }
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                echo "Installing requirements"
                sh 'cd Yolo5 && pip install -r requirements.txt'
                sh 'pip install pylint'
            }
        }

        stage('Unittest') {
            steps {
                echo "Running unit tests"
                sh 'cd Yolo5 && python3 -m pytest --junitxml results.xml tests'
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'Yolo5/results.xml'
                }
            }
        }

        stage('Black Linting') {
            steps {
                echo "Running Black Linitng"
                sh 'pip install black'
                sh 'black .'
            }
        }
    }
}