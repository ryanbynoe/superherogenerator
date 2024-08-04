pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')
        APP_NAME = "superhero-generator"
        DOCKER_IMAGE = "${DOCKERHUB_CREDENTIALS_USR}/${APP_NAME}:${BUILD_NUMBER}"
        AWS_CREDENTIALS = credentials('aws-creds')
        KUBECONFIG = credentials('kubeconfig')
        CLUSTER_NAME = "superherogen_cluster"
        AWS_REGION = "us-east-2"  // Replace with your AWS region
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build and Test Python App') {
            steps {
                script {
                    // Create and activate virtual environment
                    bat 'python -m venv venv'
                    bat 'venv\\Scripts\\activate.bat && python -m pip install --upgrade pip'

                    // Install dependencies from requirements.txt
                    bat 'venv\\Scripts\\activate.bat && pip install -r requirements.txt'

                    // Install pytest and flake8
                    bat 'venv\\Scripts\\activate.bat && pip install pytest flake8'

                    // Lint the Python code
                    bat 'venv\\Scripts\\activate.bat && flake8 app.py'

                    // Run unit tests (if any)
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

        stage('Test Docker Image') {
            steps {
                script {
                    // Run the Docker container
                    bat "docker run -d --name ${APP_NAME}-test -p 5000:5000 ${DOCKER_IMAGE}"
                    
                    // Wait for the app to start
                    bat 'timeout /t 10'

                    // Test if the app is running
                    bat 'curl http://localhost:5000'

                    // Stop and remove the container
                    bat "docker stop ${APP_NAME}-test"
                    bat "docker rm ${APP_NAME}-test"
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