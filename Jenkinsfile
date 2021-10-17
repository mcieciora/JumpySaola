pipeline {
    parameters {
        booleanParam(name: 'RELOAD_CONFIGURATION', defaultValue: false, description: '')
        string(name: 'BUILD_VERSION', defaultValue: "1.0", description: 'Provide to-build app version')
        string(name: 'BRANCH', defaultValue: "master", description: 'Provide branch value e.g feature/new_feature')
        choice(name: 'IMAGE_DEPLOY', choices: ['NO', 'DOCKER', 'REGISTRY'])
        string(name: 'DOCKER_REGISTRY', defaultValue: "mcieciora/jumpy_saola", description: 'Provide Docker registry name')
        string(name: 'DEVELOPMENT_REGISTRY', defaultValue: "localhost:5000/jumpy_saola", description: 'Provide dev-Docker registry name')
        string(name: 'GIT_REPOSITORY', defaultValue: "https://github.com/mcieciora/JumpySaola.git", description: 'Provide Git repository https url')
        string(name: 'PYTHON_VERSION', defaultValue: "python3.9", description: 'Provide Python version')
        booleanParam(name: 'VERBOSE', defaultValue: true, description: 'Print more logs during testing stage if true')
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

        stage('Checkout branch') {
            steps {
                script {
                    if (params.BRANCH != "master") {
                        sh 'git checkout $BRANCH'
                    }
                }
            }
        }

        stage('Lint code') {
            steps {
                sh '$PYTHON_VERSION -m pycodestyle --filename=*.py --max-line-length=120 .'
            }
        }

        stage('Automated tests') {
            steps {
                sh '$PYTHON_VERSION -m pip install -r requirements.txt'
                script {
                    if (params.VERBOSE) {
                        sh '$PYTHON_VERSION -m pytest automated_tests/ --log-cli-level=10'
                    }
                    else {
                        sh '$PYTHON_VERSION -m pytest automated_tests/'
                    }
                }

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
                sh "docker build -t selenium_tests:latest automated_selenium/Dockerfile"
                sh "docker run -d --name tested_image selenium_tests:latest"
                sh "docker stop tested_image"
            }
        }

        stage('Deploy image') {
            steps {
                script {
                    if (params.IMAGE_DEPLOY == "DOCKER") {
                        sh "docker image tag jumpy_saola:$BUILD_VERSION.$BUILD_NUMBER $DOCKER_REGISTRY:$BUILD_VERSION.$BUILD_NUMBER"
                        sh "docker push $DOCKER_REGISTRY:$BUILD_VERSION.$BUILD_NUMBER"
                    }
                    if (params.IMAGE_DEPLOY == "REGISTRY") {
                        sh "docker run -d -p 5000:5000 --restart=always --name registry -v /mnt/registry:/var/lib/registry registry:2"
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
            script{
                sh 'docker system prune -af'
            }
        }
    }
}