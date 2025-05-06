pipeline {
    agent any

    stages {
        stage('Clone Repo') {
            steps {
                git 'https://github.com/Pragati01/Jenkins_CI-CD_Pipeline.git'
            }
        }
        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Run ETL Script') {
            steps {
                sh 'python etl/titanic_csv_to_postgres.py'
            }
        }
    }

    post {
        success {
            echo '✅ ETL Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed. Check logs.'
        }
    }
}
