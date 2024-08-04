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
        
        stage('Deploy to Kubernetes') {
            steps {
                script {
                    // Write kubeconfig to a file
                    writeFile file: 'kubeconfig', text: KUBECONFIG

                    // Update the deployment YAML with the new image
                    sh """
                        sed -i 's|image: .*|image: ${DOCKER_IMAGE}|' kubernetes/deployment.yaml
                    """

                    // Apply the Kubernetes configurations
                    sh """
                        kubectl --kubeconfig=kubeconfig apply -f kubernetes/deployment.yaml
                        kubectl --kubeconfig=kubeconfig apply -f kubernetes/service.yaml
                    """
                }
            }
        }
    }
    
    post {
        always {
            sh 'docker logout'
            sh 'rm -f kubeconfig'
        }
    }
}