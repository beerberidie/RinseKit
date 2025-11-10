from pathlib import Path
from typing import List, Dict


DEFAULT_AI_PHRASES = [
    "as an ai language model",
    "in this code snippet",
    "this function is responsible for",
    "in this function, we will",
    "i'm sorry, but",
    "as a large language model",
]


def detect_ai_phrases(path: Path, text: str, phrases=None) -> List[Dict]:
    if phrases is None:
        phrases = DEFAULT_AI_PHRASES
    lowered = text.lower().splitlines()
    results: List[Dict] = []
    for idx, line in enumerate(lowered, start=1):
        for phrase in phrases:
            if phrase in line:
                results.append(
                    {
                        "file": str(path),
                        "line": idx,
                        "phrase": phrase,
                        "kind": "ai_phrase",
                    }
                )
    return results
