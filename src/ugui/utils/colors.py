def hash_string(s: str) -> int:
    """FNV-1a hashing algorithm for better distribution"""
    FNV_PRIME = 0x01000193
    FNV_OFFSET = 0x811C9DC5

    hash_value = FNV_OFFSET
    for char in s.encode():
        hash_value = ((hash_value ^ char) * FNV_PRIME) & 0xFFFFFFFF
    return hash_value


def colorhash(text: str) -> str:
    """Generate a bright, readable color from text input"""
    hash_value = hash_string(text)

    # Multiple golden ratios for better distribution
    golden_ratio1 = 0.618033988749895
    golden_ratio2 = 0.517638090205041  # Another golden mean variant

    # Use text length to vary starting point
    start_hue = (0.314159265 + (len(text) * 0.1)) % 1.0

    # Generate hue with dual golden ratio influence
    hue = ((start_hue + (hash_value * golden_ratio1 * golden_ratio2)) % 1.0) * 360

    # More varied saturation and lightness based on text characteristics
    saturation = 65 + ((hash_value + len(text)) % 25)  # 65-90%
    lightness = 35 + ((hash_value ^ len(text)) % 20)  # 35-55%

    return f"hsl({hue}, {saturation}%, {lightness}%)"
