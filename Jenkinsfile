pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')
        APP_NAME = "superhero-generator"
        DOCKER_IMAGE = "${DOCKERHUB_CREDENTIALS_USR}/${APP_NAME}:${BUILD_NUMBER}"
        KUBECONFIG = credentials('kubeconfig')
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
                    bat "docker build -t ${DOCKER_IMAGE} ."
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        bat "echo %DOCKER_PASSWORD% | docker login -u %DOCKER_USERNAME% --password-stdin"
                        bat "docker push ${DOCKER_IMAGE}"
                        bat "docker push ${DOCKERHUB_CREDENTIALS_USR}/${APP_NAME}:latest"
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    // Write kubeconfig to a file
                    writeFile file: 'kubeconfig', text: KUBECONFIG

                    // Update the deployment YAML with the new image
                    bat "powershell -Command \"(Get-Content kubernetes\\deployment.yaml) -replace 'image: .*', 'image: ${DOCKER_IMAGE}' | Set-Content kubernetes\\deployment.yaml\""

                    // Apply the Kubernetes configurations
                    bat "kubectl --kubeconfig=kubeconfig apply -f kubernetes\\deployment.yaml"
                    bat "kubectl --kubeconfig=kubeconfig apply -f kubernetes\\service.yaml"
                }
            }
        }
    }

    post {
        always {
            // Clean up resources
            script {
                bat "docker logout"
                bat "del kubeconfig"
            }
        }
    }
}
