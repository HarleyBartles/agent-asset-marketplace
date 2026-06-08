"""
Client-side encryption using AES-256-GCM with user-controlled keys.
"""

import base64
import hashlib
import json
import os
from pathlib import Path
from threading import Lock
from dataclasses import dataclass
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


@dataclass
class CryptoResult:
    """Encryption result with metadata."""

    ciphertext: bytes
    algorithm: str
    key_id: str
    plaintext_sha256: str
    ciphertext_sha256: str


_KEY_STORE_LOCK = Lock()
_KEY_STORE: dict[str, bytes] = {}
_KEY_STORE_LOADED = False


def _key_store_path() -> Path:
    """Return the on-disk key store path."""
    env_path = os.environ.get("LUMERA_KEY_STORE_PATH")
    if env_path:
        return Path(env_path)
    return Path.home() / ".lumera-agent-memory" / "keys.json"


def _load_key_store() -> None:
    """Load persisted keys from disk once."""
    global _KEY_STORE_LOADED
    if _KEY_STORE_LOADED:
        return

    path = _key_store_path()
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            for key_id, encoded_key in data.items():
                _KEY_STORE[key_id] = base64.b64decode(encoded_key.encode("ascii"))
        except Exception:
            # Fall back to an empty store and regenerate as needed.
            _KEY_STORE.clear()

    _KEY_STORE_LOADED = True


def _save_key_store() -> None:
    """Persist keys to disk atomically."""
    path = _key_store_path()
    path.parent.mkdir(parents=True, exist_ok=True)

    data = {
        key_id: base64.b64encode(key).decode("ascii")
        for key_id, key in _KEY_STORE.items()
    }

    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    tmp_path.replace(path)


def _get_or_create_key(key_id: str = "default") -> bytes:
    """Get or create encryption key."""
    with _KEY_STORE_LOCK:
        _load_key_store()
        if key_id not in _KEY_STORE:
            # Generate new 256-bit key and persist it for future restarts.
            _KEY_STORE[key_id] = AESGCM.generate_key(bit_length=256)
            _save_key_store()
        return _KEY_STORE[key_id]


def encrypt_data(plaintext: str, key_id: str = "default") -> CryptoResult:
    """
    Encrypt data using AES-256-GCM.

    Args:
        plaintext: Data to encrypt (string)
        key_id: Key identifier

    Returns:
        CryptoResult with encrypted data and metadata
    """
    # Get encryption key
    key = _get_or_create_key(key_id)
    aesgcm = AESGCM(key)

    # Generate random nonce (96 bits for GCM)
    nonce = os.urandom(12)

    # Encrypt
    plaintext_bytes = plaintext.encode("utf-8")
    ciphertext_without_nonce = aesgcm.encrypt(nonce, plaintext_bytes, None)

    # Prepend nonce to ciphertext for storage
    ciphertext = nonce + ciphertext_without_nonce

    # Compute hashes
    plaintext_sha256 = hashlib.sha256(plaintext_bytes).hexdigest()
    ciphertext_sha256 = hashlib.sha256(ciphertext).hexdigest()

    return CryptoResult(
        ciphertext=ciphertext,
        algorithm="AES-256-GCM",
        key_id=key_id,
        plaintext_sha256=plaintext_sha256,
        ciphertext_sha256=ciphertext_sha256,
    )


def decrypt_data(ciphertext: bytes, key_id: str = "default", expected_ciphertext_sha256: str = None) -> str:
    """
    Decrypt AES-256-GCM encrypted data.

    Args:
        ciphertext: Encrypted data (with nonce prepended)
        key_id: Key identifier
        expected_ciphertext_sha256: Optional integrity check

    Returns:
        Decrypted plaintext string
    """
    # Verify ciphertext integrity
    if expected_ciphertext_sha256:
        actual_sha256 = hashlib.sha256(ciphertext).hexdigest()
        if actual_sha256 != expected_ciphertext_sha256:
            raise ValueError(
                f"Ciphertext integrity check failed. Expected: {expected_ciphertext_sha256}, Got: {actual_sha256}"
            )

    # Get decryption key
    key = _get_or_create_key(key_id)
    aesgcm = AESGCM(key)

    # Extract nonce (first 12 bytes)
    nonce = ciphertext[:12]
    ciphertext_only = ciphertext[12:]

    # Decrypt
    plaintext_bytes = aesgcm.decrypt(nonce, ciphertext_only, None)

    return plaintext_bytes.decode("utf-8")
