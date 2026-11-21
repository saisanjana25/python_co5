# PART B - TASK B4: Practical AI Implementation (Sentiment Scorer with Negation)

POSITIVE = {"good", "clean", "fast", "helpful", "improved"}
NEGATIVE = {"bad", "dirty", "slow", "rude", "smoke", "broken"}
NEGATORS = {"not", "never", "no"}


def score(text):
    """+1 per positive word, -1 per negative word; a preceding negator flips sign."""
    words = text.lower().replace(".", "").replace(",", "").split()
    total = 0
    for i, word in enumerate(words):
        val = 0
        if word in POSITIVE:
            val = 1
        elif word in NEGATIVE:
            val = -1
        if val != 0:
            if i > 0 and words[i - 1] in NEGATORS:
                val = -val
            total += val
    return total


def label(text):
    s = score(text)
    return "positive" if s > 0 else "negative" if s < 0 else "neutral"


if __name__ == "__main__":
    test_complaints = [
        "Roads are clean and the bus was fast.",
        "Smoke from the factory, air is bad.",
        "The staff were not helpful.",
        "Not bad, service improved.",
    ]
    for c in test_complaints:
        print(f"{label(c):8} | {c}")
