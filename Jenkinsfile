pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                // Получаем код из репозитория
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[url: 'https://github.com/olovekb/urfu_AutoML.git']]
                ])
            }
        }
        stage('Install Dependencies') {
            steps {
                // Создаем виртуальное окружение и устанавливаем зависимости
                bat 'python -m venv venv'
                bat 'venv\\Scripts\\pip install -r requirements.txt'
            }
        }
        stage('Run Tests') {
            steps {
                // Запускаем тесты (если они имеются)
                bat 'venv\\Scripts\\pytest'
            }
        }
    }
}
