from flask import Flask, render_template, request, send_file
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from datetime import datetime
import os

def generate_aes_key():
    """Generates a new AES key."""
    return Fernet.generate_key()

def generate_rsa_keys():
    """Generates RSA key pair."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    return private_key, public_key

app = Flask(__name__)

# AES Setup
encryption_key = generate_aes_key()
cipher = Fernet(encryption_key)

# RSA Setup
rsa_private_key, rsa_public_key = generate_rsa_keys()

@app.route('/', methods=['GET', 'POST'])
def home():
    output = ""
    error = ""
    if request.method == 'POST':
        action = request.form.get('action')
        user_input = request.form.get('text')
        uploaded_files = request.files.getlist('file')

        try:
            if action == 'encrypt' and user_input:
                encrypted = cipher.encrypt(user_input.encode())
                # Format the output for readability
                output = "\n".join([encrypted[i:i+64].decode() for i in range(0, len(encrypted), 64)])
            elif action == 'decrypt' and user_input:
                decrypted = cipher.decrypt(user_input.encode())
                output = decrypted.decode()
            elif action == 'encrypt' and uploaded_files:
                file_outputs = []
                for file in uploaded_files:
                    file_content = file.read()
                    encrypted_content = cipher.encrypt(file_content)
                    metadata = f"Encrypted on {datetime.now()}\n".encode()
                    filename = f"{file.filename}.enc"
                    with open(filename, 'wb') as f:
                        f.write(metadata + encrypted_content)
                    file_outputs.append(filename)
                output = f"Encrypted files: {', '.join(file_outputs)}"
            elif action == 'rsa_encrypt' and user_input:
                encrypted = rsa_public_key.encrypt(
                    user_input.encode(),
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                # Format the output for readability
                output = "\n".join([encrypted.hex()[i:i+64] for i in range(0, len(encrypted.hex()), 64)])
            elif action == 'rsa_decrypt' and user_input:
                encrypted_bytes = bytes.fromhex(user_input)
                decrypted = rsa_private_key.decrypt(
                    encrypted_bytes,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                output = decrypted.decode()
        except Exception as e:
            error = f"Error: {str(e)}"

    return render_template('index.html', output=output, error=error)

@app.route('/key', methods=['GET'])
def get_key():
    """Endpoint to retrieve the current AES encryption key."""
    return encryption_key.decode()

if __name__ == '__main__':
    # For local development, set debug mode to True
    app.run(host='0.0.0.0', port=8080, debug=True)
