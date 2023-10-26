import pyodbc
import pandas as pd
from camera import pred_query
import time

df = pd.read_excel("Dataset.xlsx", sheet_name=0, header=None)
pre = len(df)
df = df.dropna(axis=0)
post = len(df)
print(pre - post)

df = df.iloc[:10]


predizioni = []
for i, row in df.iterrows():
    query = row[0] + " " + row[2]
    p = pred_query(query)
    print(i, query, p)
    predizioni.append(p)
    time.sleep(2)

df["preds"] = predizioni
df.to_excel("predizioni.xlsx")
# server_name = "sql-dev-captureonebi02.database.windows.net"
# user = "aasdevcaptureonebi02"
# pw = "LM0xHJ!jMj4pLvCD!N3x"
# db = "EDW"
# connection_string = f"Driver={{ODBC Driver 18 for SQL Server}};Server={server_name};Database={db};UID={user};PWD={pw}"
# conn = pyodbc.connect(connection_string)
# cursor = conn.cursor()

# sql_query = "SELECT CameraBrand, Series  FROM [edw].[DimAppCameras];"
# cursor.execute(sql_query)
# for row in cursor.fetchall():
#     print(row)

# cursor.close()
# conn.close()
