"""
Unittest für die Vigenere-Verschlüsselung
"""

import unittest
from vigenere_cipher import VigenereCipher


class TestVigenereCipher(unittest.TestCase):
    """Testsuite für die VigenereCipher-Klasse"""
    
    def setUp(self):
        """Bereitet jeden Test vor"""
        self.cipher = VigenereCipher("SCHLUESSEL")
    
    def test_initialization(self):
        """Test der Cipher-Initialisierung"""
        self.assertEqual(self.cipher.key, "SCHLUESSEL")
    
    def test_invalid_key(self):
        """Test mit ungültigem Schlüssel"""
        with self.assertRaises(ValueError):
            VigenereCipher("")
        
        with self.assertRaises(ValueError):
            VigenereCipher("123456")
    
    def test_basic_encryption(self):
        """Test der grundlegenden Verschlüsselung"""
        plaintext = "HELLOWORLD"
        ciphertext = self.cipher.encrypt(plaintext)
        self.assertNotEqual(plaintext, ciphertext)
        self.assertIsInstance(ciphertext, str)
    
    def test_encryption_decryption_roundtrip(self):
        """Test: Verschlüsselung und Entschlüsselung sollten Original zurückgeben"""
        plaintext = "DIESISTEINGEHEIMNIS"
        encrypted = self.cipher.encrypt(plaintext)
        decrypted = self.cipher.decrypt(encrypted)
        self.assertEqual(plaintext, decrypted)
    
    def test_encryption_with_spaces_and_punctuation(self):
        """Test mit Leerzeichen und Sonderzeichen"""
        plaintext = "HALLO, WELT!"
        encrypted = self.cipher.encrypt(plaintext)
        decrypted = self.cipher.decrypt(encrypted)
        self.assertEqual(plaintext, decrypted)
    
    def test_lowercase_preservation(self):
        """Test der Erhaltung der Groß-/Kleinschreibung"""
        plaintext = "Guten Morgen"
        encrypted = self.cipher.encrypt_lowercase(plaintext)
        decrypted = self.cipher.decrypt_lowercase(encrypted)
        self.assertEqual(plaintext, decrypted)
    
    def test_same_plaintext_different_output(self):
        """Test: Samma Klartext ergibt unterschiedliches Chiffrat bei verschiedenen Positionen"""
        cipher1 = VigenereCipher("KEY")
        cipher2 = VigenereCipher("DIFFERENTKEY")
        
        plaintext = "HELLO"
        ciphertext1 = cipher1.encrypt(plaintext)
        ciphertext2 = cipher2.encrypt(plaintext)
        
        self.assertNotEqual(ciphertext1, ciphertext2)
    
    def test_historical_example(self):
        """Test mit historischem Beispiel"""
        # Vigenere-Beispiel mit Verifikation
        cipher = VigenereCipher("VIGENERECIPHER")
        plaintext = "ATTACKATDAWN"
        
        ciphertext = cipher.encrypt(plaintext)
        # Verifiziere die Rundtrip-Eigenschaft
        self.assertEqual(cipher.decrypt(ciphertext), plaintext)
    
    def test_decrypt_historical_example(self):
        """Test der Entschlüsselung mit historischem Beispiel"""
        cipher = VigenereCipher("VIGENERECIPHER")
        plaintext = "ATTACKATDAWN"
        
        ciphertext = cipher.encrypt(plaintext)
        decrypted = cipher.decrypt(ciphertext)
        # Verifiziere, dass Entschlüsselung Original zurückgibt
        self.assertEqual(decrypted, plaintext)
    
    def test_case_insensitivity(self):
        """Test: Chiffre sollte Groß-/Kleinschreibung ignorieren"""
        cipher1 = VigenereCipher("schluessel")
        cipher2 = VigenereCipher("SCHLUESSEL")
        
        plaintext = "HELLOWORLD"
        ciphertext1 = cipher1.encrypt(plaintext)
        ciphertext2 = cipher2.encrypt(plaintext)
        
        self.assertEqual(ciphertext1, ciphertext2)


if __name__ == '__main__':
    unittest.main()
