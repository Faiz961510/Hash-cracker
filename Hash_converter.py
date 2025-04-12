import hashlib
import itertools
import string
from typing import Optional

class HashCracker:
    def __init__(self):
        self.common_passwords = [
            "password", "123456", "123456789", "12345", "qwerty",
            "password1", "12345678", "111111", "123123", "1234567890",
            "admin", "welcome", "monkey", "sunshine", "password123"
        ]
    
    def hash_string(self, text: str, algorithm: str = "md5") -> str:
        """Hash a string using the specified algorithm."""
        hash_func = getattr(hashlib, algorithm.lower(), None)
        if not hash_func:
            raise ValueError(f"Unsupported hash algorithm: {algorithm}")
        return hash_func(text.encode()).hexdigest()
    
    def crack_hash(self, target_hash: str, algorithm: str = "md5", 
                   max_length: int = 6, charset: str = string.ascii_lowercase + string.digits,
                   use_dictionary: bool = True) -> Optional[str]:
        """
        Attempt to crack a hash using various methods.
        
        Args:
            target_hash: The hash to crack
            algorithm: Hash algorithm to use (md5, sha1, sha256, etc.)
            max_length: Maximum length for brute-force attempts
            charset: Character set to use for brute-force
            use_dictionary: Whether to try dictionary attack first
            
        Returns:
            The plaintext if found, otherwise None
        """
        # First try common passwords
        if use_dictionary:
            for word in self.common_passwords:
                if self.hash_string(word, algorithm) == target_hash:
                    return word
        
        # Then try brute-force
        for length in range(1, max_length + 1):
            for attempt in itertools.product(charset, repeat=length):
                attempt_str = ''.join(attempt)
                if self.hash_string(attempt_str, algorithm) == target_hash:
                    return attempt_str
        
        return None

def main():
    print("Hash to Plaintext Converter Tool")
    print("--------------------------------")
    
    cracker = HashCracker()
    
    while True:
        print("\nOptions:")
        print("1. Crack a hash")
        print("2. Hash a string")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == "1":
            target_hash = input("Enter the hash to crack: ").strip()
            algorithm = input("Enter hash algorithm (md5, sha1, sha256, etc.): ").strip().lower()
            
            print("\nAttempting to crack hash...")
            result = cracker.crack_hash(target_hash, algorithm)
            
            if result:
                print(f"\nSuccess! Plaintext found: {result}")
            else:
                print("\nFailed to crack the hash. Try a more comprehensive dictionary or longer brute-force.")
        
        elif choice == "2":
            text = input("Enter text to hash: ").strip()
            algorithm = input("Enter hash algorithm (md5, sha1, sha256, etc.): ").strip().lower()
            
            try:
                hashed = cracker.hash_string(text, algorithm)
                print(f"\n{algorithm.upper()} hash of '{text}': {hashed}")
            except ValueError as e:
                print(f"\nError: {e}")
        
        elif choice == "3":
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
