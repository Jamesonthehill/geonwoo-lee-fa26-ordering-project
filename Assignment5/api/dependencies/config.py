import os


class conf:
    host = os.getenv("DB_HOST", "localhost")
    database = os.getenv("DB_NAME", "sandwich_maker_api")
    port = int(os.getenv("DB_PORT", "3306"))
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "")
