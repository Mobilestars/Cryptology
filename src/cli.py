import sys
from pathlib import Path
from vigenere_cipher import VigenereCipher

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

def print_banner():
    print("\n" + "=" * 60)
    print("  VIGENERE CIPHER - Verschlüsselungsmittel")
    print("=" * 60 + "\n")

def print_menu():
    print("\nWählen Sie eine Option:")
    print("1. Text verschlüsseln")
    print("2. Text entschlüsseln")
    print("3. Batch-Datei verarbeiten")
    print("4. Informationen anzeigen")
    print("5. Programmende")
    print("-" * 40)

def validate_code(code: str) -> bool:
    if not code.isdigit():
        return False
    digits = [int(c) for c in code]
    n = max(digits)
    for i in range(1, n + 1):
        if i not in digits:
            return False
    return True

def permute_text(text: str, code: str) -> str:
    text = text.replace(" ", "")
    code_indices = [int(c) - 1 for c in code]
    n = len(code_indices)
    result = []
    for i in range(0, len(text), n):
        block = list(text[i:i+n])
        permuted = [''] * len(block)
        used = [0] * len(block)
        for idx, code_idx in enumerate(code_indices):
            if idx >= len(block):
                continue
            pos = code_idx
            while pos < len(block) and used[pos]:
                pos += 1
            if pos >= len(block):
                pos = 0
                while used[pos]:
                    pos += 1
            permuted[pos] = block[idx]
            used[pos] = 1
        result.extend(permuted)
    return ''.join(result)

def inverse_permute_text(text: str, code: str) -> str:
    code_indices = [int(c) - 1 for c in code]
    n = len(code_indices)
    result = []
    for i in range(0, len(text), n):
        block = list(text[i:i+n])
        orig = [''] * len(block)
        used = [0] * len(block)
        for idx, code_idx in enumerate(code_indices):
            if idx >= len(block):
                continue
            pos = code_idx
            while pos < len(block) and used[pos]:
                pos += 1
            if pos >= len(block):
                pos = 0
                while used[pos]:
                    pos += 1
            orig[idx] = block[pos]
            used[pos] = 1
        result.extend(orig)
    return ''.join(result)

def get_vigenere_key() -> str:
    key = input("Geben Sie den Vigenère-Schlüssel ein: ").strip()
    if not key:
        print("Fehler: Schlüssel darf nicht leer sein!")
        return get_vigenere_key()
    return key

def get_code() -> str:
    code = input("Geben Sie den Code ein (Zahlenfolge, Pflichtfeld): ").strip()
    if not code or not validate_code(code):
        print("Ungültiger Code! Er muss alle Zahlen von 1 bis zur größten Ziffer enthalten.")
        return get_code()
    return code

def encrypt_mode():
    print("\n--- VERSCHLÜSSELUNGSMODUS ---")
    key = get_vigenere_key()
    cipher = VigenereCipher(key)
    plaintext = input("Geben Sie den zu verschlüsselnden Text ein: ").strip()
    if not plaintext:
        print("Fehler: Text darf nicht leer sein!")
        return
    code = get_code()
    plaintext_perm = permute_text(plaintext, code)
    ciphertext = cipher.encrypt_lowercase(plaintext_perm)
    print("\n" + "-" * 40)
    print(f"Klartext:    {plaintext}")
    print(f"Schlüssel:   {key}")
    print(f"Code:        {code}")
    print(f"Geheimtext:  {ciphertext}")
    print("-" * 40)

def decrypt_mode():
    print("\n--- ENTSCHLÜSSELUNGSMODUS ---")
    key = get_vigenere_key()
    cipher = VigenereCipher(key)
    ciphertext = input("Geben Sie den zu entschlüsselnden Text ein: ").strip()
    if not ciphertext:
        print("Fehler: Text darf nicht leer sein!")
        return
    code = get_code()
    decrypted = cipher.decrypt_lowercase(ciphertext)
    plaintext = inverse_permute_text(decrypted, code)
    print("\n" + "-" * 40)
    print(f"Geheimtext:  {ciphertext}")
    print(f"Schlüssel:   {key}")
    print(f"Code:        {code}")
    print(f"Klartext:    {plaintext}")
    print("-" * 40)

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
            text = line.strip()
            if not text:
                continue
            if mode == "1":
                text_perm = permute_text(text, code)
                result = cipher.encrypt_lowercase(text_perm)
            else:
                decrypted = cipher.decrypt_lowercase(text)
                result = inverse_permute_text(decrypted, code)
            f.write(result + "\n")
    print(f"\nErgebnis in '{output_path}' gespeichert!")

def show_info():
    print("""
--- INFORMATIONEN ZUR VIGENERE-CHIFFRE ---

Die Vigenere-Chiffre ist ein polyalphabetisches Substitutionsverfahren,
das 1553 von Giambattista della Porta beschrieben wurde.

FUNKTIONSWEISE:
- Kombination mehrerer Caesar-Verschiebungen
- Schlüssel bestimmt die Verschiebung je Zeichen

SICHERHEIT:
- Historisch relevant
- Heute kryptographisch unsicher
""")

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
