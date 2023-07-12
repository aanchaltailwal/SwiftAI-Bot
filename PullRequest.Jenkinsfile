pipeline {
    agent any

    stages {

        stage('Safety Check') {
            steps {
                sh 'pip install safety'
                sh 'cd Yolo5 && /var/lib/jenkins/.local/bin/safety check -r requirements.txt'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo "Installing requirements"
                sh 'cd Yolo5 && pip install -r requirements.txt'
                sh 'pip install pylint'
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