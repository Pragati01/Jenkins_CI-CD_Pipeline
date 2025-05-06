# 🛠 Titanic Data ETL Pipeline with Jenkins CI/CD

This project demonstrates a complete CI/CD pipeline using **Jenkins**, **GitHub**, and **PostgreSQL** to automate a simple ETL process for Titanic passenger data.

---

## 📌 Project Overview

- 🐘 Source: Titanic dataset from a public GitHub repo
- 🐍 ETL Script: Python (pandas + SQLAlchemy + psycopg2)
- 🛠 CI/CD: Jenkins Pipeline (Declarative)
- 🔐 Secure credentials using Jenkins credentials store
- 🗄 Target: PostgreSQL database
- 🌐 Repo: GitHub

---

## ✅ What This Pipeline Does

1. Jenkins watches the GitHub repository.
2. When manually triggered (or via a future webhook), Jenkins:
   - Pulls the latest code
   - Installs Python dependencies
   - Runs a Python ETL script
   - Loads Titanic data into a PostgreSQL table

---

## 📁 Project Structure

```
jenkins-etl-pipeline/
├── etl/
│   └── titanic_csv_to_postgres.py
├── requirements.txt
├── Jenkinsfile
└── README.md
```

---

## 🚀 Step-by-Step Setup Guide

### 1. Prepare PostgreSQL Database
- Create a database locally or use a free hosted service like [ElephantSQL](https://www.elephantsql.com/)
- Note your host, port, DB name, username, and password

---

### 2. Securely Store Credentials in Jenkins

1. Go to **Jenkins Dashboard → Manage Jenkins → Credentials → (Global) → Add Credentials**
2. Choose **“Secret text”**
3. Add the following (use exact IDs):
   - `DB_USER`
   - `DB_PASS`
   - `DB_HOST`
   - `DB_NAME`

These will be securely injected into your Jenkins pipeline and accessed by your Python script using environment variables.

---

### 3. Clone & Set Up the Repo

Push the following structure to GitHub.

#### 🔹 Jenkinsfile

```groovy
pipeline {
    agent any

    environment {
        DB_USER = credentials('DB_USER')
        DB_PASS = credentials('DB_PASS')
        DB_HOST = credentials('DB_HOST')
        DB_NAME = credentials('DB_NAME')
        DB_PORT = '5432'
    }

    stages {
        stage('Install Dependencies') {
            steps {
                sh 'python3 -m pip install --upgrade pip'
                sh 'python3 -m pip install --only-binary :all: psycopg2-binary'
                sh 'python3 -m pip install -r requirements.txt'
            }
        }

        stage('Run ETL Script') {
            steps {
                sh 'python3 etl/titanic_csv_to_postgres.py'
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
```

#### 🔹 requirements.txt

```
psycopg2-binary
pandas
sqlalchemy
```

#### 🔹 etl/titanic_csv_to_postgres.py

```python
import os
import pandas as pd
from sqlalchemy import create_engine

url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)
df.columns = [col.strip().replace(" ", "_").lower() for col in df.columns]

# Securely fetch DB credentials from environment variables
db_user = os.environ.get("DB_USER")
db_pass = os.environ.get("DB_PASS")
db_host = os.environ.get("DB_HOST")
db_port = os.environ.get("DB_PORT", "5432")
db_name = os.environ.get("DB_NAME")

engine = create_engine(f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}')
df.to_sql('titanic_passengers', engine, if_exists='replace', index=False)
print("✅ Loaded Titanic data into PostgreSQL!")
```

---

### 4. Install Jenkins (macOS)

```bash
brew install jenkins-lts
brew services start jenkins-lts
open http://localhost:8080
```

Use the password from:

```bash
sudo less /opt/homebrew/var/jenkins/secrets/initialAdminPassword
```

---

### 5. Create Jenkins Pipeline Job

- Go to **http://localhost:8080**
- Click **New Item → Pipeline**
- Enter name: `titanic-etl-pipeline`
- Select: **Pipeline script from SCM**
- SCM: Git
- Repo URL: `https://github.com/<your-username>/jenkins-etl-pipeline.git`
- Branch: `main`
- Script Path: `Jenkinsfile`
- Save

---

### 6. Build & Verify

- Click **Build Now**
- View **Console Output**
- If successful, log into PostgreSQL and run:

```sql
SELECT * FROM titanic_passengers LIMIT 5;
```

---

## 🧠 Optional Next Steps

- 🔁 Add GitHub webhook for auto-triggering
- 🐳 Dockerize the pipeline
- 📬 Add Slack/email notifications
- 🔎 Run SQL analytics on the loaded data

---

## 🙌 Credits

Built by [Your Name] using:
- [Jenkins](https://www.jenkins.io/)
- [pandas](https://pandas.pydata.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Titanic Dataset](https://github.com/datasciencedojo/datasets/blob/master/titanic.csv)
