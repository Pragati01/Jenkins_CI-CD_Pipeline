import os
import pandas as pd
import psycopg2
from sqlalchemy import create_engine



# New working public CSV dataset
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"

# Load CSV
df = pd.read_csv(url)
df.columns = [col.strip().replace(" ", "_").lower() for col in df.columns]  # Clean column names


# Secure DB credentials from environment variables
db_user = os.environ.get("DB_USER")
db_pass = os.environ.get("DB_PASS")
db_host = os.environ.get("DB_HOST")
db_port = os.environ.get("DB_PORT", "5432")
db_name = os.environ.get("DB_NAME")

# SQLAlchemy engine
engine = create_engine(f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}')

#df.to_sql('titanic_passengers', engine, if_exists='replace', index=False)
#engine = create_engine(conn_str)


# Load into DB
df.to_sql('covid_cases_nyc', engine, if_exists='replace', index=False)
print("✅ Data loaded into PostgreSQL successfully!")
