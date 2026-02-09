"""
Vigenere Cipher Implementation
Eine klassische polyalphabetische Substitutionsverschlüsselung
"""

class VigenereCipher:
    """
    Implementierung der Vigenere-Verschlüsselung.
    
    Die Vigenere-Verschlüsselung ist ein polyalphabetisches Verschlüsselungsverfahren,
    das einen Schlüsseltext verwendet, um nacheinander Caesar-Verschiebungen durchzuführen.
    """
    
    def __init__(self, key: str):
        """
        Initialisiert die Vigenere-Chiffre mit einem Schlüssel.
        
        Args:
            key: Der Verschlüsselungsschlüssel (darf nur Buchstaben enthalten)
            
        Raises:
            ValueError: Wenn der Schlüssel leer oder ungültig ist
        """
        if not key or not key.isalpha():
            raise ValueError("Der Schlüssel muss aus Buchstaben bestehen und darf nicht leer sein")
        
        self.key = key.upper()
    
    def _expand_key(self, text: str) -> str:
        """
        Wiederholt den Schlüssel so oft, bis er die Länge des Textes hat.
        Ignoriert dabei Leerzeichen und Sonderzeichen.
        
        Args:
            text: Der Text, für den der Schlüssel erweitert werden soll
            
        Returns:
            Der erweiterte Schlüssel
        """
        key_index = 0
        expanded_key = []
        
        for char in text:
            if char.isalpha():
                expanded_key.append(self.key[key_index % len(self.key)])
                key_index += 1
            else:
                # Leerzeichen und Sonderzeichen werden nicht verschlüsselt
                expanded_key.append(char)
        
        return ''.join(expanded_key)
    
    def encrypt(self, plaintext: str) -> str:
        """
        Verschlüsselt einen Text mit der Vigenere-Chiffre.
        
        Args:
            plaintext: Der zu verschlüsselnde Text
            
        Returns:
            Der verschlüsselte Text
        """
        plaintext = plaintext.upper()
        expanded_key = self._expand_key(plaintext)
        ciphertext = []
        
        for plain_char, key_char in zip(plaintext, expanded_key):
            if plain_char.isalpha():
                # Shift-Wert aus dem Schlüssel (A=0, B=1, ..., Z=25)
                shift = ord(key_char) - ord('A')
                
                # Verschlüsselter Buchstabe
                encrypted_char = chr((ord(plain_char) - ord('A') + shift) % 26 + ord('A'))
                ciphertext.append(encrypted_char)
            else:
                # Nicht-Buchstaben bleiben unverändert
                ciphertext.append(plain_char)
        
        return ''.join(ciphertext)
    
    def decrypt(self, ciphertext: str) -> str:
        """
        Entschlüsselt einen mit Vigenere verschlüsselten Text.
        
        Args:
            ciphertext: Der zu entschlüsselnde Text
            
        Returns:
            Der entschlüsselte (ursprüngliche) Text
        """
        ciphertext = ciphertext.upper()
        expanded_key = self._expand_key(ciphertext)
        plaintext = []
        
        for cipher_char, key_char in zip(ciphertext, expanded_key):
            if cipher_char.isalpha():
                # Shift-Wert aus dem Schlüssel
                shift = ord(key_char) - ord('A')
                
                # Entschlüsselter Buchstabe (inverse Operation)
                decrypted_char = chr((ord(cipher_char) - ord('A') - shift) % 26 + ord('A'))
                plaintext.append(decrypted_char)
            else:
                # Nicht-Buchstaben bleiben unverändert
                plaintext.append(cipher_char)
        
        return ''.join(plaintext)
    
    def encrypt_lowercase(self, plaintext: str) -> str:
        """
        Verschlüsselt einen Text und behält die ursprüngliche Groß-/Kleinschreibung bei.
        
        Args:
            plaintext: Der zu verschlüsselnde Text
            
        Returns:
            Der verschlüsselte Text mit beibehaltener Groß-/Kleinschreibung
        """
        plaintext_upper = plaintext.upper()
        encrypted = self.encrypt(plaintext_upper)
        
        # Wiederherstellen der ursprünglichen Groß-/Kleinschreibung
        result = []
        for original, encrypted_char in zip(plaintext, encrypted):
            if original.islower() and encrypted_char.isalpha():
                result.append(encrypted_char.lower())
            else:
                result.append(encrypted_char)
        
        return ''.join(result)
    
    def decrypt_lowercase(self, ciphertext: str) -> str:
        """
        Entschlüsselt einen Text und behält die ursprüngliche Groß-/Kleinschreibung bei.
        
        Args:
            ciphertext: Der zu entschlüsselnde Text
            
        Returns:
            Der entschlüsselte Text mit beibehaltener Groß-/Kleinschreibung
        """
        ciphertext_upper = ciphertext.upper()
        decrypted = self.decrypt(ciphertext_upper)
        
        # Wiederherstellen der ursprünglichen Groß-/Kleinschreibung
        result = []
        for original, decrypted_char in zip(ciphertext, decrypted):
            if original.islower() and decrypted_char.isalpha():
                result.append(decrypted_char.lower())
            else:
                result.append(decrypted_char)
        
        return ''.join(result)
