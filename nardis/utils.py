from .constants import ENCODING


def encode_string(s: str, encoding=ENCODING) -> bytes:
    """Encodes a unicode string to bytes"""
    return s.encode(encoding)


def decode_string(b: bytes, encoding=ENCODING) -> str:
    """Decodes bytes to a unicode string"""
    return b.decode(encoding)
