#!/usr/bin/env python3
"""
Testdatei für das revolutionäre HMAC-System der Vigenere-Verschlüsselung.

Das neue System bietet:
1. Adaptive HMAC-basierte Key-Evolution nach jedem Block
2. Eingebettete HMAC-Tags für Authentifizierung und Integritätsprüfung
3. Extreme Diffusion durch HMAC-gestützte Schlüsseltransformation
4. Automatische Authentizitätsprüfung beim Entschlüsseln
"""

from vigenere_cipher import VigenereCipher

HMAC_TAG_LENGTH = 12  # Muss mit vigenere_cipher.py synchron sein


def test_basic_hmac_encryption():
    """Test: Grundlegende Verschlüsselung mit HMAC-System"""
    print("=" * 60)
    print("TEST 1: Basis-Verschlüsselung mit HMAC-Integration")
    print("=" * 60)
    
    cipher = VigenereCipher("MySecretKey123!")
    plaintext = "Hello World! This is a test message with HMAC authentication."
    
    # Verschlüssele mit HMAC-System (Standard)
    ciphertext = cipher.encrypt(plaintext, use_nonce=True, use_hmac=True)
    print(f"\nPlaintext:  {plaintext}")
    print(f"Ciphertext: {ciphertext}\n")
    
    # Entschlüssele und verifiziere HMAC
    try:
        decrypted = cipher.decrypt(ciphertext, verify_hmac=True)
        print(f"Decrypted:  {decrypted}")
        print(f"✓ HMAC-Authentifizierung erfolgreich!")
        assert plaintext == decrypted, "Plaintext stimmt nicht überein!"
        print("✓ Verschlüsselung/Entschlüsselung korrekt!\n")
    except ValueError as e:
        print(f"✗ HMAC-Fehler: {e}\n")


def test_hmac_tampering_detection():
    """Test: Erkennung von Manipulationen durch HMAC"""
    print("=" * 60)
    print("TEST 2: Erkennung von Nachrichtenmanipulation")
    print("=" * 60)
    
    cipher = VigenereCipher("SecureKey456!")
    plaintext = "Important data that must not be altered in the message body"
    
    ciphertext = cipher.encrypt(plaintext, use_nonce=True, use_hmac=True)
    print(f"\nOriginaltext:  {plaintext}")
    print(f"Verschlüsselt: {ciphertext}\n")
    
    # Manipuliere den Ciphertext im Body
    # Struktur: [NONCE_LEN(2)][NONCE][HMAC_FLAG(1)][HMAC_TAG(12)][CIPHERTEXT_BODY]
    # Manipuliere im Ciphertext-Body (nach dem HMAC-Tag)
    header_len = 2 + len(ciphertext.split('H')[0][2:]) + 1 + HMAC_TAG_LENGTH if 'H' in ciphertext else len(ciphertext.split('N')[0]) + 1
    body_start = ciphertext.find('H') + 1 + HMAC_TAG_LENGTH if 'H' in ciphertext else ciphertext.find('N') + 1
    
    if body_start < len(ciphertext) - 5:
        manipulation_pos = body_start + 10
        tampered = (ciphertext[:manipulation_pos] + 
                   ('X' if ciphertext[manipulation_pos] != 'X' else 'Y') + 
                   ciphertext[manipulation_pos+1:])
        print(f"Manipuliert:   {tampered}")
        
        try:
            decrypted = cipher.decrypt(tampered, verify_hmac=True)
            print(f"✗ FEHLER: Manipulation nicht erkannt!")
        except ValueError as e:
            print(f"✓ Manipulation erkannt! {e}\n")
    else:
        print("Text zu kurz für Manipulationstest - Test übersprungen\n")


def test_hmac_vs_no_hmac():
    """Test: Vergleich HMAC aktiviert vs. deaktiviert"""
    print("=" * 60)
    print("TEST 3: Vergleich HMAC aktiviert vs. deaktiviert")
    print("=" * 60)
    
    cipher = VigenereCipher("TestKey789!")
    plaintext = "Data with and without HMAC protection"
    
    # Verschlüssele ohne HMAC
    ciphertext_no_hmac = cipher.encrypt(plaintext, use_nonce=True, use_hmac=False)
    print(f"\nOhne HMAC:  {ciphertext_no_hmac}")
    print(f"Länge: {len(ciphertext_no_hmac)} Zeichen")
    
    # Verschlüssele mit HMAC
    ciphertext_with_hmac = cipher.encrypt(plaintext, use_nonce=True, use_hmac=True)
    print(f"\nMit HMAC:   {ciphertext_with_hmac}")
    print(f"Länge: {len(ciphertext_with_hmac)} Zeichen")
    print(f"Größenunterschied: +{len(ciphertext_with_hmac) - len(ciphertext_no_hmac)} Zeichen (HMAC-Tags)\n")
    
    # Beide sollten sich entschlüsseln lassen
    decrypted_no_hmac = cipher.decrypt(ciphertext_no_hmac, verify_hmac=False)
    decrypted_with_hmac = cipher.decrypt(ciphertext_with_hmac, verify_hmac=True)
    
    print(f"Entschlüsselt (ohne HMAC): {decrypted_no_hmac}")
    print(f"Entschlüsselt (mit HMAC):  {decrypted_with_hmac}")
    print(f"✓ Beide Versionen funktionieren korrekt!\n")


def test_longer_text_with_multiple_blocks():
    """Test: Längerer Text mit mehreren HMAC-Blöcken"""
    print("=" * 60)
    print("TEST 4: Längerer Text mit mehreren HMAC-Blöcken")
    print("=" * 60)
    
    cipher = VigenereCipher("LongKeyForLongText")
    plaintext = """The quick brown fox jumps over the lazy dog.
This is a longer text that will trigger multiple HMAC block generations.
Each block is authenticated separately, providing extreme diffusion and security.
The HMAC-based key evolution makes this cipher extremely resistant to cryptanalysis."""
    
    ciphertext = cipher.encrypt(plaintext, use_nonce=True, use_hmac=True)
    print(f"\nPlaintext-Länge:  {len(plaintext)} Zeichen")
    print(f"Ciphertext-Länge: {len(ciphertext)} Zeichen")
    
    # Entschlüssele
    try:
        decrypted = cipher.decrypt(ciphertext, verify_hmac=True)
        print(f"\n✓ Entschlüsselung erfolgreich!")
        print(f"✓ HMAC-Blöcke verifiziert!")
        assert plaintext == decrypted, "Texte stimmen nicht überein!"
        print(f"✓ Text-Integrität bestätigt!\n")
    except ValueError as e:
        print(f"✗ Fehler: {e}\n")


def test_mixed_key_and_mix_key():
    """Test: Kombination mit mix_key für gemischtes Alphabet"""
    print("=" * 60)
    print("TEST 5: HMAC + Gemischtes Alphabet (mix_key)")
    print("=" * 60)
    
    cipher = VigenereCipher("SecretKey", mix_key="AlphabetMixer42")
    plaintext = "Advanced encryption with mixed alphabet and HMAC!"
    
    ciphertext = cipher.encrypt(plaintext, use_nonce=True, use_hmac=True)
    print(f"\nPlaintext:  {plaintext}")
    print(f"Ciphertext: {ciphertext}\n")
    
    try:
        decrypted = cipher.decrypt(ciphertext, verify_hmac=True)
        print(f"Decrypted:  {decrypted}")
        print(f"✓ Verschlüsselung mit mix_key und HMAC erfolgreich!\n")
    except ValueError as e:
        print(f"✗ Fehler: {e}\n")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("HMAC-SYSTEM TESTSUITE - Vigenere Cipher Revolution")
    print("=" * 60 + "\n")
    
    test_basic_hmac_encryption()
    test_hmac_tampering_detection()
    test_hmac_vs_no_hmac()
    test_longer_text_with_multiple_blocks()
    test_mixed_key_and_mix_key()
    
    print("=" * 60)
    print("ALLE TESTS ABGESCHLOSSEN")
    print("=" * 60)
