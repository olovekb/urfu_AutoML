pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[url: 'https://github.com/olovekb/urfu_AutoML.git']]
                ])
            }
        }
        stage('Install Dependencies') {
            steps {
                // Создаём виртуальное окружение и устанавливаем зависимости
                bat 'python -m venv venv'
                bat 'venv\\Scripts\\pip install --upgrade pip'
                bat 'venv\\Scripts\\pip install -r requirements.txt'
            }
        }
        stage('Run data_creation.py') {
            steps {
                bat 'venv\\Scripts\\python lab1\\data_creation.py'
            }
        }
        stage('Run data_preprocessing.py') {
            steps {
                bat 'venv\\Scripts\\python lab1\\data_preprocessing.py'
            }
        }
        stage('Run model_preparation.py') {
            steps {
                bat 'venv\\Scripts\\python lab1\\model_preparation.py'
            }
        }
        stage('Run model_testing.py') {
            steps {
                bat 'venv\\Scripts\\python lab1\\model_testing.py'
            }
        }
    }
}
