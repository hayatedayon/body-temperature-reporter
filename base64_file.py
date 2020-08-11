import base64
import os.path

FILE_PATH = 'p'

def get_password_path(filename: str) -> str:
    return os.path.join(os.path.dirname(__file__), filename)

def exist_password_file() -> bool:
    return os.path.exists(get_password_path(FILE_PATH))

def get_password() -> str:
    p = ''
    with open(get_password_path(FILE_PATH)) as rf:
        p = rf.read()
    return base64.b64decode(p).decode()
