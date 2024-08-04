pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')
        APP_NAME = "superhero-generator"
        DOCKER_IMAGE = "${DOCKERHUB_CREDENTIALS_USR}/${APP_NAME}:${BUILD_NUMBER}"
        AWS_CREDENTIALS = credentials('aws-creds')
        KUBECONFIG = credentials('kubeconfig')
        CLUSTER_NAME = "your-eks-cluster-name"
        AWS_REGION = "us-east-1"  // Replace with your AWS region
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Python App') {
            steps {
                script {
                    // Create and activate virtual environment
                    bat 'python -m venv venv'
                    bat 'venv\\Scripts\\activate.bat && python -m pip install --upgrade pip'

                    // Install dependencies from requirements.txt
                    bat 'venv\\Scripts\\activate.bat && pip install -r requirements.txt'

                    // Install pytest explicitly
                    bat 'venv\\Scripts\\activate.bat && pip install pytest'

                    // List installed packages for debugging
                    bat 'venv\\Scripts\\activate.bat && pip list'

                    // Run tests using pytest
                    bat 'venv\\Scripts\\activate.bat && pytest tests/ -v'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    bat "docker build -t ${DOCKER_IMAGE} ."
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        bat 'docker login -u %DOCKER_USERNAME% -p %DOCKER_PASSWORD%'
                        bat "docker push ${DOCKER_IMAGE}"
                        bat "docker tag ${DOCKER_IMAGE} ${DOCKERHUB_CREDENTIALS_USR}/${APP_NAME}:latest"
                        bat "docker push ${DOCKERHUB_CREDENTIALS_USR}/${APP_NAME}:latest"
                    }
                }
            }
        }

        stage('Deploy to EKS') {
            steps {
                script {
                    withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'aws-creds', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {
                        // Configure AWS CLI
                        bat 'aws configure set aws_access_key_id %AWS_ACCESS_KEY_ID%'
                        bat 'aws configure set aws_secret_access_key %AWS_SECRET_ACCESS_KEY%'
                        bat "aws configure set region ${AWS_REGION}"

                        // Update kubeconfig
                        bat "aws eks get-token --cluster-name ${CLUSTER_NAME} > temp_token.json"
                        bat "aws eks update-kubeconfig --name ${CLUSTER_NAME} --region ${AWS_REGION}"

                        // Apply Kubernetes manifests
                        bat "kubectl apply -f kubernetes/deployment.yaml"
                        bat "kubectl apply -f kubernetes/service.yaml"

                        // Update deployment with new image
                        bat "kubectl set image deployment/${APP_NAME} ${APP_NAME}=${DOCKER_IMAGE}"

                        // Check deployment status
                        bat "kubectl rollout status deployment/${APP_NAME}"
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