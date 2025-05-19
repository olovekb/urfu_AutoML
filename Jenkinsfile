pipeline {
  // Используем Docker-агент: внутри контейнера будет Linux + Python 3.9
  agent {
    docker {
      image 'python:3.9-slim'
      args  '-v /var/run/docker.sock:/var/run/docker.sock' // если нужен Docker внутри контейнера
    }
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
        // Стандартный checkout вашего репо
        checkout([
          $class: 'GitSCM',
          branches: [[name: '*/FinalTask-back']],
          userRemoteConfigs: [[url: 'https://github.com/olovekb/urfu_AutoML.git']]
        ])
      }
    }

    stage('Setup Env & DVC') {
      steps {
        sh '''
          python3 -m venv venv
          . venv/bin/activate
          pip install --upgrade pip
          # Устанавливаем зависимости и инструменты
          pip install -r requirements.txt \
                      dvc[gdrive] \
                      pytest
          # Не устанавливаем GE пока — он тяжелый и ломается на Windows,
          # но под Linux пойдет нормально. Можно раскомментировать:
          # pip install great_expectations
          dvc remote modify ${DVC_REMOTE} gdrive_use_service_account true
          dvc remote modify ${DVC_REMOTE} gdrive_service_account_json_file_path $GDRIVE_KEY
        '''
      }
    }

    stage('DVC Pull') {
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
          dvc add data/train/train_data.csv data/test/test_data.csv
        '''
      }
    }

    stage('Preprocess & Track Data') {
      steps {
        sh '''
          . venv/bin/activate
          python src/data_preprocessing.py
          dvc add data/train/train_data_scaled.csv data/test/test_data_scaled.csv
        '''
      }
    }

    stage('Data Quality Checks') {
      steps {
        sh '''
          . venv/bin/activate
          # Если нужно — установите и запустите GE:
          # pip install great_expectations
          # great_expectations checkpoint run default
        '''
      }
    }

    stage('Unit & Data Tests') {
      steps {
        sh '''
          . venv/bin/activate
          pytest --junitxml=reports/junit.xml
        '''
      }
    }

    stage('Push Data') {
      steps {
        sh '''
          . venv/bin/activate
          dvc push -r ${DVC_REMOTE}
        '''
      }
    }

    stage('Build & Push Docker') {
      steps {
        sh '''
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
      archiveArtifacts artifacts: 'reports/**/*.xml', allowEmptyArchive: true
      junit 'reports/junit.xml'
    }
    success {
      echo '✅ Pipeline succeeded'
    }
    failure {
      echo '❌ Pipeline failed, check log'
    }
  }
}
