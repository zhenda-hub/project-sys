from pathlib import Path
from datetime import datetime

from cryptography.fernet import Fernet, MultiFernet


def generate_key(folder: str, key_name: str):
    """

    :return: address of key file with date
    """
    key = Fernet.generate_key()
    # breakpoint()

    cur_path = Path(folder)
    cur_path.mkdir(parents=True, exist_ok=True)

    date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    key_file = cur_path / f'{key_name}_{date}.key'

    key_file.write_bytes(key)
    print(f'key_file: {str(key_file)}')
    return str(key_file)


def load_key(key_file: str):
    """

    :param key_file:
    :return:
    """
    return Path(key_file).read_bytes()


def encrypt(key_file: str, file: str):
    """
    直接对file加密
    :param key_file:
    :param file:
    :return:
    """
    key = load_key(key_file)

    fernet = Fernet(key)

    with open(file, 'rb') as f:
        data = f.read()

    encrypted_data = fernet.encrypt(data)

    with open(file, 'wb') as f:
        f.write(encrypted_data)


def decrypt(key_file: str, file: str):
    """
    直接对file解密
    :param key_file:
    :param file:
    :return:
    """
    key = load_key(key_file)

    fernet = Fernet(key)

    with open(file, 'rb') as f:
        data = f.read()

    decrypted_data = fernet.decrypt(data)

    with open(file, 'wb') as f:
        f.write(decrypted_data)

    return file


def encrypt_fold(key_file: str, folder: str):
    # breakpoint()
    for file in Path(folder).rglob('*'):
        if file.is_file():
            encrypt(key_file, str(file))


def decrypt_fold(key_file: str, folder: str):
    for file in Path(folder).rglob('*'):
        if file.is_file():
            decrypt(key_file, str(file))


if __name__ == '__main__':
    # key_file = generate_key('./keys', 'pj_sys')

    # encrypt('keys\pj_sys_2023-08-16-12-45-43.key', 'dbback/db2-3-4.json')
    # decrypt('keys\pj_sys_2023-08-16-12-45-43.key', 'dbback/db2-3-4.json')

    encrypt_fold('keys\pj_sys_2023-08-16-12-45-43.key', 'dbback')
    # decrypt_fold('keys\pj_sys_2023-08-16-12-45-43.key', 'dbback')
