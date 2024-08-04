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
        
        stage('Build and Deploy') {
            steps {
                script {
                    // Build Docker Image
                    bat "docker build -t ${DOCKER_IMAGE} ."
                    
                    // Push Docker Image
                    withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        bat "echo %DOCKER_PASSWORD% | docker login -u %DOCKER_USERNAME% --password-stdin"
                        bat "docker push ${DOCKER_IMAGE}"
                        bat "docker push ${DOCKERHUB_CREDENTIALS_USR}/${APP_NAME}:latest"
                    }
                    
                    // Deploy to Kubernetes
                    withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                        // Update the deployment YAML with the new image
                        bat "powershell -Command \"(Get-Content kubernetes\\deployment.yaml) -replace 'image: .*', 'image: ${DOCKER_IMAGE}' | Set-Content kubernetes\\deployment.yaml\""

                        // Apply the Kubernetes configurations
                        bat "kubectl --kubeconfig=%KUBECONFIG% apply -f kubernetes\\deployment.yaml"
                        bat "kubectl --kubeconfig=%KUBECONFIG% apply -f kubernetes\\service.yaml"
                    }
                }
            }
        }
    }
    
    post {
        always {
            script {
                bat "docker logout"
            }
        }
    }
}