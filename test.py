import pandas as pd
from sqlalchemy import create_engine
engine = create_engine('sqlite:///data/fraud_detector.db')
df = pd.read_sql("SELECT lat, lon FROM transactions ORDER BY timestamp DESC LIMIT 10", engine)
print(df)
