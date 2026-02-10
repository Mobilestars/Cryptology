"""
Erweiterte Kryptoanalyse-Tools für Vigenere-Chiffre
Funktionen zum Brechen und Analysieren der Vigenere-Verschlüsselung
"""

from collections import Counter
from math import gcd
from functools import reduce
from vigenere_cipher import VigenereCipher


class VigenereAnalysis:
    """Werkzeuge zur Kryptoanalyse der Vigenere-Chiffre"""
    
    @staticmethod
    def frequency_analysis(text: str) -> dict:
        """
        Führt eine Häufigkeitsanalyse durch.
        
        Args:
            text: Der zu analysierende Text
            
        Returns:
            Ein Dictionary mit Buchstaten und ihren Häufigkeiten
        """
        text = text.upper().replace(" ", "").replace("\n", "")
        text = ''.join(c for c in text if c.isalpha())
        
        letter_count = Counter(text)
        total = len(text)
        
        frequency = {
            letter: (count / total * 100)
            for letter, count in sorted(letter_count.items())
        }
        
        return frequency
    
    @staticmethod
    def index_of_coincidence(text: str) -> float:
        """
        Berechnet den Index of Coincidence (IC) eines Textes.
        Der IC hilft bei der Bestimmung der Schlüssellänge.
        
        Args:
            text: Der zu analysierende Text
            
        Returns:
            Der Index of Coincidence (Wert zwischen 0 und 1)
        """
        text = text.upper().replace(" ", "").replace("\n", "")
        text = ''.join(c for c in text if c.isalpha())
        
        if len(text) <= 1:
            return 0.0
        
        letter_count = Counter(text)
        n = len(text)
        
        ic = sum(count * (count - 1) for count in letter_count.values()) / (n * (n - 1))
        return ic
    
    @staticmethod
    def find_key_length(ciphertext: str, max_length: int = 20) -> list:
        """
        Versucht, die Schlüssellänge mit der Kasiski-Methode zu bestimmen.
        
        Args:
            ciphertext: Der verschlüsselte Text
            max_length: Maximale zu testende Schlüssellänge
            
        Returns:
            Eine Liste mit wahrscheinlichen Schlüssellängen
        """
        ciphertext = ciphertext.upper().replace(" ", "").replace("\n", "")
        
        # Suche nach wiederholten Sequenzen (3er und 4er)
        distances = []
        
        for seq_len in [3, 4]:
            for i in range(len(ciphertext) - seq_len):
                seq = ciphertext[i:i+seq_len]
                for j in range(i + seq_len, len(ciphertext) - seq_len + 1):
                    if ciphertext[j:j+seq_len] == seq:
                        distances.append(j - i)
        
        if not distances:
            return []
        
        # Berechne GCD aller Distanzen
        common_divisor = reduce(gcd, distances)
        
        # Finde alle Teiler des GCD
        divisors = []
        for i in range(2, min(common_divisor + 1, max_length + 1)):
            if common_divisor % i == 0:
                divisors.append(i)
        
        return sorted(divisors)
    
    @staticmethod
    def chi_squared_test(observed: dict, expected: dict) -> float:
        """
        Berechnet die Chi-Quadrat-Statistik zwischen zwei Häufigkeitsverteilungen.
        
        Args:
            observed: Beobachtete Häufigkeitsverteilung
            expected: Erwartete Häufigkeitsverteilung
            
        Returns:
            Der Chi-Quadrat-Wert (niedriger = besser)
        """
        chi_squared = 0.0
        
        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            obs = observed.get(letter, 0)
            exp = expected.get(letter, 0.1)  # Vermeidung von Division durch Null
            
            if exp > 0:
                chi_squared += ((obs - exp) ** 2) / exp
        
        return chi_squared
    
    @staticmethod
    def attack_single_char(ciphertext: str, position: int, expected_freq: dict) -> str:
        """
        Führt einen Angriff auf einen einzelnen Zeichensatz durch (mit bekannter Häufigkeit).
        
        Args:
            ciphertext: Der verschlüsselte Text
            position: Position im wiederholten Schlüssel
            expected_freq: Erwartete Häufigkeitsverteilung (z.B. Deutsch)
            
        Returns:
            Der wahrscheinlichste Schlüsselbuchstabe
        """
        ciphertext = ciphertext.upper()
        
        # Extrahiere alle Zeichen an Position (position mod Schlüssellänge)
        subset = ""
        idx = position
        while idx < len(ciphertext):
            if ciphertext[idx].isalpha():
                subset += ciphertext[idx]
            idx += 1
        
        if not subset:
            return ""
        
        best_key = None
        best_chi_squared = float('inf')
        
        # Probiere alle möglichen Schlüsselbuchstaben (A-Z)
        for shift in range(26):
            # Entschlüsseln mit diesem Shift
            decrypted = ""
            for char in subset:
                decrypted += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            
            # Häufigkeitsanalyse
            freq = VigenereAnalysis.frequency_analysis(decrypted)
            
            # Chi-Quadrat-Test
            chi_sq = VigenereAnalysis.chi_squared_test(freq, expected_freq)
            
            if chi_sq < best_chi_squared:
                best_chi_squared = chi_sq
                best_key = chr(shift + ord('A'))
        
        return best_key
    
    @staticmethod
    def analyze_text(text: str):
        """
        Führt eine vollständige Analyse eines verschlüsselten Textes durch.
        
        Args:
            text: Der zu analysierende Text
        """
        print("\n=== VIGENERE-ANALYSE ===\n")
        
        # Index of Coincidence
        ic = VigenereAnalysis.index_of_coincidence(text)
        print(f"Index of Coincidence: {ic:.4f}")
        print("(Englisch ≈ 0.065, Deutsch ≈ 0.073, Zufallstext ≈ 0.038)")
        
        # Häufigkeitsanalyse
        print("\n--- Häufigkeitsanalyse ---")
        freq = VigenereAnalysis.frequency_analysis(text)
        for letter in sorted(freq.keys()):
            print(f"{letter}: {freq[letter]:>6.2f}%")
        
        # Kasiski-Analyse
        print("\n--- Kasiski-Analyse ---")
        key_lengths = VigenereAnalysis.find_key_length(text)
        if key_lengths:
            print(f"Wahrscheinliche Schlüssellängen: {key_lengths[:5]}")
        else:
            print("Keine wiederholten Sequenzen gefunden")


# Standard-Häufigkeitsverteilung für Deutsch
GERMAN_FREQUENCY = {
    'A': 6.51, 'B': 1.89, 'C': 3.06, 'D': 5.08, 'E': 17.40, 'F': 1.66,
    'G': 3.01, 'H': 4.76, 'I': 7.55, 'J': 0.27, 'K': 1.21, 'L': 3.44,
    'M': 2.53, 'N': 9.78, 'O': 2.51, 'P': 0.79, 'Q': 0.02, 'R': 7.00,
    'S': 7.27, 'T': 6.15, 'U': 4.35, 'V': 0.67, 'W': 1.89, 'X': 0.03,
    'Y': 0.04, 'Z': 1.13
}

# Standard-Häufigkeitsverteilung für Englisch
ENGLISH_FREQUENCY = {
    'A': 8.17, 'B': 1.29, 'C': 2.78, 'D': 4.25, 'E': 12.70, 'F': 2.23,
    'G': 2.02, 'H': 6.09, 'I': 7.00, 'J': 0.15, 'K': 0.77, 'L': 4.03,
    'M': 2.41, 'N': 6.75, 'O': 7.51, 'P': 1.93, 'Q': 0.10, 'R': 5.99,
    'S': 6.33, 'T': 9.06, 'U': 2.76, 'V': 0.98, 'W': 2.36, 'X': 0.15,
    'Y': 1.97, 'Z': 0.07
}
