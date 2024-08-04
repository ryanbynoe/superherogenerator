pipeline {
    agent any
    
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')
        APP_NAME = "superhero-generator"
        DOCKER_IMAGE = "${DOCKERHUB_CREDENTIALS_USR}/${APP_NAME}:${BUILD_NUMBER}"
        AWS_CREDENTIALS = credentials('aws-credentials')
        KUBECONFIG = credentials('kubeconfig')
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
                        
                        // Configure AWS CLI and deploy to Kubernetes
                        withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'aws-credentials', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {
                            bat 'aws configure set aws_access_key_id %AWS_ACCESS_KEY_ID%'
                            bat 'aws configure set aws_secret_access_key %AWS_SECRET_ACCESS_KEY%'
                            bat 'aws configure set region us-east-2'
                            
                            // Debug: Print AWS CLI version and configured region
                            bat 'aws --version'
                            bat 'aws configure get region'
                            
                            // Update kubeconfig
                            bat 'aws eks get-token --cluster-name superherogen-cluster > temp_token.json'
                            
                            // Debug: Print content of temp_token.json
                            bat 'type temp_token.json'
                            
                            // Write kubeconfig to a file
                            writeFile file: 'kubeconfig', text: KUBECONFIG
                            
                            // Update kubeconfig with the new token
                            bat '''
                            powershell -Command "$token = (Get-Content temp_token.json | ConvertFrom-Json).status.token; (Get-Content kubeconfig) -replace 'exec:.*', ('exec: { apiVersion: client.authentication.k8s.io/v1beta1, command: \\\"echo\\\", args: [\\\"' + $token + '\\\"] }') | Set-Content updated_kubeconfig"
                            '''
                            
                            // Debug: Print first few lines of updated_kubeconfig
                            bat 'powershell -Command "Get-Content updated_kubeconfig | Select-Object -First 10"'
                            
                            // Deploy to Kubernetes
                            bat "kubectl --kubeconfig=updated_kubeconfig apply -f kubernetes\\deployment.yaml"
                            bat "kubectl --kubeconfig=updated_kubeconfig apply -f kubernetes\\service.yaml"

                            // Print information about the deployment
                            bat "kubectl --kubeconfig=updated_kubeconfig get deployments"
                            bat "kubectl --kubeconfig=updated_kubeconfig get services"
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
                bat "del temp_token.json"
                bat "del kubeconfig"
                bat "del updated_kubeconfig"
            }
        }
        success {
            echo "Deployment successful!"
        }
        failure {
            echo "The pipeline failed. Please check the logs for details."
        }
    }
}