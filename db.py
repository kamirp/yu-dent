# db.py
import fdb

def get_connection():
    return fdb.connect(
        dsn="192.168.201.138:/data/primak.a/box_med.fdb",
        user="SYSDBA",
        password="masterkey",
        charset="UTF8"
    )
