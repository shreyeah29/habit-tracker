pipeline {
    agent any

    environment {
        DOCKER_HUB = 'shreyeah29/habit-tracker'
        DOCKER_CRED = credentials('dockerhub-cred')
        KUBE_CRED = credentials('kubeconfig')
    }

    stages {

        stage('Checkout Code') {
            steps {
                echo '📦 Checking out code from GitHub...'
                git branch: 'main', url: 'https://github.com/shreyeah29/habit-tracker.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '🐳 Building Docker image...'
                sh 'docker build -t $DOCKER_HUB:latest .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo '⬆️ Pushing image to Docker Hub...'
                sh '''
                echo $DOCKER_CRED_PSW | docker login -u $DOCKER_CRED_USR --password-stdin
                docker push $DOCKER_HUB:latest
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo '🚀 Deploying to Kubernetes...'
                writeFile file: 'kubeconfig', text: "${KUBE_CRED}"
                sh '''
                export KUBECONFIG=kubeconfig
                kubectl apply -f k8s/deployment.yaml
                kubectl apply -f k8s/service.yaml
                '''
            }
        }
    }

    post {
        success {
            echo '✅ CI/CD pipeline executed successfully! App is live on Kubernetes.'
        }
        failure {
            echo '❌ Pipeline failed. Check console logs for details.'
        }
    }
}
