# Vigenere Cipher - Quick Start Anleitung

## 🚀 5-Minuten-Einstieg

### Option 1: Interaktive CLI (Empfohlen für Anfänger)

```bash
python src/cli.py
```

oder via start.bat/start.sh

Wählen Sie aus dem Menü:
1. **Verschlüsseln** - Geben Sie einen Text ein
2. **Entschlüsseln** - Geben Sie Geheimtext ein
3. **Batch** - Verarbeiten Sie ganze Dateien
4. **Info** - Lernen Sie über Vigenere

### Option 2: Python-Skript (Für Entwickler)

```python
from vigenere_cipher import VigenereCipher

# Erstelle Chiffre mit Schlüssel
cipher = VigenereCipher("GEHEIM")

# Verschlüssele
geheimtext = cipher.encrypt_lowercase("Meine Nachricht")
print(geheimtext)

# Entschlüssele
original = cipher.decrypt_lowercase(geheimtext)
print(original)
```

### Option 3: Beispiele ansehen

```bash
python src/examples.py
```

Zeigt 7 verschiedene Anwendungsszenarien.

### Option 4: Tests durch starten

```bash
python src/test_vigenere.py
```

Alle 10 Unit-Tests sollten bestanden werden.

---

## 📚 Häufige Aufgaben

### Allgemeiner Text verschlüsseln

```python
from vigenere_cipher import VigenereCipher

cipher = VigenereCipher("MEINSCHLUESSEL")
text = "Das ist ein Test"
chiffrat = cipher.encrypt_lowercase(text)
print(chiffrat)  # Größe und Kleinschreibung werden beibehalten!
```

### Datei verschlüsseln (Batch-Modus)

1. Text-Datei erstellen: `meine_datei.txt`
2. `python src/cli.py` ausführen
3. Option 3 (Batch) wählen
4. Dateiname und Schlüssel eingeben
5. Ergebnis wird in `meine_datei_output.txt` gespeichert

### Text-Häufigkeit analysieren

```python
from vigenere_analysis import VigenereAnalysis

text = "Ein zu analysierender Text..."
freq = VigenereAnalysis.frequency_analysis(text)

for letter in sorted(freq.keys(), key=lambda x: freq[x], reverse=True)[:5]:
    print(f"{letter}: {freq[letter]:.1f}%")

ic = VigenereAnalysis.index_of_coincidence(text)
print(f"Index of Coincidence: {ic:.4f}")
```

### Schlüssellänge erraten (Kasiski-Analyse)

```python
from vigenere_analysis import VigenereAnalysis

ciphertext = "LONGENCRYPTEDTEXT..."
lengths = VigenereAnalysis.find_key_length(ciphertext)
print(f"Mögliche Schlüssellängen: {lengths}")
```

---

## 💡 Tipps und Tricks

### Guter Schlüssel

- ✅ Lange Schlüssel (10+ Zeichen)
- ✅ Random oder Passphrase aus mehreren Wörtern
- ✅ Mix aus verschiedenen Buchstaben
- ❌ Keine bekannten Wörter
- ❌ Keine wiederholten Buchstaben

**Beispiele:**
- `HALLO` (schlecht: kurz, bekannt)
- `MEIN_LIEBLINGS_FILM_VON_2024` (gut: lang, zufällig)
- `XYZPQRST` (gut: nicht vorhersehbar)

### Sicherheit

⚠️ **WARNUNG**: Die Vigenere-Chiffre ist **nicht sicher** gegen moderne Techniken!

Diese sind 1863 gebrochen und können mit modernen Computern in Sekunden analysiert werden.

Verwenden Sie für echte Sicherheit: **AES-256**, **RSA**, oder **TLS**

### Performance

- Kleine Texte (< 1MB): Instant
- Große Dateien (> 100MB): Wenige Sekunden
- Die Implementierung ist CPU-effizient

---

## 🔧 Fehlerbehebung

### Fehler: "Der Schlüssel muss aus Buchstaben bestehen"

**Problem**: Sie haben Zahlen oder Sonderzeichen im Schlüssel
**Lösung**: Verwenden Sie nur Buchstaben (A-Z, a-z)

```python
# ❌ Falsch
cipher = VigenereCipher("KEY123")

# ✅ Richtig
cipher = VigenereCipher("KEYTHREE")
```

### Verschlüsselte Text ist nicht lesbar

**Problem**: Das ist normal! Verschlüsselter Text sieht zufällig aus
**Lösung**: Verwenden Sie den gleichen Schlüssel zum Entschlüsseln

### Import-Fehler

Stellen Sie sicher, dass alle `.py`-Dateien im selben Verzeichnis sind:

```
Cryptology/src/
  ├── cli.py
  ├── examples.py
  ├── test_vigenere.py
  ├── vigenere_cipher.py
  └── vigenere_analysis.py
```

---

## 📖 Dateien-Übersicht

| Datei | Zweck |
|-------|-------|
| `vigenere_cipher.py` | Kern-Implementierung |
| `vigenere_analysis.py` | Kryptoanalyse-Tools |
| `cli.py` | Interaktives Programm |
| `test_vigenere.py` | Unit-Tests (10) |
| `examples.py` | 7 Demonstrationen |
| `README.md` | Ausführliche Dokumentation |
| `QUICKSTART.md` | Diese Datei |
| `sample_input.txt` | Beispiel-Eingabedatei |

---

## 🎯 Nächste Schritte

1. **Anfänger**: `python src/cli.py` ausführen und spielen
2. **Entwickler**: Code in `vigenere_cipher.py` studieren
3. **Interessiert**: `README.md` für Mathematik lesen
4. **Sicherheitsorientiert**: `vigenere_analysis.py` erkunden

---

## ❓ FAQ

**F: Kann ich diesen Code für Schulprojekte verwenden?**
A: Ja! Das ist genau der Zweck. Alles ist Open Source.

**F: Ist es schnell genug für große Dateien?**
A: Ja, mehrere MB pro Sekunde möglich.

**F: Kann ich den Code in meinem Projekt verwenden?**
A: Ja, alle Dateien sind frei verwendbar.

**F: Was ist besser: kurzer oder langer Schlüssel?**
A: Länger ist besser! Minimum 8, ideal 16+ Zeichen.

**F: Geschwindigkeit: encrypt vs decrypt?**
A: Identisch - beide sind $O(n)$.

---

## 🌟 Weitere Krypto-Projekte zum Lernen

- Caesar Cipher (einfacher)
- Playfair Cipher (komplexer)
- Substitution Cipher (ähnlich)
- One-Time Pad (perfekt sicher, aber impraktisch)
- Enigma Machine (historisch interessant)

---

Viel Spaß beim Verschlüsseln! 🔐
