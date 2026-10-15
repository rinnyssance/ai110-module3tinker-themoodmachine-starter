# mood_analyzer.py
"""
Rule based mood analyzer for short text snippets.

This class starts with very simple logic:
  - Preprocess the text
  - Look for positive and negative words
  - Compute a numeric score
  - Convert that score into a mood label
"""

from typing import List, Dict, Tuple, Optional
import re

from dataset import NEGATIVE_WORDS, POSITIVE_WORDS, SARCASM_PHRASES

# Mood-bearing slang is kept separate so the lexicon can be tuned without
# changing the starter vocabulary. The values represent sentiment strength.
SLANG_SCORES = {
    "bussin": 2,
    "fire": 2,
    "lit": 1,
    "goated": 2,
    "ate": 2,
    "valid": 1,
    "dope": 1,
    "slaps": 2,
    "wack": -2,
    "mid": -1,
    "salty": -1,
    "pressed": -1,
    "trippin": -1,
}

SLANG_PHRASE_SCORES = {
    ("down", "bad"): -2,
    ("not", "it"): -2,
    ("on", "point"): 2,
    ("no", "cap"): 1,
}


class MoodAnalyzer:
    """
    A very simple, rule based mood classifier.
    """

    def __init__(
        self,
        positive_words: Optional[List[str]] = None,
        negative_words: Optional[List[str]] = None,
    ) -> None:
        # Use the default lists from dataset.py if none are provided.
        positive_words = positive_words if positive_words is not None else POSITIVE_WORDS
        negative_words = negative_words if negative_words is not None else NEGATIVE_WORDS

        # Store as sets for faster lookup.
        self.positive_words = set(w.lower() for w in positive_words)
        self.negative_words = set(w.lower() for w in negative_words)
        self.sarcasm_phrases = [
            tuple(phrase.lower().split()) for phrase in SARCASM_PHRASES
        ]
        self.slang_scores = SLANG_SCORES
        self.slang_phrase_scores = SLANG_PHRASE_SCORES

    # ---------------------------------------------------------------------
    # Preprocessing
    # ---------------------------------------------------------------------

    def preprocess(self, text: str) -> List[str]:
        """
        Convert raw text into a list of tokens the model can work with.

        TODO: Improve this method.

        Right now, it does the minimum:
          - Strips leading and trailing whitespace
          - Converts everything to lowercase
          - Splits on spaces

        Ideas to improve:
          - Remove punctuation
          - Handle simple emojis separately (":)", ":-(", "🥲", "😂")
          - Normalize repeated characters ("soooo" -> "soo")
        """
        cleaned = text.strip().lower()
        # Keep contractions together while dropping punctuation around words.
        tokens = re.findall(r"[a-z0-9]+(?:'[a-z0-9]+)?", cleaned)
        print(f"Tokens: {tokens}")

        return tokens

    # ---------------------------------------------------------------------
    # Scoring logic
    # ---------------------------------------------------------------------

    def score_text(self, text: str) -> int:
        """
        Compute a numeric "mood score" for the given text.

        Positive words increase the score.
        Negative words decrease the score.

        TODO: You must choose AT LEAST ONE modeling improvement to implement.
        For example:
          - Handle simple negation such as "not happy" or "not bad"
          - Count how many times each word appears instead of just presence
          - Give some words higher weights than others (for example "hate" < "annoyed")
          - Treat emojis or slang (":)", "lol", "💀") as strong signals
        """
        tokens = self.preprocess(text)
        score = 0
        negation_words = {
            "not", "never", "no", "don't", "dont", "isn't", "isnt",
            "can't", "cant", "won't", "wont",
        }

        for index, token in enumerate(tokens):
            value = 0
            if token in self.slang_scores:
                value = self.slang_scores[token]
            elif token in self.positive_words:
                value = 1
            elif token in self.negative_words:
                value = -1

            # Enhancement: a negation immediately before a mood word flips it.
            if value and index > 0 and tokens[index - 1] in negation_words:
                value *= -1

            score += value

        # Score common multi-word slang expressions once when they appear.
        for phrase, phrase_score in self.slang_phrase_scores.items():
            phrase_length = len(phrase)
            score += sum(
                phrase_score
                for index in range(len(tokens) - phrase_length + 1)
                if tuple(tokens[index:index + phrase_length]) == phrase
            )

        # Enhancement: flip an otherwise positive score for known sarcastic
        # phrases such as "love getting stuck" or "great another homework".
        token_sequence = tuple(tokens)
        is_sarcastic = any(
            phrase and phrase == token_sequence[index:index + len(phrase)]
            for phrase in self.sarcasm_phrases
            for index in range(len(tokens) - len(phrase) + 1)
        )
        if is_sarcastic and score > 0:
            score = -score

        return score

    # ---------------------------------------------------------------------
    # Label prediction
    # ---------------------------------------------------------------------

    def predict_label(self, text: str) -> str:
        """
        Turn the numeric score for a piece of text into a mood label.

        The default mapping is:
          - score > 0  -> "positive"
          - score < 0  -> "negative"
          - score == 0 -> "neutral"

        TODO: You can adjust this mapping if it makes sense for your model.
        For example:
          - Use different thresholds (for example score >= 2 to be "positive")
          - Add a "mixed" label for scores close to zero
        Just remember that whatever labels you return should match the labels
        you use in TRUE_LABELS in dataset.py if you care about accuracy.
        """
        score = self.score_text(text)

        if score > 0:
            return "positive"
        if score < 0:
            return "negative"
        return "neutral"

    # ---------------------------------------------------------------------
    # Explanations (optional but recommended)
    # ---------------------------------------------------------------------

    def explain(self, text: str) -> str:
        """
        Return a short string explaining WHY the model chose its label.

        TODO:
          - Look at the tokens and identify which ones counted as positive
            and which ones counted as negative.
          - Show the final score.
          - Return a short human readable explanation.

        Example explanation (your exact wording can be different):
          'Score = 2 (positive words: ["love", "great"]; negative words: [])'

        The current implementation is a placeholder so the code runs even
        before you implement it.
        """
        tokens = self.preprocess(text)

        positive_hits: List[str] = []
        negative_hits: List[str] = []
        score = 0

        for token in tokens:
            if token in self.positive_words:
                positive_hits.append(token)
                score += 1
            if token in self.negative_words:
                negative_hits.append(token)
                score -= 1

        return (
            f"Score = {score} "
            f"(positive: {positive_hits or '[]'}, "
            f"negative: {negative_hits or '[]'})"
        )
