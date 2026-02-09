"""
Command-Line Interface für die Vigenere-Verschlüsselung
Interaktives Terminal-Programm zum Verschlüsseln und Entschlüsseln
"""

import sys
from vigenere_cipher import VigenereCipher


def print_banner():
    """Zeigt den Programm-Header"""
    print("\n" + "=" * 60)
    print("  VIGENERE CIPHER - Verschlüsselungsittel")
    print("=" * 60 + "\n")


def print_menu():
    """Zeigt das Hauptmenü"""
    print("\nWählen Sie eine Option:")
    print("1. Text verschlüsseln")
    print("2. Text entschlüsseln")
    print("3. Batch-Datei verarbeiten")
    print("4. Informationen anzeigen")
    print("5. Programmende")
    print("-" * 40)


def encrypt_mode():
    """Modus zum Verschlüsseln von Text"""
    print("\n--- VERSCHLÜSSELUNGSMODUS ---")
    
    try:
        key = input("Geben Sie den Schlüssel ein: ").strip()
        if not key:
            print("Fehler: Schlüssel kann nicht leer sein!")
            return
        
        cipher = VigenereCipher(key)
        plaintext = input("Geben Sie den zu verschlüsselnden Text ein: ").strip()
        
        if not plaintext:
            print("Fehler: Text kann nicht leer sein!")
            return
        
        ciphertext = cipher.encrypt_lowercase(plaintext)
        
        print("\n" + "-" * 40)
        print(f"Klartext:    {plaintext}")
        print(f"Schlüssel:   {key}")
        print(f"Geheimtext:  {ciphertext}")
        print("-" * 40)
        
    except ValueError as e:
        print(f"Fehler: {e}")


def decrypt_mode():
    """Modus zum Entschlüsseln von Text"""
    print("\n--- ENTSCHLÜSSELUNGSMODUS ---")
    
    try:
        key = input("Geben Sie den Schlüssel ein: ").strip()
        if not key:
            print("Fehler: Schlüssel kann nicht leer sein!")
            return
        
        cipher = VigenereCipher(key)
        ciphertext = input("Geben Sie den zu entschlüsselnden Text ein: ").strip()
        
        if not ciphertext:
            print("Fehler: Text kann nicht leer sein!")
            return
        
        plaintext = cipher.decrypt_lowercase(ciphertext)
        
        print("\n" + "-" * 40)
        print(f"Geheimtext:  {ciphertext}")
        print(f"Schlüssel:   {key}")
        print(f"Klartext:    {plaintext}")
        print("-" * 40)
        
    except ValueError as e:
        print(f"Fehler: {e}")


def batch_mode():
    """Modus zur Verarbeitung mehrerer Texte"""
    print("\n--- BATCH-MODUS ---")
    
    try:
        key = input("Geben Sie den Schlüssel ein: ").strip()
        if not key:
            print("Fehler: Schlüssel kann nicht leer sein!")
            return
        
        cipher = VigenereCipher(key)
        
        filename = input("Geben Sie die Eingabedatei an: ").strip()
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            encrypt_or_decrypt = input("Verschlüsseln (1) oder Entschlüsseln (2)? ").strip()
            
            output_filename = filename.rsplit('.', 1)[0] + "_output.txt"
            
            with open(output_filename, 'w', encoding='utf-8') as f:
                for line in lines:
                    text = line.strip()
                    if text:
                        if encrypt_or_decrypt == "1":
                            result = cipher.encrypt_lowercase(text)
                        else:
                            result = cipher.decrypt_lowercase(text)
                        f.write(result + "\n")
            
            print(f"\nErgebnis in '{output_filename}' gespeichert!")
            
        except FileNotFoundError:
            print(f"Fehler: Datei '{filename}' nicht gefunden!")
        except IOError as e:
            print(f"Fehler beim Lesen/Schreiben der Datei: {e}")
            
    except ValueError as e:
        print(f"Fehler: {e}")


def show_info():
    """Zeigt Informationen über die Vigenere-Chiffre"""
    info_text = """
    --- INFORMATIONEN ZUR VIGENERE-CHIFFRE ---
    
    Die Vigenere-Chiffre ist ein polyalphabetisches Substitutionsverfahren,
    das 1553 von Giambattista della Porta beschrieben wurde.
    
    FUNKTIONSWEISE:
    - Ein Schlüsselwort wird verwendet, um mehrere Caesar-Verschiebungen zu kombinieren
    - Jeder Buchstabe wird um einen anderen Betrag verschoben
    - Der Betrag wird durch den entsprechenden Buchstaben des Schlüssels bestimmt
    
    BEISPIEL:
    Klartext:    H E L L O W O R L D
    Schlüssel:   K E Y K E Y K E Y K
    Geheimtext:  R I F V S U Y V J N
    
    SICHERHEIT:
    - Die Vigenere-Chiffre war lange Zeit sehr sicher
    - Wurde 1863 von Friedrich Kasiski gebrochen
    - Ist heute nur noch für Lernzwecke relevant
    
    VORTEILE:
    - Einfach zu verstehen und implementieren
    - Beständig gegen Häufigkeitsanalyse (wenn Schlüssel lang)
    
    NACHTEILE:
    - Anfällig für Kasiski-Analyse und Friedman-Test
    - Nicht sicher gegen moderne Kryptanalyse
    - Schlüsselmanagement ist schwierig
    """
    print(info_text)


def main():
    """Hauptprogramm"""
    print_banner()
    
    while True:
        print_menu()
        choice = input("Eingabe: ").strip()
        
        if choice == "1":
            encrypt_mode()
        elif choice == "2":
            decrypt_mode()
        elif choice == "3":
            batch_mode()
        elif choice == "4":
            show_info()
        elif choice == "5":
            print("\nAuf Wiedersehen!\n")
            sys.exit(0)
        else:
            print("Ungültige Eingabe! Bitte wählen Sie 1-5.")


if __name__ == "__main__":
    main()
