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
                    bat 'start /B cmd /c "venv\\Scripts\\activate.bat && python app.py > flask.log 2>&1"'
                    
                    // Wait for the Flask app to start (max 30 seconds)
                    def maxAttempts = 30
                    def isAppRunning = false
                    for (int i = 0; i < maxAttempts; i++) {
                        sleep 1
                        def status = bat(script: 'curl -s -o /dev/null -w "%{http_code}" http://localhost:5000', returnStatus: true)
                        if (status == 0) {
                            isAppRunning = true
                            break
                        }
                    }
                    
                    if (!isAppRunning) {
                        error "Flask app failed to start within 30 seconds"
                    }
                    
                    bat 'type flask.log'  // Display Flask app logs
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
                    sleep 10
                    bat 'curl http://localhost:5000 || echo Docker container is not responding'
                    bat "docker logs ${APP_NAME}-test"
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
                bat "taskkill /F /IM python.exe /T"
                bat "docker logout"
                bat "if exist temp_token.json del temp_token.json"
                bat "if exist flask.log del flask.log"
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