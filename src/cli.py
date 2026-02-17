
import sys
import random
import secrets
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
    Permutation (Blocktransposition). Leerzeichen und Satzzeichen werden mitpermutiert.
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


def _derive_seed(vigenere_key: str, code: str, nonce: str | None = None) -> int:
    """
    Ableitung des Seeds für RNG basierend auf Vigenere-Key, transpositions-code und optional Nonce.
    """
    if nonce:
        data = (vigenere_key + "|" + code + "|" + nonce).encode("utf-8")
    else:
        data = (vigenere_key + "|" + code).encode("utf-8")
    digest = hashlib.sha256(data).hexdigest()
    return int(digest[:16], 16)


def apply_dynamic_chaff(ciphertext: str, vigenere_key: str, code: str, nonce: str | None = None) -> str:
    """
    Fake-Zeichen (Chaff) aus dem kompletten CHARSET einfügen.
    Die Position/Anzahl wird pseudo-deterministisch aus vigenere_key+code(+nonce) abgeleitet.
    """
    seed = _derive_seed(vigenere_key, code, nonce)
    rng = random.Random(seed)
    result = []
    for char in ciphertext:
        fake_count = rng.randint(0, 3)  
        for _ in range(fake_count):
            result.append(rng.choice(ALPHABET))
        result.append(char)
    return ''.join(result)


def remove_dynamic_chaff(fake_text: str, vigenere_key: str, code: str, nonce: str | None = None) -> str:
    seed = _derive_seed(vigenere_key, code, nonce)
    rng = random.Random(seed)
    result = []
    i = 0
    n = len(fake_text)
    while i < n:
        fake_count = rng.randint(0, 3)
        for _ in range(fake_count):
            
            if i >= n:
                break
            i += 1
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


def _make_nonce() -> str:
    
    return secrets.token_hex(8)


def _encode_with_nonce_marker(nonce: str, payload: str) -> str:
    return f"[NONCE:{nonce}]{payload}"


def _extract_nonce_from_prefixed(ciphertext: str) -> tuple[str | None, str]:
    """
    Wenn der Ciphertext mit [NONCE:...] beginnt, extrahiere Nonce und Rest.
    Sonst (None, original).
    """
    if ciphertext.startswith("[NONCE:"):
        end = ciphertext.find("]")
        if end != -1:
            nonce = ciphertext[len("[NONCE:"):end]
            rest = ciphertext[end+1:]
            return nonce, rest
    return None, ciphertext


def encrypt_mode():
    print("\n--- VERSCHLÜSSELUNGSMODUS ---")
    key = get_vigenere_key()
    mix_key = get_mix_key()
    code = get_code()

    
    plaintext = input("Geben Sie den zu verschlüsselnden Text ein: ")
    if plaintext is None or plaintext == "":
        print("Fehler: Text darf nicht leer sein!")
        return

    
    nonce = _make_nonce()
    mix_key_effective = f"{mix_key}|{nonce}"

    cipher = VigenereCipher(key, mix_key_effective)

    
    plaintext_perm = permute_text(plaintext, code)
    ciphertext = cipher.encrypt_lowercase(plaintext_perm)
    ciphertext_fake = apply_dynamic_chaff(ciphertext, key, code, nonce)

    
    final = _encode_with_nonce_marker(nonce, ciphertext_fake)

    print("\n" + "-" * 40)
    print(f"Klartext:       {plaintext}")
    print(f"Vigenère-Key:   {key}")
    print(f"Misch-Key:      {mix_key}  (effective: {mix_key_effective})")
    print(f"Code:           {code}")
    print(f"Nonce:          {nonce}")
    print(f"Geheimtext:     {final}")
    print("-" * 40)


def decrypt_mode():
    print("\n--- ENTSCHLÜSSELUNGSMODUS ---")
    key = get_vigenere_key()
    mix_key = get_mix_key()
    ciphertext = input("Geben Sie den zu entschlüsselnden Text ein: ")
    if ciphertext is None or ciphertext == "":
        print("Fehler: Text darf nicht leer sein!")
        return
    code = get_code()

    
    nonce, rest = _extract_nonce_from_prefixed(ciphertext)
    if nonce:
        ciphertext_body = rest
        mix_key_effective = f"{mix_key}|{nonce}"
    else:
        ciphertext_body = ciphertext
        mix_key_effective = f"{mix_key}"  

    cipher = VigenereCipher(key, mix_key_effective)
    cleaned = remove_dynamic_chaff(ciphertext_body, key, code, nonce)
    decrypted = cipher.decrypt_lowercase(cleaned)
    plaintext = inverse_permute_text(decrypted, code)

    print("\n" + "-" * 40)
    print(f"Geheimtext:     {ciphertext}")
    print(f"Vigenère-Key:   {key}")
    print(f"Misch-Key:      {mix_key}  (effective: {mix_key_effective})")
    print(f"Code:           {code}")
    print(f"Nonce:          {nonce}")
    print(f"Klartext:       {plaintext}")
    print("-" * 40)


def txt_mode():
    print("\n--- TXT-MODUS ---")
    key = get_vigenere_key()
    mix_key = get_mix_key()
    cipher = None
    filename = input("Geben Sie die Eingabedatei an: ").strip()
    input_path = DATA_DIR / filename
    output_path = DATA_DIR / f"{input_path.stem}_output.txt"
    code = get_code()
    mode = input("Verschlüsseln (1) oder Entschlüsseln (2)? ").strip()
    with input_path.open("r", encoding="utf-8") as f:
        lines = f.readlines()
    with output_path.open("w", encoding="utf-8") as f:
        for line in lines:
            text = line.rstrip("\n")
            if text == "":
                f.write("\n")
                continue
            if mode == "1":
                
                nonce = _make_nonce()
                mix_key_effective = f"{mix_key}|{nonce}"
                cipher = VigenereCipher(key, mix_key_effective)
                text_perm = permute_text(text, code)
                encrypted = cipher.encrypt_lowercase(text_perm)
                result_body = apply_dynamic_chaff(encrypted, key, code, nonce)
                result = _encode_with_nonce_marker(nonce, result_body)
            else:
                
                nonce, rest = _extract_nonce_from_prefixed(text)
                if nonce:
                    ciphertext_body = rest
                    mix_key_effective = f"{mix_key}|{nonce}"
                else:
                    ciphertext_body = text
                    mix_key_effective = f"{mix_key}"
                cipher = VigenereCipher(key, mix_key_effective)
                cleaned = remove_dynamic_chaff(ciphertext_body, key, code, nonce)
                decrypted = cipher.decrypt_lowercase(cleaned)
                result = inverse_permute_text(decrypted, code)
            f.write(result + "\n")
    print(f"\nErgebnis in '{output_path}' gespeichert!")


def show_info():
    print("""
--- INFORMATIONEN ZUR VIGENERE-CHIFFRE MIT FAKE-ZEICHEN, MISCH-ALPHABET & NONCE ---

- Pro Verschlüsselung wird ein Nonce erzeugt (z. B. 16 hex-Zeichen) und als Präfix gespeichert: [NONCE:<hex>]...
- Der angegebene Misch-Key wird intern mit dem Nonce kombiniert, so entsteht pro-Nonce
  ein anderes gemischtes Alphabet.
- Chaff-Einfügung (Fake-Zeichen) wird ebenfalls durch einen Seed bestimmt, der den Nonce benutzt.
- Vorteil: gleiche Eingaben + gleiche Schlüssel produzieren unterschiedliche Ciphertexte.
- Wichtig: Nonce muss gespeichert/übertragen werden (ist nicht geheim), sonst ist
  Entschlüsselung nicht möglich.
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
