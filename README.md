# ACEest Fitness & Gym - DevOps CI/CD Pipeline
## Project Overview
This repository contains the end-to-end Continuous Integration and Continuous Delivery (CI/CD) implementation for ACEest Fitness & Gym.  

The project transitions a legacy Tkinter desktop application into a containerized REST API and Web Application using Flask. The CI/CD pipeline automates testing, code quality checks, containerization, and progressive deployment with zero-downtime rollbacks.  

### Tech Stack Utilized
Version Control: Git & GitHub  

Application Framework: Python Flask & SQLite

Testing: Pytest  

Code Quality: SonarQube  

Containerization: Docker & Docker Hub  

Orchestration: Kubernetes (Minikube)  

CI/CD Automation: Jenkins  

## Repository Structure
<pre>
aceest-fitness/
├── app.py                  # Core Flask application and database logic
├── templates/
│   └── index.html          # Web UI for the client registration portal
├── requirements.txt        # Python dependencies (Flask, Pytest)
├── test_app.py             # Automated unit tests for Pytest
├── Dockerfile              # Instructions to containerize the application
├── k8s-deployment.yaml     # Kubernetes manifests (Deployment & Service)
├── Jenkinsfile             # Declarative Jenkins CI/CD pipeline configuration
└── README.md               # Project documentation
</pre>
## Prerequisites
Before running this project, ensure the following are installed and configured:

Git
Python 3.9+
Docker Desktop (Signed into Docker Hub)
Minikube & kubectl
Jenkins Server (With Docker Pipeline and GitHub integration plugins)

## Step 1: Local Development & Testing
To run the application and tests locally before containerization:

Clone the repository:

Bash
git clone  https://github.com/sharanraj6/aceest-fitness.git
cd aceest-fitness
Create and activate a virtual environment:

Bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:

Bash
pip install -r requirements.txt


4. **Run Automated Tests:**
   Validate the application logic using Pytest.
   ```bash
   pytest test_app.py -v
Run the Application:

Bash
python app.py
Navigate to http://localhost:5000 in your web browser to view the ACEest Fitness Portal.

## Step 2: Docker Containerization
Package the application into an isolated container.  

Build the Docker Image:

Bash
docker build -t sharanraj67/aceest-fitness:latest .
Run the Container Locally:

Bash
docker run -d -p 5000:5000 --name aceest-app sharanraj67/aceest-fitness:latest
Verify: Open http://localhost:5000 in your browser. Once verified, stop the container:

Bash
docker stop aceest-app && docker rm aceest-app


---

## Step 3: Kubernetes Deployment (Minikube)
Deploy the containerized application to a local Kubernetes cluster.

1. **Start Minikube:**
   ```bash
   minikube start --driver=docker
Apply Kubernetes Manifests:
This deploys the pods and configures a LoadBalancer service.

Bash
kubectl apply -f k8s-deployment.yaml
Check Pod Status:
Ensure all 3 replicas are running successfully.

Bash
kubectl get pods
Access the Application:
Retrieve the live endpoint URL for the application.  

Bash
minikube service aceest-fitness-service --url
## Step 4: Jenkins CI/CD Automation
Configure Jenkins to automate the entire lifecycle.  

Add Docker Hub Credentials in Jenkins:

Go to Manage Jenkins > Credentials > System > Global credentials.

Add a Username with password credential.

Important: Set the ID exactly as dockerhub-credentials-id.

Create the Pipeline:

Create a new Jenkins Pipeline item named ACEest-Pipeline.

Under the Pipeline section, choose Pipeline script from SCM.

Select Git, provide your repository URL, and set the Script Path to Jenkinsfile.

Trigger the Build:

Click Build Now.

Jenkins will automatically pull the code, build the image, run tests, perform static analysis, push to Docker Hub, and deploy to Minikube.

## Step 5: Advanced Deployment & Rollback Strategy
This project implements a Rolling Update deployment strategy[cite: 1]. This ensures zero downtime during version upgrades.

To demonstrate rollback capabilities:

Introduce a breaking change to app.py and push it to GitHub.

Allow Jenkins to deploy the broken version.

Observe the deployment failure or pod instability (kubectl get pods).

Execute an instant rollback to the previous stable version:

Bash
kubectl rollout undo deployment/aceest-fitness-deployment

5. Verify the successful rollback:
   ```bash
   kubectl rollout status deployment/aceest-fitness-deployment


## Screenshots:
Web Interface:
<img width="800" height="800" alt="Screenshot 2026-05-01 at 00 37 23" src="https://github.com/user-attachments/assets/73c85409-3cd2-4e62-bea3-97af87874b28" />

Jenkins Pipeline:
Console Log:
<img width="800" height="800" alt="Screenshot 2026-05-01 at 01 05 47" src="https://github.com/user-attachments/assets/38ea7834-e1dc-4f6b-863b-0090b99d6f5c" />

Full Console Log Text: [Jenkins-Succesful_pipelin.txt](https://github.com/user-attachments/files/27258860/Jenkins-Succesful_pipelin.txt)

Running Locally Minikube:
<img width="800" height="450" alt="Screenshot 2026-05-01 at 01 06 26" src="https://github.com/user-attachments/assets/251ab90b-605f-48ab-a8c5-e92510873aab" />

Containers:
<img width="800" height="800" alt="Screenshot 2026-05-01 at 01 06 37" src="https://github.com/user-attachments/assets/f3c159c1-5783-46be-9fcb-37899af0b2bb" />


