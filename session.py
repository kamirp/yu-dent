# session.py

class Session:
    dcode: int = None
    dname: str = None
    accesslevel: int = None
    drights: int = None
    filial: int = None

    @classmethod
    def clear(cls):
        cls.dcode = None
        cls.dname = None
        cls.accesslevel = None
        cls.drights = None
        cls.filial = None
