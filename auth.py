# auth.py
from db import get_connection


def get_users():
    con = get_connection()
    cur = con.cursor()
    cur.execute("""
        SELECT DCODE, DNAME
        FROM DOCTOR
        WHERE COALESCE(LOCKED, 0) = 0
          AND DNAME IS NOT NULL
          AND COALESCE(SYSTYPE, 0) = 0 
        ORDER BY DNAME
    """)
    users = cur.fetchall()
    con.close()
    return users


def check_password(dcode: int, password: str) -> bool:
    con = get_connection()
    cur = con.cursor()
    cur.execute("""
        SELECT DPASSWRD
        FROM DOCTOR
        WHERE DCODE = ?
    """, (dcode,))
    row = cur.fetchone()
    con.close()

    if not row:
        return False

    return (row[0] or "") == password

def load_user_session(dcode: int):
    con = get_connection()
    cur = con.cursor()
    cur.execute("""
        SELECT
            DNAME,
            ACCESSLEVEL,
            DRIGHTS,
            FILIAL
        FROM DOCTOR
        WHERE DCODE = ?
    """, (dcode,))
    row = cur.fetchone()
    con.close()

    if not row:
        return None

    return {
        "dname": row[0],
        "accesslevel": row[1],
        "drights": row[2],
        "filial": row[3],
    }
