import sys
from pathlib import Path
from vigenere_cipher import VigenereCipher


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)


def print_banner():
    print("\n" + "=" * 60)
    print("  VIGENERE CIPHER - Verschlüsselungsittel")
    print("=" * 60 + "\n")


def print_menu():
    print("\nWählen Sie eine Option:")
    print("1. Text verschlüsseln")
    print("2. Text entschlüsseln")
    print("3. Batch-Datei verarbeiten")
    print("4. Informationen anzeigen")
    print("5. Programmende")
    print("-" * 40)


def encrypt_mode():
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
    print("\n--- BATCH-MODUS ---")

    try:
        key = input("Geben Sie den Schlüssel ein: ").strip()
        if not key:
            print("Fehler: Schlüssel kann nicht leer sein!")
            return

        cipher = VigenereCipher(key)
        filename = input("Geben Sie die Eingabedatei an: ").strip()

        input_path = DATA_DIR / filename
        output_path = DATA_DIR / f"{input_path.stem}_output.txt"

        with input_path.open("r", encoding="utf-8") as f:
            lines = f.readlines()

        mode = input("Verschlüsseln (1) oder Entschlüsseln (2)? ").strip()

        with output_path.open("w", encoding="utf-8") as f:
            for line in lines:
                text = line.strip()
                if not text:
                    continue
                if mode == "1":
                    result = cipher.encrypt_lowercase(text)
                else:
                    result = cipher.decrypt_lowercase(text)
                f.write(result + "\n")

        print(f"\nErgebnis in '{output_path}' gespeichert!")

    except FileNotFoundError:
        print("Fehler: Eingabedatei nicht gefunden!")
    except ValueError as e:
        print(f"Fehler: {e}")
    except IOError as e:
        print(f"Dateifehler: {e}")


def show_info():
    print("""
--- INFORMATIONEN ZUR VIGENERE-CHIFFRE ---

Die Vigenere-Chiffre ist ein polyalphabetisches Substitutionsverfahren,
das 1553 von Giambattista della Porta beschrieben wurde.

FUNKTIONSWEISE:
- Kombination mehrerer Caesar-Verschiebungen
- Schlüssel bestimmt die Verschiebung je Zeichen

SICHERHEIT:
- Historisch relevant
- Heute kryptographisch unsicher
""")


def main():
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
