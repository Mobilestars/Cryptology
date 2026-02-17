import sys
import random
from pathlib import Path
from vigenere_cipher import VigenereCipher, CHARSET
import string
import hashlib

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

ALPHABET = CHARSET  

def print_banner():
    print("\n" + "=" * 60)
    print("  JikCrypt - VIGENERE; Transposition; Chaff (mit Mischalphabet & kompletter Zeichensatz)")
    print("=" * 60 + "\n")


def print_menu():
    print("\nWählen Sie eine Option:")
    print("1. Text verschlüsseln")
    print("2. Text entschlüsseln")
    print("3. TXT-Datei verarbeiten")
    print("4. Informationen anzeigen")
    print("5. Programmende")
    print("-" * 40)


def validate_code(code: str) -> bool:
    if not code.isdigit():
        return False
    digits = [int(c) for c in code]
    n = max(digits)
    return all(i in digits for i in range(1, n + 1))


def permute_text(text: str, code: str) -> str:
    """
    Permutation (Blocktransposition). WICHTIG: jetzt werden auch Leerzeichen,
    Satzzeichen und Ziffern permutiert (keine Entfernung von spaces).
    """
    
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

    produced_full = sum(1 for idx in code_indices if idx < block_size)

    result = []
    i = 0
    n = len(text)

    while n - i >= produced_full and produced_full > 0:
        block = text[i:i + produced_full]
        original = [''] * block_size
        positions = [idx for idx in code_indices if idx < block_size]
        for pos, idx in enumerate(positions):
            original[idx] = block[pos]
        result.extend(original)
        i += produced_full

    remaining = n - i
    if remaining > 0:
        found = False
        for b in range(1, block_size + 1):
            produced_b = sum(1 for idx in code_indices if idx < b)
            if produced_b == remaining:
                block = text[i:i + produced_b]
                original = [''] * b
                positions = [idx for idx in code_indices if idx < b]
                for pos, idx in enumerate(positions):
                    original[idx] = block[pos]
                result.extend(original)
                i += produced_b
                found = True
                break
        if not found:
            b = min(block_size, remaining)
            block = text[i:i + remaining]
            original = [''] * b
            positions = [idx for idx in code_indices if idx < b]
            pos = 0
            for idx in positions:
                if pos < len(block) and idx < b:
                    original[idx] = block[pos]
                    pos += 1
            result.extend(original)
            i = n

    return ''.join(result)


def _derive_seed(vigenere_key: str, code: str) -> int:
    data = (vigenere_key + "|" + code).encode("utf-8")
    digest = hashlib.sha256(data).hexdigest()
    return int(digest[:16], 16)


def apply_dynamic_chaff(ciphertext: str, vigenere_key: str, code: str) -> str:
    """
    Fake-Zeichen (Chaff) aus dem kompletten CHARSET einfügen.
    Die Position/Anzahl wird pseudo-deterministisch aus vigenere_key+code abgeleitet.
    """
    seed = _derive_seed(vigenere_key, code)
    rng = random.Random(seed)
    result = []
    for char in ciphertext:
        fake_count = rng.randint(0, 3)  
        for _ in range(fake_count):
            result.append(rng.choice(ALPHABET))
        result.append(char)
    return ''.join(result)


def remove_dynamic_chaff(fake_text: str, vigenere_key: str, code: str) -> str:
    seed = _derive_seed(vigenere_key, code)
    rng = random.Random(seed)
    result = []
    i = 0
    n = len(fake_text)
    while i < n:
        fake_count = rng.randint(0, 3)
        for _ in range(fake_count):
            
            rng.choice(ALPHABET)
            i += 1
            if i >= n:
                break
        if i >= n:
            break
        result.append(fake_text[i])
        i += 1
    return ''.join(result)


def get_vigenere_key() -> str:
    key = input("Geben Sie den Vigenère-Schlüssel ein (case-sensitive): ").strip()
    if not key:
        print("Fehler: Schlüssel darf nicht leer sein!")
        return get_vigenere_key()
    return key


def get_mix_key() -> str:
    mix_key = input("Geben Sie den Misch-Schlüssel (zweiter Key) ein: ").strip()
    if not mix_key:
        print("Fehler: Misch-Schlüssel darf nicht leer sein!")
        return get_mix_key()
    return mix_key


def get_code() -> str:
    code = input("Geben Sie den Code ein (1-n, min. 1x.): ").strip()
    if not code or not validate_code(code):
        print("Ungültiger Code! Er muss alle Zahlen von 1 bis zur größten Ziffer mindestens einmal enthalten.")
        return get_code()
    return code


def encrypt_mode():
    print("\n--- VERSCHLÜSSELUNGSMODUS ---")
    key = get_vigenere_key()
    mix_key = get_mix_key()
    cipher = VigenereCipher(key, mix_key)
    plaintext = input("Geben Sie den zu verschlüsselnden Text ein: ")
    if plaintext is None or plaintext == "":
        print("Fehler: Text darf nicht leer sein!")
        return
    use_nonce_input = input("Nonce verwenden? (j/n, Standard: j): ").strip().lower()
    use_nonce = use_nonce_input != "n"
    code = get_code()
    plaintext_perm = permute_text(plaintext, code)
    ciphertext = cipher.encrypt_lowercase(plaintext_perm, use_nonce=use_nonce)
    ciphertext_fake = apply_dynamic_chaff(ciphertext, key, code)
    print("\n" + "-" * 40)
    print(f"Klartext:       {plaintext}")
    print(f"Vigenère-Key:   {key}")
    print(f"Misch-Key:      {mix_key}")
    print(f"Code:           {code}")
    print(f"Mit Nonce:      {'Ja' if use_nonce else 'Nein'}")
    print(f"Geheimtext:     {ciphertext_fake}")
    print("-" * 40)


def decrypt_mode():
    print("\n--- ENTSCHLÜSSELUNGSMODUS ---")
    key = get_vigenere_key()
    mix_key = get_mix_key()
    cipher = VigenereCipher(key, mix_key)
    ciphertext = input("Geben Sie den zu entschlüsselnden Text ein: ")
    if ciphertext is None or ciphertext == "":
        print("Fehler: Text darf nicht leer sein!")
        return
    code = get_code()
    cleaned = remove_dynamic_chaff(ciphertext, key, code)
    decrypted = cipher.decrypt_lowercase(cleaned)
    plaintext = inverse_permute_text(decrypted, code)
    print("\n" + "-" * 40)
    print(f"Geheimtext:     {ciphertext}")
    print(f"Vigenère-Key:   {key}")
    print(f"Misch-Key:      {mix_key}")
    print(f"Code:           {code}")
    print(f"Klartext:       {plaintext}")
    print("-" * 40)


def txt_mode():
    print("\n--- TXT-MODUS ---")
    key = get_vigenere_key()
    mix_key = get_mix_key()
    cipher = VigenereCipher(key, mix_key)
    filename = input("Geben Sie die Eingabedatei an: ").strip()
    input_path = DATA_DIR / filename
    output_path = DATA_DIR / f"{input_path.stem}_output.txt"
    code = get_code()
    mode = input("Verschlüsseln (1) oder Entschlüsseln (2)? ").strip()
    use_nonce = False
    if mode == "1":
        use_nonce_input = input("Nonce verwenden? (j/n, Standard: j): ").strip().lower()
        use_nonce = use_nonce_input != "n"
    with input_path.open("r", encoding="utf-8") as f:
        lines = f.readlines()
    with output_path.open("w", encoding="utf-8") as f:
        for line in lines:
            
            text = line.rstrip("\n")
            if text == "":
                f.write("\n")
                continue
            if mode == "1":
                text_perm = permute_text(text, code)
                encrypted = cipher.encrypt_lowercase(text_perm, use_nonce=use_nonce)
                result = apply_dynamic_chaff(encrypted, key, code)
            else:
                cleaned = remove_dynamic_chaff(text, key, code)
                decrypted = cipher.decrypt_lowercase(cleaned)
                result = inverse_permute_text(decrypted, code)
            f.write(result + "\n")
    print(f"\nErgebnis in '{output_path}' gespeichert!")


def show_info():
    print("""
--- INFORMATIONEN ZUR VIGENERE-CHIFFRE MIT NONCE, FAKE-ZEICHEN UND MISCH-ALPHABET ---

- Komplettes Charset verwendet: Kleinbuchstaben, Großbuchstaben (separat), Zahlen, Satzzeichen, Leerzeichen.
- Zweiter Key erzeugt deterministisch gemischtes Alphabet (mix_key).
- Nonce: 16 zufällige Zeichen am Anfang des Ciphertexts (optional).
  * Garantiert unterschiedliche Ciphertexte für denselben Plaintext.
  * Format: [NONCE]|[CIPHERTEXT]
  * Wird automatisch bei Entschlüsselung erkannt.
- Zusätzliche Fake-Zeichen erhöhen Sicherheit.
- Blocktransposition permutiert jede Block mit konfigurierbarem Code.
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
            txt_mode()
        elif choice == "4":
            show_info()
        elif choice == "5":
            print("\nAuf Wiedersehen!\n")
            sys.exit(0)
        else:
            print("Ungültige Eingabe! Bitte wählen Sie 1-5.")


if __name__ == "__main__":
    main()