pipeline {
    agent any

    options {
        disableConcurrentBuilds()
        timestamps()
    }

    environment {
        IMAGE_NAME = 'assignment3-site'
        STAGING_PORT = '8091'
        PROD_PORT = '8082'
        STAGING_CONTAINER = 'assignment3-staging'
        PROD_CONTAINER = 'assignment3-prod'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'test -f index.html && test -f tests/test_site.py'
            }
        }

        stage('Package') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .'
            }
        }

        stage('Start Staging') {
            steps {
                sh '''
                    docker rm -f "$STAGING_CONTAINER" 2>/dev/null || true
                    docker run -d --name "$STAGING_CONTAINER" \
                      -p 127.0.0.1:${STAGING_PORT}:80 "${IMAGE_NAME}:${BUILD_NUMBER}"
                    for i in 1 2 3 4 5; do
                      if curl -fsS "http://127.0.0.1:${STAGING_PORT}/" >/dev/null; then
                        exit 0
                      fi
                      sleep 2
                    done
                    echo 'Staging site did not become ready' >&2
                    exit 1
                '''
            }
        }

        stage('Test') {
            agent {
                dockerfile {
                    dir 'tests'
                    args '--network host'
                    reuseNode true
                }
            }
            environment {
                HOME = '/tmp'
                BASE_URL = 'http://127.0.0.1:8091'
            }
            steps {
                sh 'pytest tests/test_site.py -v --junitxml=test-results.xml'
            }
            post {
                always {
                    junit testResults: 'test-results.xml', allowEmptyResults: true
                    archiveArtifacts artifacts: 'screenshot.png', allowEmptyArchive: true
                }
            }
        }

        stage('Deploy') {
            steps {
                echo 'All Selenium tests passed; deploying on port 8082.'
                sh '''
                    docker rm -f "$PROD_CONTAINER" 2>/dev/null || true
                    docker run -d --name "$PROD_CONTAINER" \
                      --restart unless-stopped \
                      -p ${PROD_PORT}:80 "${IMAGE_NAME}:${BUILD_NUMBER}"
                      sleep 5
                    curl -fsS "http://127.0.0.1:${PROD_PORT}/" >/dev/null
                '''
            }
        }
    }

    post {
        always {
            sh 'docker rm -f assignment3-staging 2>/dev/null || true'
        }
        success {
            echo "Assignment 3 build ${BUILD_NUMBER} deployed successfully."
        }
        failure {
            echo "Assignment 3 build ${BUILD_NUMBER} failed; no new version deployed by this run."
        }
    }
}
