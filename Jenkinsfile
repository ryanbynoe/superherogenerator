pipeline {
    agent any
    
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')
        APP_NAME = "superhero-generator"
        DOCKER_IMAGE = "${DOCKERHUB_CREDENTIALS_USR}/${APP_NAME}:${BUILD_NUMBER}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}")
                }
            }
        }
        
        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'dockerhub') {
                        docker.image("${DOCKER_IMAGE}").push()
                        docker.image("${DOCKER_IMAGE}").push('latest')
                    }
                }
            }
        }
        
        stage('Deploy') {
            steps {
                // This is where you'd add deployment steps
                // For example, updating a Kubernetes deployment
                echo 'Deploying....'
            }
        }
    }
    
    post {
        always {
            sh 'docker logout'
        }
    }
}