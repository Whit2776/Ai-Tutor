import hashlib
import base64
import os
from django.contrib.auth.hashers import PBKDF2PasswordHasher

class CrossPlatformPBKDF2Hasher(PBKDF2PasswordHasher):
    """
    PBKDF2 hasher that works on both Python 3.13.1 and 3.13.5
    """
    
    def encode(self, password, salt, iterations=None):
        assert password is not None
        assert salt and '$' not in salt
        
        if iterations is None:
            iterations = self.iterations
        
        # Use a consistent implementation
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            iterations,
            dklen=32  # Explicitly set length
        )
        
        hash = base64.b64encode(key).decode('ascii').strip()
        return f"{self.algorithm}${iterations}${salt}${hash}"