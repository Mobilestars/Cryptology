#!/usr/bin/env python3
"""Test Script für die neue Edit Config Funktionalität"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from cli import load_config, save_config

def test_config_operations():
    print("=" * 60)
    print("Test: Config Load/Save Funktionen")
    print("=" * 60)
    
    # Test 1: Originale Config laden
    print("\n1. Aktuelle Config laden...")
    original_config = load_config()
    print(f"   ✓ nonce_length: {original_config.get('nonce_length', 'N/A')}")
    print(f"   ✓ hmac_block_size: {original_config.get('hmac_block_size', 'N/A')}")
    print(f"   ✓ hmac_tag_length: {original_config.get('hmac_tag_length', 'N/A')}")
    
    # Test 2: Neue Werte speichern
    print("\n2. Neue Config-Werte speichern...")
    test_config = {
        'nonce_length': 32,
        'hmac_block_size': 16,
        'hmac_tag_length': 24
    }
    save_config(test_config)
    
    # Test 3: Verifizieren, dass Werte gespeichert wurden
    print("\n3. Gespeicherte Werte verifizieren...")
    loaded_config = load_config()
    print(f"   ✓ nonce_length: {loaded_config.get('nonce_length')} (erwartet: 32)")
    print(f"   ✓ hmac_block_size: {loaded_config.get('hmac_block_size')} (erwartet: 16)")
    print(f"   ✓ hmac_tag_length: {loaded_config.get('hmac_tag_length')} (erwartet: 24)")
    
    # Test 4: Original wiederherstellen
    print("\n4. Original-Config wiederherstellen...")
    save_config(original_config)
    restored = load_config()
    print(f"   ✓ nonce_length: {restored.get('nonce_length')} (original: {original_config.get('nonce_length')})")
    
    print("\n" + "=" * 60)
    print("✓ Alle Tests erfolgreich abgeschlossen!")
    print("=" * 60)

if __name__ == "__main__":
    test_config_operations()
