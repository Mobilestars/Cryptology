
import string
import hashlib
import random
import secrets
from typing import Optional


CHARSET = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation + " "
NONCE_LENGTH = 16  

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
        Der Nonce wird verwendet, um Verschiedenheit in der Verschlüsselung zu garantieren.
        """
        return ''.join(secrets.choice(self.alphabet) for _ in range(NONCE_LENGTH))

    def _extend_key_with_nonce(self, nonce: str) -> str:
        """
        Verlängert den Schlüssel mit dem Nonce für zusätzliche Sicherheit.
        Der neue Key ist: original_key + nonce
        """
        return self._clean_key + nonce

    def _format_text(self, text: str) -> str:
        """
        Hier: wir lassen alle Zeichen durch, aber verwerfen (nicht verschlüsseln)
        solche, die nicht im Charset sind — alternativ könnten wir sie auch
        direkt durchreichen. Wir wählen: durchreichen (keine Veränderung),
        damit der Nutzer keine Überraschungen hat. (=> diese Methode nur zur Prüfung)
        """
        
        return text

    def encrypt_lowercase(self, plaintext: str, use_nonce: bool = True) -> str:
        """
        Verschlüsselt plaintext (case-sensitive). 
        Zeichensätze, die nicht im alphabet sind, werden unverändert durchgereicht.
        
        Wenn use_nonce=True, wird einem zufälligen Nonce am Anfang des Ciphertexts hinzugefügt.
        Format: [NONCE]|[CIPHERTEXT]
        """
        plaintext = self._format_text(plaintext)
        
        
        nonce = self._generate_nonce() if use_nonce else ""
        extended_key = self._extend_key_with_nonce(nonce) if use_nonce else self._clean_key
        
        ciphertext = []
        key_len = len(extended_key)
        key_pos = 0

        for char in plaintext:
            if char not in self.alphabet:
                ciphertext.append(char)
            else:
                p_idx = self.alphabet.index(char)
                k_char = extended_key[key_pos % key_len]
                k_idx = self.alphabet.index(k_char)
                c = self.square[k_idx][p_idx]
                ciphertext.append(c)
                key_pos += 1
        
        result = ''.join(ciphertext)
        
        
        if use_nonce:
            result = nonce + "|" + result
        
        return result

    def decrypt_lowercase(self, ciphertext: str) -> str:
        """
        Entschlüsselt ciphertext (case-sensitive). 
        Zeichen, die nicht im alphabet sind, werden unverändert durchgereicht.
        
        Falls der Text mit einem Nonce versehen ist (Format: [NONCE]|[CIPHERTEXT]),
        wird dieser extrahiert und bei der Entschlüsselung verwendet.
        """
        ciphertext = self._format_text(ciphertext)
        
        
        nonce = ""
        if "|" in ciphertext:
            nonce, ciphertext = ciphertext.split("|", 1)
        
        extended_key = self._extend_key_with_nonce(nonce) if nonce else self._clean_key
        
        plaintext = []
        key_len = len(extended_key)
        key_pos = 0

        for char in ciphertext:
            if char not in self.alphabet:
                plaintext.append(char)
            else:
                k_char = extended_key[key_pos % key_len]
                k_idx = self.alphabet.index(k_char)
                row = self.square[k_idx]
                p_idx = row.index(char)
                plaintext.append(self.alphabet[p_idx])
                key_pos += 1
        return ''.join(plaintext)

    def encrypt(self, plaintext: str, use_nonce: bool = True) -> str:
        """
        Alias für encrypt_lowercase() für Backward Compatibility.
        """
        return self.encrypt_lowercase(plaintext, use_nonce=use_nonce)

    def decrypt(self, ciphertext: str) -> str:
        """
        Alias für decrypt_lowercase() für Backward Compatibility.
        """
        return self.decrypt_lowercase(ciphertext)