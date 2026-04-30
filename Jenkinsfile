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
            environment {
                SCANNER_HOME = tool 'sonar-scanner'
            }
            steps {
                withCredentials([string(credentialsId: 'sonar-secret-token', variable: 'SONAR_TOKEN')]) {
                    withSonarQubeEnv('SonarQube-Server') {
                        sh "${SCANNER_HOME}/bin/sonar-scanner -Dsonar.projectKey=aceest-fitness -Dsonar.sources=. -Dsonar.login=${SONAR_TOKEN}"
                    }
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials-id', passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER')]) {
                    sh "echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin"
                    sh "docker push ${DOCKER_IMAGE}:${DOCKER_TAG}"
                }
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                
                sh "sed -i '' 's/latest/${DOCKER_TAG}/g' k8s-deployment.yaml"
                

                sh "kubectl apply -f k8s-deployment.yaml"
            }
        }
    }
}
