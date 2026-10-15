import re

SUSPICIOUS_PATTERNS = [
    r"ignore (all )?previous instructions",
    r"reveal (the )?system prompt",
    r"send .* passwords",
    r"disable (all )?security",
    r"bypass .* policy",
]


def detect_threat(content: str) -> dict:
    matches = [
        pattern
        for pattern in SUSPICIOUS_PATTERNS
        if re.search(pattern, content, re.IGNORECASE)
    ]

    return {
        "suspicious": bool(matches),
        "matched_patterns": matches,
        "reason": "Potential prompt injection" if matches else None,
    }