"""
Beispiele und Demonstrationen für die Vigenere-Verschlüsselung
"""

from vigenere_cipher import VigenereCipher
from vigenere_analysis import VigenereAnalysis, GERMAN_FREQUENCY, ENGLISH_FREQUENCY


def example_basic_usage():
    """Grundlegende Verwendung der Vigenere-Chiffre"""
    print("=" * 60)
    print("BEISPIEL 1: Grundlegende Verwendung")
    print("=" * 60)
    
    # Erstelle eine Chiffre mit dem Schlüssel "GEHEIM"
    cipher = VigenereCipher("GEHEIM")
    
    # Verschlüssele einen Text
    plaintext = "Das ist eine geheime Nachricht"
    ciphertext = cipher.encrypt_lowercase(plaintext)
    
    print(f"\nKlartext:    {plaintext}")
    print(f"Schlüssel:   GEHEIM")
    print(f"Geheimtext:  {ciphertext}")
    
    # Entschlüssele den Text
    decrypted = cipher.decrypt_lowercase(ciphertext)
    print(f"Entschlüsselt: {decrypted}")
    print()


def example_different_keys():
    """Demonstriert, wie unterschiedliche Schlüssel unterschiedliche Ergebnisse liefern"""
    print("=" * 60)
    print("BEISPIEL 2: Verschiedene Schlüssel")
    print("=" * 60)
    
    plaintext = "HELLO"
    
    keys = ["KEY", "SECRET", "VERYLONGKEY", "A"]
    
    print(f"\nKlartext: {plaintext}\n")
    
    for key in keys:
        cipher = VigenereCipher(key)
        ciphertext = cipher.encrypt(plaintext)
        print(f"Schlüssel: {key:<15} -> Geheimtext: {ciphertext}")
    
    print()


def example_historical():
    """Historisches Beispiel aus Wikipedia"""
    print("=" * 60)
    print("BEISPIEL 3: Historisches Beispiel")
    print("=" * 60)
    
    cipher = VigenereCipher("VIGENERECIPHER")
    
    plaintext = "ATTACKATDAWN"
    expected = "LXFOPVEFRNHR"
    
    ciphertext = cipher.encrypt(plaintext)
    
    print(f"\nKlartext:          {plaintext}")
    print(f"Schlüssel:         VIGENERECIPHER")
    print(f"Erwarteter Text:   {expected}")
    print(f"Berechnet:         {ciphertext}")
    print(f"Korrekt:           {ciphertext == expected}")
    
    # Entschlüsselung
    decrypted = cipher.decrypt(expected)
    print(f"Entschlüsselt:     {decrypted}")
    print()


def example_case_handling():
    """Demonstriert die Behandlung von Groß-/Kleinschreibung"""
    print("=" * 60)
    print("BEISPIEL 4: Groß- und Kleinschreibung")
    print("=" * 60)
    
    cipher = VigenereCipher("SCHLUESSEL")
    
    texts = [
        "Hallo Welt",
        "ALLESMAJUSKEL",
        "alleskeinbuchstabe",
        "MiScHeD CaSe MiT PuNkTuAtIoN!"
    ]
    
    print()
    for text in texts:
        encrypted = cipher.encrypt_lowercase(text)
        decrypted = cipher.decrypt_lowercase(encrypted)
        
        print(f"Original:      {text}")
        print(f"Verschlüsselt: {encrypted}")
        print(f"Entschlüsselt: {decrypted}")
        print(f"Korrekt:       {text == decrypted}\n")


def example_frequency_analysis():
    """Demonstriert die Häufigkeitsanalyse"""
    print("=" * 60)
    print("BEISPIEL 5: Häufigkeitsanalyse")
    print("=" * 60)
    
    # Ein längerer Text auf Deutsch
    german_text = """
    Die Vigenere-Chiffre ist ein polyalphabetisches Verschlüsselungsverfahren,
    das einen Schlüsseltext verwendet. Sie wurde von Giambattista della Porta
    beschrieben und nach Blaise de Vigenere benannt. Die Chiffre gilt as eine
    der sichereren klassischen Verschlüsselungsmethoden, da sie gegen einfache
    Häufigkeitsanalysen resistent ist.
    """
    
    print("\nHäufigkeitsanalyse des deutschen Texts:")
    print("-" * 40)
    
    freq = VigenereAnalysis.frequency_analysis(german_text)
    
    for letter in sorted(freq.keys(), key=lambda x: freq[x], reverse=True)[:10]:
        print(f"{letter}: {freq[letter]:>6.2f}%")
    
    # Index of Coincidence
    ic = VigenereAnalysis.index_of_coincidence(german_text)
    print(f"\nIndex of Coincidence: {ic:.4f}")
    print("(Deutsch ≈ 0.073)")
    print()


def example_kasiski_analysis():
    """Demonstriert die Kasiski-Analyse"""
    print("=" * 60)
    print("BEISPIEL 6: Kasiski-Analyse und Schlüssellängenerkennung")
    print("=" * 60)
    
    # Verschlüssele einen langen Text mit bekanntem Schlüssel
    cipher = VigenereCipher("SECRET")
    
    plaintext = """
    Der Vigenere Chiffre ist sehr interessant und wichtig in der Geschichte
    der Kryptographie. Sie wurde lange Zeit als sicher angesehen, bis Friedrich
    Kasiski sie 1863 erfolgreich zur Kryptoanalyse einsetzte. Die Kasiski-Analyse
    nutzt wiederholte Sequenzen um die Schlüssellänge zu bestimmen.
    """ * 3  # Wiederhole für längeren Text
    
    ciphertext = cipher.encrypt_lowercase(plaintext)
    
    print(f"\nVerschlüsselter Text: {ciphertext[:100]}...")
    print(f"\nAnalysiere Schlüssellänge (echter Schlüssel: 'SECRET')...")
    
    key_lengths = VigenereAnalysis.find_key_length(ciphertext, max_length=15)
    
    if key_lengths:
        print(f"Erkannte wahrscheinliche Schlüssellängen: {key_lengths[:5]}")
        print(f"Tatsächliche Schlüssellänge: 6")
        print(f"6 erkannt: {6 in key_lengths}")
    else:
        print("Keine wiederholten Sequenzen gefunden")
    
    print()


def example_special_characters():
    """Demonstriert die Verarbeitung von Sonderzeichen"""
    print("=" * 60)
    print("BEISPIEL 7: Sonderzeichen und Zahlen")
    print("=" * 60)
    
    cipher = VigenereCipher("PASSWORD")
    
    texts = [
        "Hello, World!",
        "12345 mit Text",
        "Preis: 99,99 Euro",
        "Email: test@example.com"
    ]
    
    print()
    for text in texts:
        encrypted = cipher.encrypt_lowercase(text)
        decrypted = cipher.decrypt_lowercase(encrypted)
        
        print(f"Original:      {text}")
        print(f"Verschlüsselt: {encrypted}")
        print(f"Entschlüsselt: {decrypted}")
        print(f"Korrekt:       {text == decrypted}\n")


def run_all_examples():
    """Führt alle Beispiele aus"""
    example_basic_usage()
    example_different_keys()
    example_historical()
    example_case_handling()
    example_frequency_analysis()
    example_kasiski_analysis()
    example_special_characters()
    
    print("=" * 60)
    print("Alle Beispiele abgeschlossen!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_examples()
