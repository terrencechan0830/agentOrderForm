import pyodbc
import urllib.parse

driver = '{ODBC Driver 17 for SQL Server}'
server = 'agentorderform.database.windows.net'
database = 'agentorderform'
username = 'CloudSA914ad4ea'
password = 'Qa74ze7r!'
conn = f"""Driver={driver};Server=tcp:{server},1433;Database={database};
    Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=300;"""
params = urllib.parse.quote_plus(conn)
conn_str = 'mssql+pyodbc:///?autocommit=true&odbc_connect={}'.format(params)

class Config:
    SECRET_KEY = "a016fd36023663c0ed583e6c65ae902e"
    SQLALCHEMY_DATABASE_URI = conn_str
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "no-reply@hkmakeupshop.com"
    MAIL_PASSWORD = "Lwy@0830"