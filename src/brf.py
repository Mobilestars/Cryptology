import itertools
import string
import time
from math import factorial
from pathlib import Path
from vigenere_cipher import VigenereCipher

# ==============================
# PERMUTATION (aus deinem Code)
# ==============================

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


# ==============================
# SCORE FUNKTION
# ==============================

def load_wordlist():
    """
    Lädt die Wörter aus lists/wordlist-german.txt relativ zum Base-Verzeichnis
    """
    base_dir = Path(__file__).resolve().parent.parent
    wordlist_path = base_dir / "lists" / "wordlist-german.txt"

    words = set()
    with open(wordlist_path, "r", encoding="utf-8") as f:
        for line in f:
            word = line.strip().lower()
            if word:
                words.add(word)
    return words


COMMON_WORDS = load_wordlist()

def score_text(text):
    """
    Bewertet, wie wahrscheinlich der Text Deutsch ist.
    Je höher, desto wahrscheinlicher.
    """
    text = text.lower()
    score = 0

    for word in COMMON_WORDS:
        score += text.count(word) * 10

    for letter in "etaoinshrdlu":
        score += text.count(letter)

    return score


# ==============================
# GENERATOREN
# ==============================

def generate_keys(max_len):
    letters = string.ascii_lowercase
    for length in range(1, max_len + 1):
        for key in itertools.product(letters, repeat=length):
            yield ''.join(key)


def generate_codes(max_len):
    for length in range(2, max_len + 1):
        for perm in itertools.permutations(range(1, length + 1)):
            yield ''.join(str(x) for x in perm)


# ==============================
# BRUTE FORCE
# ==============================

def brute_force(ciphertext, max_key_len, max_code_len):

    total_keys = sum(26 ** i for i in range(1, max_key_len + 1))
    total_codes = sum(factorial(i) for i in range(2, max_code_len + 1))

    print("\nGeschätzte Kombinationen:", total_keys * total_codes)
    print("Startet Brute Force...\n")

    best_score = -1
    best_result = None
    tested = 0

    start_time = time.time()

    for code in generate_codes(max_code_len):
        for key in generate_keys(max_key_len):

            tested += 1

            cipher = VigenereCipher(key)

            try:
                decrypted = cipher.decrypt_lowercase(ciphertext)
                plaintext = inverse_permute_text(decrypted, code)

                score = score_text(plaintext)

                if score > best_score:
                    best_score = score
                    best_result = (key, code, plaintext)

                    print("\n===== NEUER BESTER TREFFER =====")
                    print("Key: ", key)
                    print("Code:", code)
                    print("Score:", score)
                    print("Text:", plaintext)
                    print("=================================")

            except:
                continue

            if tested % 100000 == 0:
                elapsed = time.time() - start_time
                print(f"{tested} Kombinationen getestet | {round(elapsed,2)} Sekunden")

    print("\n\n===== FERTIG =====")
    if best_result:
        print("Bester Key:", best_result[0])
        print("Bester Code:", best_result[1])
        print("Klartext:", best_result[2])
    else:
        print("Nichts gefunden.")


# ==============================
# TERMINAL INTERFACE
# ==============================

def main():
    print("=" * 60)
    print("VIGENERE + PERMUTATION BRUTE FORCE TOOL")
    print("=" * 60)

    ciphertext = input("Ciphertext eingeben: ").strip().lower()

    max_key_len = int(input("Maximale Schlüssellänge (z.B. 3): "))
    max_code_len = int(input("Maximale Code-Länge (z.B. 3): "))

    brute_force(ciphertext, max_key_len, max_code_len)


if __name__ == "__main__":
    main()
