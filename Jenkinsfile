pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')
        APP_NAME = "superhero-generator"
        DOCKER_IMAGE = "${DOCKERHUB_CREDENTIALS_USR}/${APP_NAME}:${BUILD_NUMBER}"
        AWS_CREDENTIALS = credentials('aws-creds')
        KUBECONFIG = credentials('kubeconfig')
        CLUSTER_NAME = "superherogen_cluster"
        AWS_REGION = "us-east-2"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Lint Python Code') {
            steps {
                script {
                    bat 'python -m venv venv'
                    bat 'venv\\Scripts\\activate.bat && pip install flake8'
                    bat 'venv\\Scripts\\activate.bat && flake8 app.py --max-line-length=100 --statistics'
                }
            }
        }

        stage('Install Dependencies and Run App') {
            steps {
                script {
                    bat 'venv\\Scripts\\activate.bat && pip install -r requirements.txt'
                    bat 'start /B venv\\Scripts\\activate.bat && python app.py'
                    bat 'timeout /t 10'  // Wait for the app to start
                    bat 'curl http://localhost:5000'  // Test if the app is running
                    bat 'taskkill /F /IM python.exe'  // Stop the Flask app
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
                    bat "docker run -d --name ${APP_NAME}-test -p 5000:5000 ${DOCKER_IMAGE}"
                    bat 'timeout /t 10'
                    bat 'curl http://localhost:5000'
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
                        bat 'aws configure set aws_access_key_id %AWS_ACCESS_KEY_ID%'
                        bat 'aws configure set aws_secret_access_key %AWS_SECRET_ACCESS_KEY%'
                        bat "aws configure set region ${AWS_REGION}"
                        bat "aws eks get-token --cluster-name ${CLUSTER_NAME} > temp_token.json"
                        bat "aws eks update-kubeconfig --name ${CLUSTER_NAME} --region ${AWS_REGION}"
                        bat "kubectl apply -f kubernetes/deployment.yaml"
                        bat "kubectl apply -f kubernetes/service.yaml"
                        bat "kubectl set image deployment/${APP_NAME} ${APP_NAME}=${DOCKER_IMAGE}"
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
                bat "if exist temp_token.json del temp_token.json"
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