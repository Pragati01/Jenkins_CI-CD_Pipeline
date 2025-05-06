pipeline {
    agent any

    stages {
        
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
