import string
import hashlib
import random
import secrets
from typing import Optional

CHARSET = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation + " "
NONCE_LENGTH = 16  # Länge des Nonce in Zeichen


class VigenereCipher:
    def __init__(self, key: str, mix_key: Optional[str | int] = None):
        """
        key: Vigenère-Schlüssel (case-sensitive)
        mix_key: zweiter, beliebiger Key zur deterministischen Mischung des Charsets
        """
        if not key:
            raise ValueError("Vigenère-Key darf nicht leer sein.")
        
        self.key = key
        self.alphabet = self._generate_mixed_alphabet(mix_key)
        self.square = self._build_square()

        self._clean_key = ''.join([c for c in self.key if c in self.alphabet])
        if not self._clean_key:
            raise ValueError("Vigenère-Key enthält keine gültigen Zeichen aus dem Charset.")

    def _generate_mixed_alphabet(self, mix_key):
        """
        Erzeugt eine deterministische, gemischte Alphabet-Reihenfolge
        basierend auf mix_key. Wenn mix_key None ist, wird das Standard-Charset zurückgegeben.
        """
        letters = list(CHARSET)
        if mix_key is None:
            return ''.join(letters)

        seed_data = str(mix_key).encode("utf-8")
        digest = hashlib.sha256(seed_data).hexdigest()
        seed = int(digest[:16], 16)
        rng = random.Random(seed)
        rng.shuffle(letters)
        return ''.join(letters)

    def _build_square(self):
        """
        Erstellt das Vigenère-Quadrat basierend auf dem gemischten Alphabet.
        Quadrate-Row i = alphabet rotated by i.
        """
        square = []
        n = len(self.alphabet)
        for i in range(n):
            row = self.alphabet[i:] + self.alphabet[:i]
            square.append(row)
        return square

    def _generate_nonce(self) -> str:
        """
        Erzeugt einen zufälligen Nonce aus dem verfügbaren Alphabet.
        """
        return ''.join(secrets.choice(self.alphabet) for _ in range(NONCE_LENGTH))

    def _extend_key_with_nonce(self, nonce: str) -> str:
        """
        Verlängert den Schlüssel mit dem Nonce für zusätzliche Sicherheit.
        """
        return self._clean_key + nonce

    def _format_text(self, text: str) -> str:
        """
        Hier: wir lassen alle Zeichen durch, auch wenn sie nicht im Charset sind.
        """
        return text

    def _diffuse_key(self, key_state: str, cipher_char: str) -> str:
        """
        Avalanche Effect: Verändert den Key basierend auf dem letzten verschlüsselten Zeichen.
        """
        if not key_state:
            return key_state
        
        cipher_idx = self.alphabet.index(cipher_char) if cipher_char in self.alphabet else 0
        rotation = (cipher_idx % len(key_state)) + 1
        rotated_key = key_state[rotation:] + key_state[:rotation]
        return rotated_key

    def _permute_key(self, key_state: str, position: int) -> str:
        """
        Permutiert den Key basierend auf der aktuellen Position.
        """
        if not key_state:
            return key_state
        
        perm_factor = position % len(key_state)
        permuted = key_state[perm_factor:] + key_state[:perm_factor]
        return permuted

    def encrypt_lowercase(self, plaintext: str, use_nonce: bool = True) -> str:
        """
        Verschlüsselt plaintext (case-sensitive).
        Fügt optional Nonce + Header hinzu.
        """
        plaintext = self._format_text(plaintext)
        
        nonce = self._generate_nonce() if use_nonce else ""
        extended_key = self._extend_key_with_nonce(nonce) if use_nonce else self._clean_key
        
        ciphertext = []
        key_len = len(extended_key)
        key_pos = 0
        current_key_state = extended_key

        for char_index, char in enumerate(plaintext):
            if char not in self.alphabet:
                ciphertext.append(char)
            else:
                permuted_key = self._permute_key(current_key_state, char_index)
                p_idx = self.alphabet.index(char)
                k_char = permuted_key[key_pos % key_len]
                k_idx = self.alphabet.index(k_char)
                c = self.square[k_idx][p_idx]
                ciphertext.append(c)
                current_key_state = self._diffuse_key(current_key_state, c)
                key_pos += 1
        
        result_body = ''.join(ciphertext)
        
        # Neuer Header-Mechanismus: 2 Ziffern für Nonce-Länge, dann Nonce, dann Ciphertext
        if use_nonce:
            header = f"{len(nonce):02d}"
            result = header + nonce + result_body
        else:
            result = result_body
        
        return result

    def decrypt_lowercase(self, ciphertext: str) -> str:
        """
        Entschlüsselt ciphertext (case-sensitive).
        Erkennt automatisch den Header mit Nonce.
        """
        ciphertext = self._format_text(ciphertext)
        
        nonce = ""
        # Prüfe auf Längenheader
        if len(ciphertext) >= 2 and ciphertext[:2].isdigit():
            length = int(ciphertext[:2])
            if len(ciphertext) >= 2 + length:
                nonce = ciphertext[2:2+length]
                ciphertext = ciphertext[2+length:]

        extended_key = self._extend_key_with_nonce(nonce) if nonce else self._clean_key
        
        plaintext = []
        key_len = len(extended_key)
        key_pos = 0
        current_key_state = extended_key

        for char_index, char in enumerate(ciphertext):
            if char not in self.alphabet:
                plaintext.append(char)
            else:
                permuted_key = self._permute_key(current_key_state, char_index)
                k_char = permuted_key[key_pos % key_len]
                k_idx = self.alphabet.index(k_char)
                row = self.square[k_idx]
                p_idx = row.index(char)
                plaintext.append(self.alphabet[p_idx])
                current_key_state = self._diffuse_key(current_key_state, char)
                key_pos += 1
                
        return ''.join(plaintext)

    # Aliase (Kompatibilität)
    def encrypt(self, plaintext: str, use_nonce: bool = True) -> str:
        return self.encrypt_lowercase(plaintext, use_nonce=use_nonce)

    def decrypt(self, ciphertext: str) -> str:
        return self.decrypt_lowercase(ciphertext)
