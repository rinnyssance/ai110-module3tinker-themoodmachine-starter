# The Mood Machine

The Mood Machine is a small, rule-based sentiment analyzer for short text. It predicts whether a message sounds **positive**, **negative**, or **neutral** by looking for words, slang, negation, and a few sarcastic phrases.

This project is also a reflection on a bigger question: how can a text classifier understand language when meaning depends on culture, context, and community?

## What it does

The analyzer in [`mood_analyzer.py`](./mood_analyzer.py) follows a simple pipeline:

1. Normalize text by lowercasing it and turning it into tokens.
2. Look up positive and negative words.
3. Add sentiment weights for mood-bearing slang.
4. Flip a nearby sentiment word when it follows a negation such as `not` or `never`.
5. Detect a small set of sarcastic phrase patterns.
6. Convert the final score into a label.

Positive scores become `positive`, negative scores become `negative`, and a score of zero becomes `neutral`.

## Examples

```text
"I love this class"               -> positive
"I am not happy about this"       -> negative
"That performance was fire"       -> positive
"This assignment is mid"          -> negative
"I am down bad"                   -> negative
"I love getting stuck in traffic" -> negative (sarcasm rule)
```

The word lists, sample posts, and sarcastic phrase patterns are stored in [`dataset.py`](./dataset.py).

## Running the project

Install the optional dependencies and run the main demo:

```bash
pip install -r requirements.txt
python main.py
```

The program evaluates the sample posts, runs a batch demo, and then opens an interactive prompt. Type `quit` or press Enter to exit the prompt.

## What I learned about sentiment analysis

Sentiment analysis is not the same as simply counting “good” and “bad” words. A useful prediction depends on several layers of interpretation:

- **Preprocessing matters.** Punctuation, capitalization, contractions, and tokenization can change whether a word is recognized.
- **Context matters.** “Not happy” does not mean the same thing as “happy,” and a phrase such as “down bad” cannot be understood by analyzing each word independently.
- **Sarcasm is difficult.** “I absolutely love getting stuck in traffic” contains positive vocabulary but communicates frustration. A small phrase rule can help, but it will never understand every sarcastic message.
- **Scores are design choices.** Giving `fire` a score of `2` and `mid` a score of `-1` is an assumption about intensity, not an objective truth.
- **A small dataset limits confidence.** A classifier can appear accurate on a few examples while still failing on new writing styles.

## Culture, slang, and algorithmic bias

Language is shaped by communities. Some of the slang in this project is associated with African American English (AAVE), while other terms are common in internet and youth language more broadly. These categories overlap, change over time, and are not interchangeable. No community uses every term in the same way.

Adding slang made the bot more useful for some messages, but it also made the risks of algorithmic bias clearer:

- **Dialect bias:** A system trained mostly on formal or standardized English may treat AAVE grammar and vocabulary as unusual, negative, or low quality.
- **Lexicon bias:** A word can be positive in one context and negative in another. For example, `fire` can describe something excellent, but it can also refer literally to danger.
- **Context and identity:** The same phrase may have different meanings depending on who says it, who hears it, and the surrounding conversation.
- **Representation bias:** If the examples do not include enough speakers, dialects, regions, ages, and contexts, the model will learn a narrow version of language.
- **Impact bias:** A wrong label is not equally harmless in every application. Mood predictions should not be used for high-stakes decisions about people.

The lesson is not that slang should be removed. The lesson is that slang should be represented carefully, tested with real context, and evaluated for different language communities. A model should not confuse unfamiliar language with negative sentiment.

## Limitations and next steps

This is an educational rule-based system, not a general-purpose language model. It can miss new slang, misunderstand reclaimed language, mishandle emojis, and make mistakes when several sentiments appear together. Its sarcasm rules are intentionally small and conservative.

Possible improvements include:

- Add more examples from different communities, with consent and careful labeling.
- Track `mixed` sentiment instead of forcing every message into one direction.
- Add emoji and repeated-character handling.
- Compare predictions across dialectal and formal rewrites of the same meaning.
- Measure false positives and false negatives separately for different types of language.
- Let people inspect and correct the words and weights used by the classifier.
- Use human review before applying sentiment predictions to real decisions.

## Project files

```text
dataset.py         Word lists, slang patterns, sample posts, and labels
mood_analyzer.py   Rule-based sentiment analyzer
main.py            Evaluation, demo, and interactive prompt
ml_experiments.py  Optional small machine-learning experiment
model_card.md      Model limitations and evaluation notes
README.md          Project documentation and reflection
```

## Takeaway

Building a small mood bot showed me that sentiment analysis is partly a technical problem and partly a language-and-culture problem. Better code can improve tokenization and scoring, but fairness also requires better data, transparent assumptions, cultural humility, and attention to how predictions affect real people.
