pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = "sharanraj67/aceest-fitness"
        DOCKER_TAG = "v${env.BUILD_ID}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/sharanraj6/aceest-fitness.git'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                }
            }
        }
        
        stage('Test & Validation') {
            steps {
                script {
                    dockerImage.inside {
                        sh 'pip install -r requirements.txt'
                        sh 'pytest test_app.py --junitxml=reports/result.xml'
                    }
                }
            }
            post {
                always {
                    junit 'reports/result.xml'
                }
            }
        }
        
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube-Server') {
                    sh 'sonar-scanner -Dsonar.projectKey=aceest-fitness -Dsonar.sources=.'
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-credentials-id') {
                        dockerImage.push()
                        dockerImage.push('latest')
                    }
                }
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                sh 'sed -i "s/latest/${DOCKER_TAG}/g" k8s-deployment.yaml'
                sh 'kubectl apply -f k8s-deployment.yaml'
            }
        }
    }
}
