from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Protocol.KDF import scrypt




def encrypt_text(text, key):
    data = text.encode('utf-8')
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    iv = cipher.iv
    
    return ct_bytes, iv

def decrypt_text(ct, iv, key):
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)

    return pt.decode('utf-8')

# Generar una clave aleatoria
password = "password"
aes_key  = password.ljust(AES.block_size, "\0").encode()
if len(password) > AES.block_size:
    aes_key = password[:AES.block_size].encode()

key = aes_key
# Texto plano a encriptar
text = "jaume primeque sexy "

# Encriptar el texto plano
ct, iv = encrypt_text(text, key)

print("Texto encriptado:", ct)
print("Vector de inicialización (IV):", iv)

# Desencriptar el texto encriptado
pt = decrypt_text(ct, iv, key)

print("Texto desencriptado:", pt)