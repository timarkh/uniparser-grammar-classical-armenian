# Classical Armenian morphological analyzer
This is a rule-based morphological analyzer for Classical Eastern Armenian. It is based on a formalized description of literary Classical Armenian morphology and uses [uniparser-morph](https://github.com/timarkh/uniparser-morph) for parsing. It performs full morphological analysis of Classical Armenian words (lemmatization, POS tagging, grammatical tagging, glossing).

## How to use
### Python package
The analyzer is available as a Python package. If you want to analyze Classical Armenian texts in Python, install the module:

```
pip3 install uniparser-classical-armenian
```

Import the module and create an instance of ``ClassicalArmenianAnalyzer`` class. After that, you can either parse tokens or lists of tokens with ``analyze_words()``, or parse a frequency list with ``analyze_wordlist()``. Here is a simple example:

```python
from uniparser_eastern_armenian import EasternArmenianAnalyzer
a = ClassicalArmenianAnalyzer()

analyses = a.analyze_words('Ձևաբանություն')
# The parser is initialized before first use, so expect
# some delay here (usually several seconds)

# You will get a list of Wordform objects
# The analysis attributes are stored in its properties
# as string values, e.g.:
for ana in analyses:
        print(ana.wf, ana.lemma, ana.gramm, ana.gloss)

# You can also pass lists (even nested lists) and specify
# output format ('xml' or 'json')
# If you pass a list, you will get a list of analyses
# with the same structure
analyses = a.analyze_words([['և'], ['Ես', 'սիրում', 'եմ', 'քեզ', ':']],
	                       format='xml')
analyses = a.analyze_words(['Ձևաբանություն', [['և'], ['Ես', 'սիրում', 'եմ', 'քեզ', ':']]],
	                       format='json')
```

Refer to the [uniparser-morph documentation](https://uniparser-morph.readthedocs.io/en/latest/) for the full list of options.
