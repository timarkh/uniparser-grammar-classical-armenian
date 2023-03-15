import re
import os
import shutil


rxDiacritics = re.compile('[՜՞]')


def collect_lemmata(dirName):
    lemmata = ''
    lexrules = ''
    for fname in os.listdir(dirName):
        if fname.endswith('.txt') and fname.startswith('xcl-lexemes'):
            f = open(os.path.join(dirName, fname), 'r', encoding='utf-8-sig')
            lemmata += f.read() + '\n'
            f.close()
        elif fname.endswith('.txt') and fname.startswith('xcl-lexrules'):
            f = open(os.path.join(dirName, fname), 'r', encoding='utf-8-sig')
            lexrules += f.read() + '\n'
            f.close()
    lemmataSet = set(re.findall('-lexeme\n(?: [^\r\n]*\n)+', lemmata, flags=re.DOTALL))
    lemmata = '\n'.join(sorted(list(lemmataSet)))
    lemmata = rxDiacritics.sub('', lemmata)
    return lemmata, lexrules


def collect_paradigms(dirName):
    paradigms = ''
    for fname in os.listdir(dirName):
        if fname.endswith('.txt') and fname.startswith('xcl-paradigms'):
            f = open(os.path.join(dirName, fname), 'r', encoding='utf-8-sig')
            paradigms += f.read() + '\n'
            f.close()
    return paradigms


def prepare_files():
    """
    Put all the lemmata to lexemes.txt. Put all the lexical
    rules to lexical_rules.txt.
    Put all grammar files to ../uniparser_classical_armenian/data/.
    """
    lemmata, lexrules = collect_lemmata('.')
    paradigms = collect_paradigms('.')
    with open('uniparser_classical_armenian/data/lexemes.txt', 'w', encoding='utf-8') as fOutLemmata:
        fOutLemmata.write(lemmata)
    with open('uniparser_classical_armenian/data/paradigms.txt', 'w', encoding='utf-8') as fOutParadigms:
        fOutParadigms.write(paradigms)
    # fOutLexrules = open('uniparser_classical_armenian/data/lex_rules.txt', 'w', encoding='utf-8')
    # fOutLexrules.write(lexrules)
    # fOutLexrules.close()
    # shutil.copy2('bad_analyses.txt', 'uniparser_classical_armenian/data/')
    # shutil.copy2('armenian_disambiguation.cg3', 'uniparser_eastern_armenian/data/')


def parse_wordlists():
    """
    Analyze wordlists/wordlist.csv.
    """
    from uniparser_classical_armenian import ClassicalArmenianAnalyzer
    a = ClassicalArmenianAnalyzer()
    # for ana in a.analyze_words('աբբայ'):
    #     print(ana.wf, ana.lemma, ana.gramm)
    # for ana in a.analyze_words('աբբայի'):
    #     print(ana.wf, ana.lemma, ana.gramm)
    # for ana in a.analyze_words('զաբբայի'):
    #     print(ana.wf, ana.lemma, ana.gramm)
    a.analyze_wordlist(freqListFile='wordlists/wordlist.csv',
                       parsedFile='wordlists/wordlist_analyzed.txt',
                       unparsedFile='wordlists/wordlist_unanalyzed.txt',
                       verbose=True)


if __name__ == '__main__':
    prepare_files()
    parse_wordlists()
