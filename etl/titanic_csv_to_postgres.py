import pandas as pd
import psycopg2
from sqlalchemy import create_engine

# New working public CSV dataset
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"

# Load CSV
df = pd.read_csv(url)
df.columns = [col.strip().replace(" ", "_").lower() for col in df.columns]  # Clean column names

conn_str = "postgresql://neondb_owner:npg_oNW2PG8Cfxgc@ep-floral-rice-a8rn0ap1-pooler.eastus2.azure.neon.tech/neondb?sslmode=require"

engine = create_engine(conn_str)


# Load into DB
df.to_sql('covid_cases_nyc', engine, if_exists='replace', index=False)
print("✅ Data loaded into PostgreSQL successfully!")
