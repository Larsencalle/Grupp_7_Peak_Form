import psycopg2
import configparser

def get_db_connection():
    """Skapar och returnerar en koppling till databasen med hjälp av config.ini"""
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Försöker koppla upp mot databasen
    try:
        conn = psycopg2.connect(
            host=config['database']['host'],
            database=config['database']['database'],
            user=config['database']['user'],
            password=config['database']['password'],
            port=config['database']['port']
        )
        return conn
        
    except Exception as e:
        print(f"Kunde inte ansluta till databasen: {e}")
        return None