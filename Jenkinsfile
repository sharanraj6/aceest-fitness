pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = "sharanraj67/aceest-fitness"
        DOCKER_TAG = "v${env.BUILD_ID}"
    }
    
    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                }
            }
        }
        
        stage('Test & Validation') {
            steps {
                // 1. Create the reports folder in the Jenkins workspace
                sh 'mkdir -p reports'
                
                // 2. Run a temporary Docker container, mount the reports folder, and execute pytest
                sh "docker run --rm -v ${env.WORKSPACE}/reports:/app/reports ${DOCKER_IMAGE}:${DOCKER_TAG} pytest test_app.py --junitxml=reports/result.xml"
            }
            post {
                always {
                    // 3. Jenkins collects the XML file created by the container
                    junit 'reports/*.xml'
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
