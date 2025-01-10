from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Random import get_random_bytes
 
def encrypt_message(key, plaintext):
    iv = get_random_bytes(16)  # Generate a random IV
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    return iv + ciphertext  # Concat IV and encrypted text to send

# Function to encrypt a message
def key_adjust(key):
    key = key.ljust(16, b'\0') 
    return key
    

# Function to decipher a message
def decrypt_message(key, ciphertext):
    iv = ciphertext[:16]  # Extract the IV (16 bytes)
    encrypted_data = ciphertext[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    return plaintext.decode()

 
 
key = b'supersecretkey'  # Fill up to 16 bytes 13 bytes
key = key.ljust(16, b'\0') 

 
if __name__ == "__main__":
    message = "AixoEsUnaProva"
    print(f"Mensaje original: {message}")
    
    # Encrypt the message
    encrypted = encrypt_message(key, message)
    print(f"Mensaje cifrado: {encrypted.hex()}")  # Display in hexadecimal format
 
    print(type(encrypted))
    
    # Decrypt the message
    decrypted = decrypt_message(key, encrypted)
    print(f"Mensaje descifrado: {decrypted}")