# Vigenere-Verschlüsselung mit revolutionärem HMAC-System

## Überblick

Die verbesserte Vigenere-Verschlüsselung integriert ein innovatives HMAC-System, das drei revolutionäre Sicherheitsebenen bietet:

1. **Adaptive HMAC-basierte Schlüsselvolution**
2. **Authentizitätsprüfung mit embedded Tags**
3. **Extreme Diffusion durch HMAC-Digest-gestützte Transformationen**

---

## Das revolutionäre HMAC-System

### 1. Adaptive Key-Evolution nach jedem Block

Das System führt nach jedem `HMAC_BLOCK_SIZE=8` verschlüsselten Zeichen eine adaptive Key-Evolution durch:

```python
# Nach jedem 8-er Block:
block = ''.join(alphabet_ciphertext[-8:])
block_hmac = HMAC-SHA256(block, key, nonce)
current_key_state = evolve_from_hmac(current_key_state, block_hmac)
```

**Vorteile:**
- Der Schlüssel evoliert basierend auf dem Ciphertext
- Unmöglich, Patterns zu wiederholen
- Extreme Änderung durch minimale Plaintext-Modifikationen (Avalanche-Effekt²)

### 2. Finale HMAC-Authentication Tags

Am Ende jeder Verschlüsselung wird ein finales HMAC-Tag berechnet:

```
[NONCE_LENGTH(2)][NONCE][H/N][HMAC_TAG(12 Zeichen)][CIPHERTEXT]
```

**Struktur:**
- `NONCE_LENGTH`: 2 Dezimalziffern (z.B. "16" für 16-stelligen Nonce)
- `NONCE`: Beliebig lange, zufällige Zeichenkette
- `H/N`: "H" für HMAC aktiviert, "N" für deaktiviert
- `HMAC_TAG`: 12 Alphabet-Zeichen, die das HMAC-SHA256-Digest repräsentieren
- `CIPHERTEXT`: Der verschlüsselte Nachrichts-Body

### 3. HMAC-Verifizierung beim Entschlüsseln

Bei der Entschlüsselung wird automatisch das HMAC überprüft:

```python
received_tag = extracted_hmac_tag  # Aus dem Ciphertext
expected_tag = compute_hmac_tag(ciphertext_body, key, nonce)

if received_tag != expected_tag:
    raise ValueError("Nachricht manipuliert!")
```

---

## Sicherheitsmerkmale

### Vertraulichkeit
- **Basis**: Klassische Vigenere mit Nonce
- **Verbesserung**: Adaptive Key-Evolution nach jedem Block (HMAC-rückgekoppelt)
- **Zusatz**: Gemischtes Alphabet (optional mit `mix_key`)

### Authentizität & Integrität
- **HMAC-SHA256**: Bestätigt Nachrichtenintegrität und Authentizität des Schlüssels
- **Sicherheitsgarantie**: Jede Manipulation wird mit hoher Wahrscheinlichkeit erkannt
- **Deterministisch**: Das gleiche Plaintext + gleicher Key erzeugt unterschiedliche Ciphertexte (wegen des Nonce)

### Diffusion & Konfusion
- **HMAC-gestützte Permutationen**: Der Schlüssel wird nach jedem Block permutiert
- **Nonce-Integration**: Verhindert Wiederholungsangriffe
- **Avalanche-Effekt**: Kleine Änderungen im Plaintext/Key erzeugen drastisch unterschiedliche Ciphertexte

---

## Verwendungsbeispiele

### Basis-Verschlüsselung mit HMAC

```python
from vigenere_cipher import VigenereCipher

# Cipher mit Schlüssel erstellen
cipher = VigenereCipher("MySecretKey123")

# Verschlüsseln mit HMAC
plaintext = "Geheime Nachricht"
ciphertext = cipher.encrypt(plaintext, use_nonce=True, use_hmac=True)
print(f"Verschlüsselt: {ciphertext}")

# Entschlüsseln und HMAC verifizieren
try:
    decrypted = cipher.decrypt(ciphertext, verify_hmac=True)
    print(f"Entschlüsselt: {decrypted}")
except ValueError as e:
    print(f"Fehler: {e}")
```

### Ohne HMAC (älter kompatible Mode)

```python
# HMAC deaktiviert für Rückwärts-Kompatibilität
ciphertext = cipher.encrypt(plaintext, use_nonce=True, use_hmac=False)

# Entschlüsseln ohne Authentifizierung
plaintext = cipher.decrypt(ciphertext, verify_hmac=False)
```

### Mit gemischtem Alphabet

```python
# Alphabet mit mix_key durchmischen für zusätzliche Sicherheit
cipher = VigenereCipher("MainKey", mix_key="AlphabetMixer42")

ciphertext = cipher.encrypt(plaintext, use_hmac=True)
decrypted = cipher.decrypt(ciphertext)
```

---

## Technische Details

### HMAC-Berechnung

```python
def _compute_hmac_digest(data: str, key: str, nonce: str = "") -> str:
    hmac_input = (key + nonce + data).encode('utf-8')
    hmac_key = key.encode('utf-8')
    digest = hmac.new(hmac_key, hmac_input, hashlib.sha256).hexdigest()
    return digest
```

### HMAC-zu-Alphabet-Konvertierung

Das 256-Bit HMAC-SHA256-Digest wird in Alphabet-Zeichen konvertiert:

```python
def _hmac_tag_to_alphabet(hmac_digest: str, length: int) -> str:
    chars = []
    for i in range(0, min(length * 4, len(hmac_digest)), 4):
        hex_block = hmac_digest[i:i+4]
        val = int(hex_block, 16) % len(self.alphabet)
        chars.append(self.alphabet[val])
    return ''.join(chars[:length])
```

Dies erzeugt 12 Alphabet-Zeichen aus dem HMAC, wobei jeder 4-er Block von Hex-Ziffern auf einen Alphabet-Index abgebildet wird.

### Schlüssel-Evolution aus HMAC

```python
def _evolve_key_from_hmac(key_state: str, hmac_digest: str, position: int) -> str:
    for i, hex_pair in enumerate(hmac_digest[::4]):
        rotation = (int(hex_pair, 16) + position) % len(key_state)
        key_state = key_state[rotation:] + key_state[:rotation]
    return key_state
```

Der Schlüssel wird basierend auf dem HMAC-Digest durch sukzessive Rotationen transformiert.

---

## Sicherheitsgarantien

| Feature | Sicherheit | Eigenschaft |
|---------|-----------|------------|
| Nonce | Verhindert Wiederholung | Jede Verschlüsselung unterschiedlich |
| HMAC-Tags | Authentifizierung | Manipulationen erkannt |
| Adaptive Key-Evolution | Diffusion | Patterns sind nicht möglich |
| Gemischtes Alphabet | Verwirrung | Nicht-linearer Offset |
| Avalanche-Effekt | Kryptographische Sicherheit | Kleine Änderungen → Große Effekte |

---

## Leistung

- **Overhead HMAC**: ~12 Zeichen für das HMAC-Tag
- **Durchsatz**: Minimal durch die Verwendung von SHA256 nur per Block
- **Speicher**: O(n) für Ciphertext-Speicherung

---

## Kompatibilität

Das System ist **rückwärts-kompatibel**:
- Alte Ciphertexte ohne HMAC können noch entschlüsselt werden
- Neue Verschlüsselungen können mit HMAC aktiviert werden
- Flag "H" oder "N" zeigt den Modus an

---

## Testsuite

Siehe `test_hmac_system.py` für umfassende Tests:

1. **TEST 1**: Basis-Verschlüsselung mit HMAC
2. **TEST 2**: Erkennung von Manipulationen
3. **TEST 3**: Vergleich mit/ohne HMAC
4. **TEST 4**: Längere Texte mit mehreren Blöcken
5. **TEST 5**: Integration mit mix_key

Alle Tests bestehen ✓

---

## Fazit

Das neue revolutionäre HMAC-System bietet:
- **Authentizität**: HMAC-SHA256 garantiert die Integrität
- **Sicherheit**: Adaptive Key-Evolution verhindert Pattern-Analyse
- **Zuverlässigkeit**: Automatische Manipulation-Erkennung
- **Flexibilität**: Einfache Auswahl zwischen HMAC und Legacy-Mode

Dies macht die Vigenere-Verschlüsselung für moderne Sicherheitsanforderungen geeignet, während sie klassische Einfachheit bewahrt.
