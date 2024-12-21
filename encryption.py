from cryptography.fernet import Fernet

# Генерация ключа (выполняется 1 раз)
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# Загрузка ключа
def load_key():
    with open("secret.key", "rb") as key_file:
        return key_file.read()

# Шифрование сообщения
def encrypt_message(message):
    key = load_key()
    fernet = Fernet(key)
    return fernet.encrypt(message.encode())

# Дешифрование сообщения
def decrypt_message(encrypted_message):
    key = load_key()
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_message).decode()
