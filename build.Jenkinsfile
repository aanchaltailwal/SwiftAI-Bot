pipeline {

    agent any
	
	environment {
		AWS_REGION = 'eu-north-1'
        ECR_REGISTRY_URL = '854171615125.dkr.ecr.eu-north-1.amazonaws.com'
        DOCKER_IMAGE_TAG = '0.0.1'
    }

    stages {

        stage('Authentication') {

            steps {

                sh '''
                aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY_URL}

                '''

            } 

        }


        stage('Build Yolo5') {

            steps {

                sh 'docker build -t abhishekc-yolo5 ./Yolo5'

            }

        }


        stage('Push Yolo5 to ECR') {

            steps {

                sh '''
                docker tag abhishekc-yolo5:latest ${ECR_REGISTRY_URL}/abhishekc-yolo5:latest
                docker push ${ECR_REGISTRY_URL}/abhishekc-yolo5:latest
                '''

            }

        }


        stage('Build Telegram Bot') {

            steps {

                sh 'docker build -t abhishekc-tg-bot ./Telegram_Bot'

            }
        }


        stage('Push Telegram_Bot to ECR') {

            steps {

                sh '''
                docker tag abhishekc-tg-bot:latest ${ECR_REGISTRY_URL}/abhishekc-tg-bot:latest
                docker push ${ECR_REGISTRY_URL}/abhishekc-tg-bot:latest
                '''
            }
        }
        
        
        
        stage('Trigger Deploy') {
        	steps {
        		build job: 'SwiftAI_Deploy', wait: false, parameters: [
            	string(name: 'DOCKER_TAG', value: "${DOCKER_IMAGE_TAG}")
        		]
    		}
		}

    }

}
