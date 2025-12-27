# db.py
import fdb

def get_connection():
    return fdb.connect(
        dsn="localhost:C:\\InfoclinicaData\\box_med.fdb",
        user="SYSDBA",
        password="masterkey",
        charset="UTF8"
    )
