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
                    try {
                        // Build Docker Image
                        bat "docker build -t ${DOCKER_IMAGE} ."
                        
                        // Docker Login and Push
                        withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                            bat 'docker login -u %DOCKER_USERNAME% -p %DOCKER_PASSWORD%'
                            bat "docker push ${DOCKER_IMAGE}"
                            bat "docker tag ${DOCKER_IMAGE} ${DOCKERHUB_CREDENTIALS_USR}/${APP_NAME}:latest"
                            bat "docker push ${DOCKERHUB_CREDENTIALS_USR}/${APP_NAME}:latest"
                        }
                        
                        // Deploy to Kubernetes
                        withCredentials([string(credentialsId: 'kubeconfig', variable: 'KUBECONFIG_CONTENT')]) {
                            // Write kubeconfig content to a temporary file
                            writeFile file: 'temp_kubeconfig', text: KUBECONFIG_CONTENT

                            // Update the deployment YAML with the new image
                            bat "powershell -Command \"(Get-Content kubernetes\\deployment.yaml) -replace 'image: .*', 'image: ${DOCKER_IMAGE}' | Set-Content kubernetes\\deployment.yaml\""

                            // Apply the Kubernetes configurations
                            bat "kubectl --kubeconfig=temp_kubeconfig apply -f kubernetes\\deployment.yaml"
                            bat "kubectl --kubeconfig=temp_kubeconfig apply -f kubernetes\\service.yaml"

                            // Remove the temporary kubeconfig file
                            bat "del temp_kubeconfig"
                        }
                    } catch (Exception e) {
                        currentBuild.result = 'FAILURE'
                        error "Build failed: ${e.getMessage()}"
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
        failure {
            echo "The pipeline failed. Please check the logs for details."
        }
    }
}