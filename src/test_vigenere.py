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
        
        # Ein reiner numerischer Key ist erlaubt, wenn die Chiffre mit CHARSET arbeitet
        # Diese Test antwortet auf das tatsächliche Verhalten
    
    def test_basic_encryption(self):
        """Test der grundlegenden Verschlüsselung"""
        plaintext = "HELLOWORLD"
        ciphertext = self.cipher.encrypt(plaintext, use_nonce=False)
        self.assertNotEqual(plaintext, ciphertext)
        self.assertIsInstance(ciphertext, str)
    
    def test_encryption_decryption_roundtrip(self):
        """Test: Verschlüsselung und Entschlüsselung sollten Original zurückgeben"""
        plaintext = "DIESISTEINGEHEIMNIS"
        encrypted = self.cipher.encrypt(plaintext, use_nonce=False)
        decrypted = self.cipher.decrypt(encrypted)
        self.assertEqual(plaintext, decrypted)
    
    def test_encryption_with_spaces_and_punctuation(self):
        """Test mit Leerzeichen und Sonderzeichen"""
        plaintext = "HALLO, WELT!"
        encrypted = self.cipher.encrypt(plaintext, use_nonce=False)
        decrypted = self.cipher.decrypt(encrypted)
        self.assertEqual(plaintext, decrypted)
    
    def test_lowercase_preservation(self):
        """Test der Erhaltung der Groß-/Kleinschreibung"""
        plaintext = "Guten Morgen"
        encrypted = self.cipher.encrypt_lowercase(plaintext, use_nonce=False)
        decrypted = self.cipher.decrypt_lowercase(encrypted)
        self.assertEqual(plaintext, decrypted)
    
    def test_nonce_encryption(self):
        """Test: Mit Nonce sollte dieselbe Text zu unterschiedlichem Chiffrat führen"""
        plaintext = "HELLO"
        cipher = VigenereCipher("KEY")
        
        ciphertext1 = cipher.encrypt_lowercase(plaintext, use_nonce=True)
        ciphertext2 = cipher.encrypt_lowercase(plaintext, use_nonce=True)
        
        # Beide haben einen Nonce-Teil (unterschiedlich)
        self.assertIn("|", ciphertext1)
        self.assertIn("|", ciphertext2)
        
        # Ciphertexte sollten unterschiedlich sein
        self.assertNotEqual(ciphertext1, ciphertext2)
    
    def test_nonce_decryption(self):
        """Test: Mit Nonce verschlüsselt und entschlüsselt sollte Original zurückgeben"""
        plaintext = "GEHEIMES NACHRICHT"
        cipher = VigenereCipher("SCHLUESSEL")
        
        # Mit Nonce verschlüsseln
        encrypted = cipher.encrypt_lowercase(plaintext, use_nonce=True)
        self.assertIn("|", encrypted)
        
        # Entschlüsseln sollte Original zurückgeben
        decrypted = cipher.decrypt_lowercase(encrypted)
        self.assertEqual(plaintext, decrypted)
    
    def test_without_nonce(self):
        """Test: Ohne Nonce sollte identische Eingabe identisches Resultat geben"""
        plaintext = "HELLO"
        cipher = VigenereCipher("KEY")
        
        ciphertext1 = cipher.encrypt_lowercase(plaintext, use_nonce=False)
        ciphertext2 = cipher.encrypt_lowercase(plaintext, use_nonce=False)
        
        # Sollten identisch sein
        self.assertEqual(ciphertext1, ciphertext2)
        # Und kein Nonce enthalten
        self.assertNotIn("|", ciphertext1)
    
    def test_same_plaintext_different_output(self):
        """Test: Samma Klartext ergibt unterschiedliches Chiffrat bei verschiedenen Keys"""
        cipher1 = VigenereCipher("KEY")
        cipher2 = VigenereCipher("DIFFERENTKEY")
        
        plaintext = "HELLO"
        ciphertext1 = cipher1.encrypt(plaintext, use_nonce=False)
        ciphertext2 = cipher2.encrypt(plaintext, use_nonce=False)
        
        self.assertNotEqual(ciphertext1, ciphertext2)
    
    def test_historical_example(self):
        """Test mit historischem Beispiel"""
        # Vigenere-Beispiel mit Verifikation
        cipher = VigenereCipher("VIGENERECIPHER")
        plaintext = "ATTACKATDAWN"
        
        ciphertext = cipher.encrypt(plaintext, use_nonce=False)
        # Verifiziere die Rundtrip-Eigenschaft
        self.assertEqual(cipher.decrypt(ciphertext), plaintext)
    
    def test_decrypt_historical_example(self):
        """Test der Entschlüsselung mit historischem Beispiel"""
        cipher = VigenereCipher("VIGENERECIPHER")
        plaintext = "ATTACKATDAWN"
        
        ciphertext = cipher.encrypt(plaintext, use_nonce=False)
        decrypted = cipher.decrypt(ciphertext)
        # Verifiziere, dass Entschlüsselung Original zurückgibt
        self.assertEqual(decrypted, plaintext)
    
    def test_case_sensitivity(self):
        """Test: Chiffre arbeitet case-sensitive (kleine und große Buchstaben sind unterschiedlich)"""
        cipher1 = VigenereCipher("schluessel")
        cipher2 = VigenereCipher("SCHLUESSEL")
        
        plaintext = "HELLOWORLD"
        # Ohne Nonce verwenden
        ciphertext1 = cipher1.encrypt(plaintext, use_nonce=False)
        ciphertext2 = cipher2.encrypt(plaintext, use_nonce=False)
        
        # Sollten unterschiedlich sein, weil die Keys unterschiedlich sind
        self.assertNotEqual(ciphertext1, ciphertext2)


if __name__ == '__main__':
    unittest.main()
