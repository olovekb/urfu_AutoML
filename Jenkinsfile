pipeline {
  // Переключаемся на Windows-нод с коротким путем рабочего каталога
  agent {
    label 'windows'
    // Папка на корне диска, чтобы избежать длинных путей
    customWorkspace 'C:\\jenkins_ws\\URFU_AutoML'
  }

  environment {
    DVC_REMOTE      = 'storage'
    DOCKER_REGISTRY = 'registry.example.com'
    IMAGE_NAME      = "${DOCKER_REGISTRY}/urfu-automl-app"
    GDRIVE_KEY      = credentials('gdrive-service-account-json')
  }

  stages {
    stage('Checkout') {
      steps {
        // Клонируем нужную ветку в короткую папку
        checkout([
          $class: 'GitSCM',
          branches: [[name: '*/FinalTask-back']],
          userRemoteConfigs: [[ url: 'https://github.com/olovekb/urfu_AutoML.git' ]]
        ])
      }
    }

    stage('Setup Python & DVC') {
      steps {
        bat """
          REM создаём и активируем виртуальное окружение
          python -m venv venv
          call venv\\Scripts\\activate

          REM понижаем pip, чтобы Great Expectations ставился корректно
          pip install --upgrade pip==24.0

          REM ставим зависимости + DVC + pytest + фиксированную версию GE
          pip install -r requirements.txt dvc[gdrive] pytest
          pip install great_expectations==0.18.21

          REM настраиваем DVC для работы через сервис-аккаунт
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
          dvc add data\\train\\train_data.csv data\\test\\test_data.csv
        """
      }
    }

    stage('Preprocess & Track Processed Data') {
      steps {
        bat """
          call venv\\Scripts\\activate
          python src\\data_preprocessing.py
          dvc add data\\train\\train_data_scaled.csv data\\test\\test_data_scaled.csv
        """
      }
    }

    stage('Data Quality Checks') {
      steps {
        bat """
          call venv\\Scripts\\activate
          great_expectations checkpoint run default
        """
      }
    }

    stage('Unit & Data Tests') {
      steps {
        bat """
          call venv\\Scripts\\activate
          pytest --junitxml=reports\\junit.xml
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
          docker build --build-arg VENV_DIR=venv -t %IMAGE_NAME%:%BUILD_NUMBER% .
          docker push %IMAGE_NAME%:%BUILD_NUMBER%
        """
      }
    }
  }

  post {
    always {
      archiveArtifacts artifacts: 'reports/**/*.xml', allowEmptyArchive: true
      junit 'reports/junit.xml'
    }
    success {
      echo '✅ Pipeline succeeded'
    }
    failure {
      echo '❌ Pipeline failed—смотрите логи выше'
    }
  }
}
