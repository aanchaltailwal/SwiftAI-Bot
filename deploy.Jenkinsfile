pipeline {
    agent any

    
    parameters { string(name: 'DOCKER_TAG', defaultValue: '', description: '') }
    
    environment {
        AWS_REGION_K8S = 'us-east-2'
        K8S_CLUSTER_NAME = 'k8s-batch1'
        K8S_NAMESPACE = 'abhishekc-ns'
        IMAGE_VERSION = ${DOCKER_TAG}
    }
    
    stages {
    	
    	stage('Staring the deploy process') {
            steps {
                // withEnv(['PATH+EXTRA=/usr/sbin:/usr/bin:/sbin:/bin']) {
                    sh 'echo "Starting off the deploy process"'
                // }
            }
        }
        stage('Connecting to the k8s cluster') {
            steps {
                // withEnv(['PATH+EXTRA=/usr/sbin:/usr/bin:/sbin:/bin']) {
                    sh 'aws eks --region ${AWS_REGION_K8S} update-kubeconfig --name ${K8S_CLUSTER_NAME}'
                // }
            }
        }
        stage('Setting default namespace') {
            steps {
                // withEnv(['PATH+EXTRA=/usr/sbin:/usr/bin:/sbin:/bin']) {
                    sh 'kubectl config set-context --current --namespace=${K8S_NAMESPACE}'
                // }
            }
        }
        
        stage('Deploy Yolo5') {
            steps {
            	sh 'kubectl apply -f yolo5-deployment.yaml --namespace abhishekc-ns'
        
            }
        }

        stage('Deploy Yolo5 Service') {
            steps {
                sh 'kubectl apply -f yolo5-service.yaml --namespace abhishekc-ns'
            }
        }

        stage('Deploy Telegram_Bot') {
            steps {
                sh 'kubectl apply -f bot-deployment.yaml --namespace abhishekc-ns'
            }
        }
    }
} 
