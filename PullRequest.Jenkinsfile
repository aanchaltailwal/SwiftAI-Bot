pipeline {
    agent any

    stages {

        stage('Safety Check') {
            steps {
                sh 'pip install safety'
                sh 'cd Yolo5 && safety check -r requirements.txt'
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