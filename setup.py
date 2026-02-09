#!/usr/bin/env python3
"""
Vigenere Cipher - Projekt Initialisierer
Überprüft die Umgebung und zeigt Starhoptions
"""

import sys
import os
from pathlib import Path


def check_python_version():
    """Überprüft, ob Python 3.7+ installiert ist"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Fehler: Python 3.7+ erforderlich")
        print(f"   Aktuelle Version: {version.major}.{version.minor}{version.micro}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} erkannt")
    return True


def check_files():
    """Überprüft, ob alle erforderlichen Dateien vorhanden sind"""
    required_files = [
        "vigenere_cipher.py",
        "vigenere_analysis.py",
        "cli.py",
        "test_vigenere.py",
        "examples.py",
        "README.md"
    ]
    
    all_present = True
    for filename in required_files:
        if Path(filename).exists():
            print(f"✅ {filename}")
        else:
            print(f"❌ {filename} - FEHLT!")
            all_present = False
    
    return all_present


def show_menu():
    """Zeigt das Startmenü"""
    print("\n" + "=" * 60)
    print("VIGENERE CIPHER - Startmenü")
    print("=" * 60 + "\n")
    
    options = [
        ("1", "Interaktive CLI starten", "python cli.py"),
        ("2", "Unit-Tests ausführen", "python test_vigenere.py"),
        ("3", "Beispiele ansehen", "python examples.py"),
        ("4", "Dokumentation lesen", "start README.md"),
        ("5", "Quick Start Anleitung", "type QUICKSTART.md"),
        ("6", "Beispiel-Eingabedatei testen", "python cli.py (dann Option 3)"),
    ]
    
    for num, desc, cmd in options:
        print(f"{num}. {desc}")
        print(f"   → {cmd}\n")


def main():
    """Hauptfunktion"""
    print("\n" + "=" * 60)
    print("Vigenere Cipher - Projektinitialisierung")
    print("=" * 60 + "\n")
    
    # Überprüfe Python-Version
    print("Überprüfe Python-Version...")
    if not check_python_version():
        sys.exit(1)
    
    # Überprüfe Dateien
    print("\nÜberprüfe erforderliche Dateien...")
    if not check_files():
        print("\n⚠️  Einige Dateien fehlen!")
        sys.exit(1)
    
    print("\n✅ Alle Überprüfungen bestanden!")
    
    # Zeige Menü
    show_menu()
    
    print("=" * 60)
    print("\nFür schnellen Start:")
    print("  → python cli.py")
    print("\nFür Entwickler:")
    print("  → from vigenere_cipher import VigenereCipher")
    print("  → cipher = VigenereCipher('KEY')")
    print("  → print(cipher.encrypt_lowercase('Hello'))")
    print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    main()
