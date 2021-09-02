pipeline {
    parameters {
        booleanParam(name: 'RELOAD_CONFIGURATION', defaultValue: false, description: '')
        string(name: 'BUILD_VERSION', defaultValue: "1.0", description: 'Provide to-build app version')
        string(name: 'BRANCH', defaultValue: "master", description: 'Provide branch value')
        booleanParam(name: 'DOCKER_DEPLOY', defaultValue: true, description: 'Push built image to docker registry if true, else put it in development registry')
        string(name: 'DOCKER_REGISTRY', defaultValue: "mcieciora/jumpy_saola", description: 'Provide Docker registry name')
        string(name: 'DEVELOPMENT_REGISTRY', defaultValue: "", description: 'Provide dev-Docker registry name')
        string(name: 'GIT_REPOSITORY', defaultValue: "https://github.com/mcieciora/JumpySaola.git", description: 'Provide Git repository https url')
        string(name: 'PYTHON_VERSION', defaultValue: "python3.8", description: 'Provide Python version')
    }
   environment {
        registry = "$DOCKER_REGISTRY"
        registryCredential = 'dockerhub_id'
        dockerImage = ''
    }
    agent {
    node {
        label 'docker_build'
    }
}
    stages {
        stage('Reload configuration'){
            when {
                expression { params.RELOAD_CONFIGURATION }
            }
            steps {
                script {
                    currentBuild.result = 'ABORTED'
                    error('Stopping job.')
                }
            }
        }

        stage('Clone GIT repository') {
            steps {
                git branch: '$BRANCH', credentialsId: 'dockerhub_id', url: "$GIT_REPOSITORY"
            }
        }

        stage('Lint code') {
            steps {
                sh 'find . -type f -name "*.py" | xargs $PYTHON_VERSION -m pylint --disable=C0114,C0115,C0116'
            }
        }

        stage('Automated tests') {
            steps {
                sh "pytest automated_tests/*"
                sh "rm -rf automated_tests"
            }
        }

        stage('Build image') {
            steps {
                script {
                    dockerImage = docker.build registry + ":$BUILD_VERSION.$BUILD_NUMBER"
                }
            }
        }

        stage('Test image') {
            steps {
                sh "docker run -d --name tested_image -p 5000:5000 $registry:$BUILD_VERSION.$BUILD_NUMBER"
                sh "sleep 60"
                sh "docker ps | grep 'tested_image'"
                sh "docker stop tested_image"
            }
        }

        stage('Deploy image') {
            steps {
                script {
                    if ($DOCKER_DEPLOY) {
                        docker.withRegistry('', registryCredential ) {
                            dockerImage.push()
                        }
                    }
                }
            }
        }

        stage('Cleanup') {
            steps {
                sh "docker system prune -a -f"
            }
        }
    }
}