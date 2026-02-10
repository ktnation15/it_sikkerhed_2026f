"""
Security Validators - Boundary Value Testing Examples
Dette modul indeholder fire klassiske sikkerhedsvalidatorer til grænseværditestning.
"""

import re
from datetime import datetime, timedelta
from typing import Tuple


class PasswordValidator:
    """Validerer password længde (8-128 tegn)"""
    
    MIN_LENGTH = 8
    MAX_LENGTH = 128
    
    @staticmethod
    def validate(password: str) -> Tuple[bool, str]:
        """
        Validerer password længde.
        
        Args:
            password: Password string at validere
            
        Returns:
            Tuple med (er_valid, besked)
        """
        # Tæl faktiske karakterer (ikke bytes)
        length = len(password)
        
        if length < PasswordValidator.MIN_LENGTH:
            return False, f"Password for kort. Minimum {PasswordValidator.MIN_LENGTH} tegn, fik {length}"
        
        if length > PasswordValidator.MAX_LENGTH:
            return False, f"Password for langt. Maksimum {PasswordValidator.MAX_LENGTH} tegn, fik {length}"
        
        return True, f"Password accepteret ({length} tegn)"


class SessionTokenValidator:
    """Validerer session token udløbstid (max 30 dage)"""
    
    MAX_DAYS = 30
    MAX_SECONDS = MAX_DAYS * 24 * 60 * 60  # 2592000 sekunder
    
    @staticmethod
    def validate(created_at: datetime, checked_at: datetime) -> Tuple[bool, str]:
        """
        Validerer om session token stadig er gyldigt.
        
        Args:
            created_at: Hvornår token blev oprettet
            checked_at: Hvornår vi checker token
            
        Returns:
            Tuple med (er_valid, besked)
        """
        time_diff = checked_at - created_at
        total_seconds = time_diff.total_seconds()
        
        if total_seconds < 0:
            return False, "Token er i fremtiden (ugyldig)"
        
        if total_seconds > SessionTokenValidator.MAX_SECONDS:
            days = total_seconds / (24 * 60 * 60)
            return False, f"Token udløbet. Alder: {days:.2f} dage (max {SessionTokenValidator.MAX_DAYS} dage)"
        
        days = total_seconds / (24 * 60 * 60)
        return True, f"Token gyldigt. Alder: {days:.2f} dage"


class FileUploadValidator:
    """Validerer fil størrelse ved upload (max 10 MB)"""
    
    MAX_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB = 10,485,760 bytes
    
    @staticmethod
    def validate(file_size_bytes: int) -> Tuple[bool, str]:
        """
        Validerer fil størrelse.
        
        Args:
            file_size_bytes: Fil størrelse i bytes
            
        Returns:
            Tuple med (er_valid, besked)
        """
        if file_size_bytes < 0:
            return False, "Ugyldig filstørrelse (negativ)"
        
        if file_size_bytes == 0:
            return False, "Fil er tom (0 bytes)"
        
        if file_size_bytes > FileUploadValidator.MAX_SIZE_BYTES:
            size_mb = file_size_bytes / (1024 * 1024)
            max_mb = FileUploadValidator.MAX_SIZE_BYTES / (1024 * 1024)
            return False, f"Fil for stor. Størrelse: {size_mb:.2f} MB (max {max_mb:.0f} MB)"
        
        size_mb = file_size_bytes / (1024 * 1024)
        return True, f"Fil accepteret ({size_mb:.2f} MB)"


class LoginAttemptValidator:
    """Validerer login forsøg og håndterer lockout (max 5 forsøg per 15 min)"""
    
    MAX_ATTEMPTS = 5
    LOCKOUT_MINUTES = 15
    
    def __init__(self):
        """Initialiserer validator med tom attempt history"""
        self.attempts = []  # Liste af timestamps for failed attempts
        self.locked_until = None
    
    def record_failed_attempt(self, attempt_time: datetime) -> Tuple[bool, str]:
        """
        Registrerer et failed login attempt.
        
        Args:
            attempt_time: Tidspunkt for attempt
            
        Returns:
            Tuple med (er_locked, besked)
        """
        # Check om allerede locked
        if self.locked_until and attempt_time < self.locked_until:
            remaining = (self.locked_until - attempt_time).total_seconds()
            return True, f"Konto låst. {remaining:.0f} sekunder tilbage"
        
        # Hvis lockout er udløbet, nulstil
        if self.locked_until and attempt_time >= self.locked_until:
            self.attempts = []
            self.locked_until = None
        
        # Fjern attempts ældre end 15 minutter
        cutoff_time = attempt_time - timedelta(minutes=self.LOCKOUT_MINUTES)
        self.attempts = [t for t in self.attempts if t > cutoff_time]
        
        # Tilføj nyt attempt
        self.attempts.append(attempt_time)
        
        # Check om vi har ramt grænsen
        if len(self.attempts) >= self.MAX_ATTEMPTS:
            # Lock baseret på det FØRSTE attempt i sekvensen + 15 minutter
            self.locked_until = self.attempts[0] + timedelta(minutes=self.LOCKOUT_MINUTES)
            return True, f"Konto låst efter {self.MAX_ATTEMPTS} forsøg. Låst i {self.LOCKOUT_MINUTES} minutter"
        
        remaining_attempts = self.MAX_ATTEMPTS - len(self.attempts)
        return False, f"Login fejlede. {remaining_attempts} forsøg tilbage"
    
    def can_attempt_login(self, check_time: datetime) -> Tuple[bool, str]:
        """
        Checker om login attempt er tilladt.
        
        Args:
            check_time: Tidspunkt at checke
            
        Returns:
            Tuple med (kan_forsøge, besked)
        """
        if self.locked_until and check_time < self.locked_until:
            remaining = (self.locked_until - check_time).total_seconds()
            return False, f"Konto låst. {remaining:.0f} sekunder tilbage"
        
        if self.locked_until and check_time >= self.locked_until:
            return True, "Lockout udløbet. Login tilladt igen"
        
        return True, "Login tilladt"


# Eksempel på brug
if __name__ == "__main__":
    print("=== Password Validator ===")
    test_passwords = ["kort", "acceptab", "godtpassword123", "x" * 128, "x" * 129]
    for pwd in test_passwords:
        valid, msg = PasswordValidator.validate(pwd)
        print(f"'{pwd[:20]}...' ({len(pwd)} tegn): {msg}")
    
    print("\n=== Session Token Validator ===")
    now = datetime.now()
    created = now - timedelta(days=30)
    valid, msg = SessionTokenValidator.validate(created, now)
    print(f"Token 30 dage gammelt: {msg}")
    
    print("\n=== File Upload Validator ===")
    test_sizes = [0, 10485760, 10485761]
    for size in test_sizes:
        valid, msg = FileUploadValidator.validate(size)
        print(f"{size} bytes: {msg}")
    
    print("\n=== Login Attempt Validator ===")
    validator = LoginAttemptValidator()
    now = datetime.now()
    for i in range(6):
        locked, msg = validator.record_failed_attempt(now + timedelta(seconds=i))
        print(f"Attempt {i+1}: {msg}")