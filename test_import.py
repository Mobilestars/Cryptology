import sys
from pathlib import Path

sys.path.insert(0, 'src')
from cli import load_config, save_config

print("CLI Module erfolgreich importiert")
cfg = load_config()
print(f"Config geladen: nonce_length={cfg.get('nonce_length', 16)}")
print(f"  hmac_block_size={cfg.get('hmac_block_size', 8)}")
print(f"  hmac_tag_length={cfg.get('hmac_tag_length', 12)}")
print("\nAlles funktioniert korrekt!")
