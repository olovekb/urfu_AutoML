pipeline {
  agent any

  environment {
    // Имя DVC-remote из .dvc/config
    DVC_REMOTE      = 'storage'
    // Docker registry и имя образа
    DOCKER_REGISTRY = 'registry.example.com'
    IMAGE_NAME      = "${DOCKER_REGISTRY}/urfu-automl-app"
    // Jenkins-credential типа “Secret file” с вашим ключом
    GDRIVE_KEY      = credentials('gdrive-service-account-json')
  }

  stages {
    stage('Checkout') {
      steps {
        checkout([
          $class: 'GitSCM',
          branches: [[name: '*/FinalTask-back']],
          userRemoteConfigs: [[
            url: 'https://github.com/olovekb/urfu_AutoML.git'
          ]]
        ])
      }
    }

    stage('Setup Python & DVC') {
      steps {
        bat """
          python -m venv venv
          call venv\\Scripts\\activate
          pip install --upgrade pip
          pip install -r requirements.txt dvc[gdrive] great_expectations pytest
          REM Настроим DVC remote для работы через сервис-аккаунт GDrive
          dvc remote modify %DVC_REMOTE% gdrive_use_service_account true
          dvc remote modify %DVC_REMOTE% gdrive_service_account_json_file_path %GDRIVE_KEY%
        """
      }
    }

    stage('DVC Pull Data') {
      steps {
        bat """
          call venv\\Scripts\\activate
          dvc pull -r %DVC_REMOTE%
        """
      }
    }

    stage('Generate & Track Raw Data') {
      steps {
        bat """
          call venv\\Scripts\\activate
          python src\\data_creation.py
          REM после генерации raw-файлов отслеживаем их DVC
          dvc add data\\train\\train_data.csv data\\test\\test_data.csv
        """
      }
    }

    stage('Preprocess & Track Processed Data') {
      steps {
        bat """
          call venv\\Scripts\\activate
          python src\\data_preprocessing.py
          REM теперь отслеживаем масштабированные данные
          dvc add data\\train\\train_data_scaled.csv data\\test\\test_data_scaled.csv
        """
      }
    }

    stage('Data Quality Checks') {
      steps {
        bat """
          call venv\\Scripts\\activate
          REM проверяем качество данных через Great Expectations
          great_expectations checkpoint run default
        """
      }
    }

    stage('Unit & Data Tests') {
      steps {
        bat """
          call venv\\Scripts\\activate
          pytest  REM запустит все тесты из папки tests/
        """
      }
    }

    stage('Push Data to Remote') {
      steps {
        bat """
          call venv\\Scripts\\activate
          dvc push -r %DVC_REMOTE%
        """
      }
    }

    stage('Build & Push Docker Image') {
      steps {
        bat """
          REM Собираем образ (если ваш Dockerfile не использует venv-папку, можно убрать --build-arg)
          docker build --build-arg VENV_DIR=venv -t %IMAGE_NAME%:%BUILD_NUMBER% .
          docker push %IMAGE_NAME%:%BUILD_NUMBER%
        """
      }
    }
  }

  post {
    always {
      archiveArtifacts artifacts: 'reports/**/*.xml, coverage/**', allowEmptyArchive: true
      junit 'reports/**/*.xml'
    }
    success {
      echo 'Pipeline completed successfully.'
    }
    failure {
      echo 'Pipeline failed. Check the logs above.'
    }
  }
}
