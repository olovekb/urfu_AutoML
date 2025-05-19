pipeline {
  agent any

  environment {
    // Имя DVC-remote из .dvc/config
    DVC_REMOTE      = 'storage'
    // Docker registry и имя образа
    DOCKER_REGISTRY = 'registry.example.com'
    IMAGE_NAME      = "${DOCKER_REGISTRY}/urfu-automl-app"
    // Jenkins-credential типа “Secret file”, в который вы загрузили my-gdrive-sa.json
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
        sh '''
          python3 -m venv venv
          . venv/bin/activate
          pip install --upgrade pip
          pip install -r requirements.txt dvc[gdrive] great_expectations pytest
          # Настроим DVC remote для работы через сервис-аккаунт GDrive
          dvc remote modify ${DVC_REMOTE} gdrive_use_service_account true
          dvc remote modify ${DVC_REMOTE} gdrive_service_account_json_file_path $GDRIVE_KEY
        '''
      }
    }

    stage('DVC Pull Data') {
      steps {
        sh '''
          . venv/bin/activate
          dvc pull -r ${DVC_REMOTE}
        '''
      }
    }

    stage('Generate & Track Raw Data') {
      steps {
        sh '''
          . venv/bin/activate
          python src/data_creation.py
          # после генерации raw-файлов отслеживаем их DVC
          dvc add data/train/train_data.csv data/test/test_data.csv
        '''
      }
    }

    stage('Preprocess & Track Processed Data') {
      steps {
        sh '''
          . venv/bin/activate
          python src/data_preprocessing.py
          # теперь отслеживаем масштабированные данные
          dvc add data/train/train_data_scaled.csv data/test/test_data_scaled.csv
        '''
      }
    }

    stage('Data Quality Checks') {
      steps {
        sh '''
          . venv/bin/activate
          # проверяем качества данных через Great Expectations
          great_expectations checkpoint run default
        '''
      }
    }

    stage('Unit & Data Tests') {
      steps {
        sh '''
          . venv/bin/activate
          pytest  # запустит все тесты из папки tests/
        '''
      }
    }

    stage('Push Data to Remote') {
      steps {
        sh '''
          . venv/bin/activate
          dvc push -r ${DVC_REMOTE}
        '''
      }
    }

    stage('Build & Push Docker Image') {
      steps {
        sh '''
          # Собираем образ (если ваш Dockerfile не использует venv-папку,
          # можно убрать --build-arg)
          docker build \
            --build-arg VENV_DIR=venv \
            -t ${IMAGE_NAME}:${BUILD_NUMBER} .
          docker push ${IMAGE_NAME}:${BUILD_NUMBER}
        '''
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
