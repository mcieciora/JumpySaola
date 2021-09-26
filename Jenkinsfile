pipeline {
    parameters {
        booleanParam(name: 'RELOAD_CONFIGURATION', defaultValue: false, description: '')
        string(name: 'BUILD_VERSION', defaultValue: "1.0", description: 'Provide to-build app version')
        string(name: 'BRANCH', defaultValue: "master", description: 'Provide branch value e.g feature/new_feature')
        booleanParam(name: 'DOCKER_DEPLOY', defaultValue: true, description: 'Push built image to docker registry if true, else put it in development registry')
        string(name: 'DOCKER_REGISTRY', defaultValue: "mcieciora/jumpy_saola", description: 'Provide Docker registry name')
        string(name: 'DEVELOPMENT_REGISTRY', defaultValue: "localhost:5000/jumpy_saola", description: 'Provide dev-Docker registry name')
        string(name: 'GIT_REPOSITORY', defaultValue: "https://github.com/mcieciora/JumpySaola.git", description: 'Provide Git repository https url')
        string(name: 'PYTHON_VERSION', defaultValue: "python3.9", description: 'Provide Python version')
    }
    agent any
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
                sh 'git clone $GIT_REPOSITORY'
                sh 'cd JumpySaola'
                script {
                    if (params.BRANCH != "master") {
                        sh 'git checkout $BRANCH'
                    }
                }
            }
        }

        stage('Lint code') {
            steps {
                // sh 'find . -type f -name "*.py" | xargs $PYTHON_VERSION -m pylint --disable=C0114,C0115,C0116 --max-line-length=120'
            }
        }

        stage('Automated tests') {
            steps {
                sh "python3 -m pip install -r requirements.txt"
                // sh "python3 -m pytest automated_tests/"
            }
        }

        stage('Build image') {
            steps {
                script {
                    sh "docker build -t jumpy_saola:$BUILD_VERSION.$BUILD_NUMBER ."
                }
            }
        }

        stage('Test image') {
            steps {
                sh "docker run -d --name tested_image -p 8000:8000 jumpy_saola:$BUILD_VERSION.$BUILD_NUMBER"
                sh "sleep 60"
                sh "docker ps | grep 'tested_image'"
                sh "docker stop tested_image"
            }
        }

        stage('Deploy image') {
            steps {
                script {
                    if (params.DOCKER_DEPLOY) {
                        sh "pwd"
                    }
                    else {
                        sh "docker start registry"
                        sh "docker image tag jumpy_saola:$BUILD_VERSION.$BUILD_NUMBER $DEVELOPMENT_REGISTRY:$BUILD_VERSION.$BUILD_NUMBER"
                        sh "docker push $DEVELOPMENT_REGISTRY:$BUILD_VERSION.$BUILD_NUMBER"
                        sh "docker stop registry"
                    }
                }
            }
        }
    }
    post {
        always {
            cleanWs()
            sh "docker system prune -a -f"
        }
    }
}