import sys
import random
from pathlib import Path
from vigenere_cipher import VigenereCipher
import string

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

ALPHABET = string.ascii_lowercase


# -------------------------------------------------
# UI
# -------------------------------------------------

def print_banner():
    print("\n" + "=" * 60)
    print("  VIGENERE CIPHER - Verschlüsselungsmittel mit Fake-Zeichen")
    print("=" * 60 + "\n")


def print_menu():
    print("\nWählen Sie eine Option:")
    print("1. Text verschlüsseln")
    print("2. Text entschlüsseln")
    print("3. Batch-Datei verarbeiten")
    print("4. Informationen anzeigen")
    print("5. Programmende")
    print("-" * 40)


# -------------------------------------------------
# Code-Validierung
# -------------------------------------------------

def validate_code(code: str) -> bool:
    if not code.isdigit():
        return False
    digits = [int(c) for c in code]
    n = max(digits)
    return all(i in digits for i in range(1, n + 1))


# -------------------------------------------------
# Transposition (angepasst für dein System)
# -------------------------------------------------

def permute_text(text: str, code: str) -> str:
    text = text.replace(" ", "")
    code_indices = [int(c) - 1 for c in code]
    block_size = max(code_indices) + 1

    result = []

    for i in range(0, len(text), block_size):
        block = list(text[i:i + block_size])
        for idx in code_indices:
            if idx < len(block):
                result.append(block[idx])

    return ''.join(result)


def inverse_permute_text(text: str, code: str) -> str:
    code_indices = [int(c) - 1 for c in code]
    block_size = max(code_indices) + 1

    result = []
    i = 0

    while i < len(text):
        block_len = min(block_size, len(text) - i)
        produced = sum(1 for idx in code_indices if idx < block_len)

        block = text[i:i + produced]
        original = [''] * block_len

        pos = 0
        for idx in code_indices:
            if idx < block_len and pos < len(block):
                original[idx] = block[pos]
                pos += 1

        result.extend(original)
        i += produced

    return ''.join(result)


# -------------------------------------------------
# Fake-Bit-System
# -------------------------------------------------

def apply_fake_bits(ciphertext: str) -> str:
    result = []
    for char in ciphertext:
        fake_char = random.choice(ALPHABET)
        result.append(fake_char)
        result.append(char)
    return ''.join(result)


def remove_fake_bits(fake_text: str) -> str:
    return fake_text[1::2]


# -------------------------------------------------
# Eingabe-Funktionen
# -------------------------------------------------

def get_vigenere_key() -> str:
    key = input("Geben Sie den Vigenère-Schlüssel ein: ").strip().lower()
    if not key:
        print("Fehler: Schlüssel darf nicht leer sein!")
        return get_vigenere_key()
    return key


def get_code() -> str:
    code = input("Geben Sie den Code ein (Zahlenfolge, Pflichtfeld): ").strip()
    if not code or not validate_code(code):
        print("Ungültiger Code! Er muss alle Zahlen von 1 bis zur größten Ziffer mindestens einmal enthalten.")
        return get_code()
    return code


# -------------------------------------------------
# Verschlüsselung
# -------------------------------------------------

def encrypt_mode():
    print("\n--- VERSCHLÜSSELUNGSMODUS ---")

    key = get_vigenere_key()
    cipher = VigenereCipher(key)

    plaintext = input("Geben Sie den zu verschlüsselnden Text ein: ").strip().lower()
    if not plaintext:
        print("Fehler: Text darf nicht leer sein!")
        return

    code = get_code()

    plaintext_perm = permute_text(plaintext, code)
    ciphertext = cipher.encrypt_lowercase(plaintext_perm)
    ciphertext_fake = apply_fake_bits(ciphertext)

    print("\n" + "-" * 40)
    print(f"Klartext:    {plaintext}")
    print(f"Schlüssel:   {key}")
    print(f"Code:        {code}")
    print(f"Geheimtext:  {ciphertext_fake}")
    print("-" * 40)


# -------------------------------------------------
# Entschlüsselung
# -------------------------------------------------

def decrypt_mode():
    print("\n--- ENTSCHLÜSSELUNGSMODUS ---")

    key = get_vigenere_key()
    cipher = VigenereCipher(key)

    ciphertext = input("Geben Sie den zu entschlüsselnden Text ein: ").strip().lower()
    if not ciphertext:
        print("Fehler: Text darf nicht leer sein!")
        return

    code = get_code()

    cleaned = remove_fake_bits(ciphertext)
    decrypted = cipher.decrypt_lowercase(cleaned)
    plaintext = inverse_permute_text(decrypted, code)

    print("\n" + "-" * 40)
    print(f"Geheimtext:  {ciphertext}")
    print(f"Schlüssel:   {key}")
    print(f"Code:        {code}")
    print(f"Klartext:    {plaintext}")
    print("-" * 40)


# -------------------------------------------------
# Batch-Modus
# -------------------------------------------------

def batch_mode():
    print("\n--- BATCH-MODUS ---")

    key = get_vigenere_key()
    cipher = VigenereCipher(key)

    filename = input("Geben Sie die Eingabedatei an: ").strip()
    input_path = DATA_DIR / filename
    output_path = DATA_DIR / f"{input_path.stem}_output.txt"

    code = get_code()
    mode = input("Verschlüsseln (1) oder Entschlüsseln (2)? ").strip()

    with input_path.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    with output_path.open("w", encoding="utf-8") as f:
        for line in lines:
            text = line.strip().lower()
            if not text:
                continue

            if mode == "1":
                text_perm = permute_text(text, code)
                encrypted = cipher.encrypt_lowercase(text_perm)
                result = apply_fake_bits(encrypted)
            else:
                cleaned = remove_fake_bits(text)
                decrypted = cipher.decrypt_lowercase(cleaned)
                result = inverse_permute_text(decrypted, code)

            f.write(result + "\n")

    print(f"\nErgebnis in '{output_path}' gespeichert!")


# -------------------------------------------------
# Info
# -------------------------------------------------

def show_info():
    print("""
--- INFORMATIONEN ZUR VIGENERE-CHIFFRE MIT FAKE-ZEICHEN ---

Die Vigenere-Chiffre ist ein polyalphabetisches Substitutionsverfahren,
das 1553 von Giambattista della Porta beschrieben wurde.

ERGÄNZUNG FÜR SCHULPROJEKT:
- Zusätzliche Fake-Zeichen erhöhen Sicherheit
- Position der echten Zeichen wird durch den Fake-Bit-Algorithmus bestimmt
- Blocktransposition nutzt die höchste Zahl als Blockgröße
""")


# -------------------------------------------------
# Main
# -------------------------------------------------

def main():
    print_banner()

    while True:
        print_menu()
        choice = input("Eingabe: ").strip()

        if choice == "1":
            encrypt_mode()
        elif choice == "2":
            decrypt_mode()
        elif choice == "3":
            batch_mode()
        elif choice == "4":
            show_info()
        elif choice == "5":
            print("\nAuf Wiedersehen!\n")
            sys.exit(0)
        else:
            print("Ungültige Eingabe! Bitte wählen Sie 1-5.")


if __name__ == "__main__":
    main()
