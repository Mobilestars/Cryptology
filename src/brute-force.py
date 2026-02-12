import itertools
import string
import time
from math import factorial
from pathlib import Path
from multiprocessing import Pool, cpu_count
from vigenere_cipher import VigenereCipher

# ==============================
# PERMUTATION
# ==============================

def inverse_permute_text(text: str, code: str) -> str:
    code_indices = [int(c) - 1 for c in code]
    n = len(code_indices)
    result = []

    for i in range(0, len(text), n):
        block = text[i:i+n]
        block_len = len(block)
        orig = [''] * block_len

        for idx, code_idx in enumerate(code_indices):
            if idx < block_len and code_idx < block_len:
                orig[idx] = block[code_idx]

        result.extend(orig)

    return ''.join(result)

# ==============================
# WORDLIST LADEN
# ==============================

def load_wordlist():
    base_dir = Path(__file__).resolve().parent.parent
    wordlist_path = base_dir / "lists" / "wordlist-german.txt"

    words = set()
    with open(wordlist_path, "r", encoding="utf-8") as f:
        for line in f:
            w = line.strip().lower()
            if w:
                words.add(w)
    return words

COMMON_WORDS = load_wordlist()

# ==============================
# SCORE / WORT-PRÜFUNG
# ==============================

def analyze_text(text):
    """
    Prüft, ob mindestens ein Wordlist-Wort im Text vorkommt.
    Berechnet Score = Summe der Wortlängen + 100*Abdeckung.
    Ignoriert alles ohne echte Wörter.
    """
    text = text.lower()
    found_words = [w for w in COMMON_WORDS if w in text]

    if not found_words:
        return 0, []

    # Abdeckung: wie viele Buchstaben des Textes gehören zu Wordlist-Wörtern
    covered_letters = 0
    for w in found_words:
        # Zähle, wie oft Wort im Text vorkommt
        covered_letters += text.count(w) * len(w)

    coverage_ratio = covered_letters / len(text)

    if coverage_ratio < 0.85:
        return 0, []

    score = int(coverage_ratio * 100) + sum(len(w) for w in found_words)
    return score, found_words

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
# WORKER
# ==============================

def worker(args):
    ciphertext, code, max_key_len = args
    results = []

    permuted = inverse_permute_text(ciphertext, code)

    for key in generate_keys(max_key_len):
        cipher = VigenereCipher(key)
        plaintext = cipher.decrypt_lowercase(permuted)

        score, words = analyze_text(plaintext)
        if score > 0:
            results.append((score, key, code, plaintext))

    return results

# ==============================
# BRUTE FORCE
# ==============================

def brute_force(ciphertext, max_key_len, max_code_len):
    total_keys = sum(26 ** i for i in range(1, max_key_len + 1))
    total_codes = sum(factorial(i) for i in range(2, max_code_len + 1))

    print("\nGeschätzte Kombinationen:", total_keys * total_codes)
    print("CPU-Kerne:", cpu_count())
    print("Startet Brute Force...\n")

    start_time = time.time()

    tasks = [(ciphertext, code, max_key_len) for code in generate_codes(max_code_len)]

    all_results = []

    with Pool(cpu_count()) as pool:
        for result in pool.imap_unordered(worker, tasks):
            if result:
                all_results.extend(result)

    elapsed = round(time.time() - start_time, 2)

    print("\n===== FERTIG =====")
    print("Zeit:", elapsed, "Sekunden")

    if not all_results:
        print("Keine passenden Ergebnisse gefunden.")
        return

    # Sortiere nach Score absteigend
    all_results.sort(reverse=True, key=lambda x: x[0])

    # In data/results.txt speichern
    output_path = Path(__file__).resolve().parent.parent / "data" / "results.txt"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        for score, key, code, plaintext in all_results:
            f.write(f"Score: {score}\n")
            f.write(f"Key:   {key}\n")
            f.write(f"Code:  {code}\n")
            f.write(f"Text:  {plaintext}\n\n")

    print(f"\nErgebnisse gespeichert in: {output_path.resolve()}")

# ==============================
# TERMINAL INTERFACE
# ==============================

def main():
    print("=" * 60)
    print("VIGENERE + PERMUTATION BRUTE FORCE TOOL (FINAL)")
    print("=" * 60)

    ciphertext = input("Ciphertext eingeben: ").strip().lower()
    max_key_len = int(input("Maximale Schlüssellänge: "))
    max_code_len = int(input("Maximale Code-Länge: "))

    brute_force(ciphertext, max_key_len, max_code_len)

if __name__ == "__main__":
    main()
