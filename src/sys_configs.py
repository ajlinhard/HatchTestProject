
class Configs():

    # DATABASE_URL = 'postgresql://username:password@localhost/dbname'
    database = "HatchMsg"
    driver = "ODBC Driver 17 for SQL Server"
    server = 'localhost\\SQLEXPRESS' 
    DATABASE_URL = f"mssql://@{server}/{database}?driver={driver}&trusted_connection=yes"