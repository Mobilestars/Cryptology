import string
import hashlib
import hmac
import random
import secrets
from pathlib import Path
from typing import Optional
import yaml

def load_config():
    """Lädt Konfigurationswerte aus config.yml."""
    config_path = Path(__file__).parent.parent / "config.yml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

config = load_config()

NONCE_LENGTH = config.get("nonce_length", 16)
HMAC_BLOCK_SIZE = config.get("hmac_block_size", 8)
HMAC_TAG_LENGTH = config.get("hmac_tag_length", 12)


CHARSET = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation + " "

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

    def _compute_hmac_digest(self, data: str, key: str, nonce: str = "") -> str:
        """
        Berechnet einen HMAC-SHA256 Digest basierend auf Daten und Schlüssel.
        Revolutionäres System: Der HMAC wird mit Nonce kombiniert für adaptive Schlüsselvolution.
        """
        hmac_input = (key + nonce + data).encode('utf-8')
        hmac_key = self._clean_key.encode('utf-8')
        digest = hmac.new(hmac_key, hmac_input, hashlib.sha256).hexdigest()
        return digest

    def _hmac_tag_to_alphabet(self, hmac_digest: str, length: int) -> str:
        """
        Konvertiert einen HMAC-Hexadecimal-Digest zu Alphabet-Zeichen.
        Dies erlaubt HMAC-Tags eingebettet in den Ciphertext zu speichern.
        """
        chars = []
        for i in range(0, min(length * 4, len(hmac_digest)), 4):
            hex_block = hmac_digest[i:i+4]
            val = int(hex_block, 16) % len(self.alphabet)
            chars.append(self.alphabet[val])
        return ''.join(chars[:length])

    def _evolve_key_from_hmac(self, key_state: str, hmac_digest: str, position: int) -> str:
        """
        Revolutionäres HMAC-Verfahren: Evoliert den Key basierend auf HMAC-Digest.
        Dies erzeugt extreme Diffusion und erschwert Kryptoanalyse erheblich.
        """
        if not key_state:
            return key_state
        
        
        for i, hex_pair in enumerate(hmac_digest[::4]):
            rotation = (int(hex_pair, 16) + position) % len(key_state)
            key_state = key_state[rotation:] + key_state[:rotation]
        
        return key_state

    def _compute_block_hmac(self, ciphertext_block: str, nonce: str, block_index: int) -> str:
        """
        Berechnet HMAC für einen Ciphertext-Block zur Authentifizierung und Key-Evolution.
        """
        block_data = f"{block_index}:{ciphertext_block}"
        return self._compute_hmac_digest(block_data, self.key, nonce)

    def encrypt_lowercase(self, plaintext: str, use_nonce: bool = True, use_hmac: bool = True) -> str:
        """
        Verschlüsselt plaintext mit integriertem revolutionärem HMAC-System.
        
        Das HMAC-System:
        - Adaptive HMAC-basierte Schlüsselevolution nach jedem Block
        - Finale Authentication Tag für Integritätsprüfung
        - Extreme Diffusion durch HMAC-Digest-gestützte Transformationen
        
        Args:
            plaintext: Text zum Verschlüsseln
            use_nonce: Nonce verwenden für zusätzliche Sicherheit
            use_hmac: Revolutionäres HMAC-System für Authentifizierung aktivieren
        """
        plaintext = self._format_text(plaintext)
        
        nonce = self._generate_nonce() if use_nonce else ""
        extended_key = self._extend_key_with_nonce(nonce) if use_nonce else self._clean_key
        
        ciphertext = []
        key_len = len(extended_key)
        key_pos = 0
        current_key_state = extended_key
        alphabet_ciphertext = []

        for plaintext_char in plaintext:
            if plaintext_char not in self.alphabet:
                ciphertext.append(plaintext_char)
            else:
                permuted_key = self._permute_key(current_key_state, len(alphabet_ciphertext))
                p_idx = self.alphabet.index(plaintext_char)
                k_char = permuted_key[key_pos % key_len]
                k_idx = self.alphabet.index(k_char)
                c = self.square[k_idx][p_idx]
                ciphertext.append(c)
                alphabet_ciphertext.append(c)
                current_key_state = self._diffuse_key(current_key_state, c)
                
                
                if use_hmac and len(alphabet_ciphertext) % HMAC_BLOCK_SIZE == 0:
                    block = ''.join(alphabet_ciphertext[-HMAC_BLOCK_SIZE:])
                    block_hmac = self._compute_hmac_digest(block, self.key, nonce)
                    current_key_state = self._evolve_key_from_hmac(current_key_state, block_hmac, len(alphabet_ciphertext))
                
                key_pos += 1
        
        result_body = ''.join(ciphertext)
        
        
        if use_nonce:
            header = f"{len(nonce):02d}{nonce}"
        else:
            header = ""
        
        if use_hmac:
            final_hmac = self._compute_hmac_digest(result_body, self.key, nonce)
            final_tag = self._hmac_tag_to_alphabet(final_hmac, HMAC_TAG_LENGTH)
            result = header + "H" + final_tag + result_body
        else:
            result = header + "N" + result_body
        
        return result


    def decrypt_lowercase(self, ciphertext: str, verify_hmac: bool = True) -> str:
        """
        Entschlüsselt ciphertext mit HMAC-Authentifizierungsprüfung.
        
        Das System verifiziert die Integrität der Nachricht, indem es das finale
        HMAC mit dem erwarteten Wert vergleicht.
        
        Args:
            ciphertext: Verschlüsselter Text
            verify_hmac: HMAC-Tags zur Authentifizierung prüfen
        
        Returns:
            Entschlüsselter Plaintext
            
        Raises:
            ValueError: Wenn HMAC-Authentifizierung fehlschlägt
        """
        ciphertext = self._format_text(ciphertext)
        
        nonce = ""
        use_hmac = False
        hmac_tag = ""
        
        
        if len(ciphertext) >= 2 and ciphertext[:2].isdigit():
            nonce_len = int(ciphertext[:2])
            if len(ciphertext) >= 2 + nonce_len:
                nonce = ciphertext[2:2 + nonce_len]
                ciphertext = ciphertext[2 + nonce_len:]
        
        
        if len(ciphertext) >= 1:
            if ciphertext[0] == "H":
                use_hmac = True
                if len(ciphertext) >= 1 + HMAC_TAG_LENGTH:
                    hmac_tag = ciphertext[1:1 + HMAC_TAG_LENGTH]
                    ciphertext = ciphertext[1 + HMAC_TAG_LENGTH:]
            elif ciphertext[0] == "N":
                use_hmac = False
                ciphertext = ciphertext[1:]

        extended_key = self._extend_key_with_nonce(nonce) if nonce else self._clean_key
        
        plaintext = []
        key_len = len(extended_key)
        key_pos = 0
        current_key_state = extended_key
        alphabet_ciphertext = []

        for ciphar_char in ciphertext:
            if ciphar_char not in self.alphabet:
                plaintext.append(ciphar_char)
            else:
                permuted_key = self._permute_key(current_key_state, len(alphabet_ciphertext))
                k_char = permuted_key[key_pos % key_len]
                k_idx = self.alphabet.index(k_char)
                row = self.square[k_idx]
                p_idx = row.index(ciphar_char)
                plaintext.append(self.alphabet[p_idx])
                current_key_state = self._diffuse_key(current_key_state, ciphar_char)
                
                alphabet_ciphertext.append(ciphar_char)
                
                
                if use_hmac and len(alphabet_ciphertext) % HMAC_BLOCK_SIZE == 0:
                    block = ''.join(alphabet_ciphertext[-HMAC_BLOCK_SIZE:])
                    block_hmac = self._compute_hmac_digest(block, self.key, nonce)
                    current_key_state = self._evolve_key_from_hmac(current_key_state, block_hmac, len(alphabet_ciphertext))
                
                key_pos += 1
        
        plaintext_result = ''.join(plaintext)
        
        
        if verify_hmac and use_hmac and hmac_tag:
            final_hmac = self._compute_hmac_digest(ciphertext, self.key, nonce)
            expected_tag = self._hmac_tag_to_alphabet(final_hmac, HMAC_TAG_LENGTH)
            
            if hmac_tag != expected_tag:
                raise ValueError(
                    "HMAC-Authentifizierung fehlgeschlagen: "
                    "Die Nachricht könnte manipuliert worden sein!"
                )
        
        return plaintext_result


    
    def encrypt(self, plaintext: str, use_nonce: bool = True, use_hmac: bool = True) -> str:
        return self.encrypt_lowercase(plaintext, use_nonce=use_nonce, use_hmac=use_hmac)

    def decrypt(self, ciphertext: str, verify_hmac: bool = True) -> str:
        return self.decrypt_lowercase(ciphertext, verify_hmac=verify_hmac)
