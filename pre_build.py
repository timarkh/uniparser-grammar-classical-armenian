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


def process_schwa(a):
    """
    Find unanalyzed words that contain a schwa inside and try analyzing them
    without the schwa. Add the results to the list of analyzed words.
    """
    rxSchwa = re.compile('^(\\w+)ը(\\w+)$')
    unanalyzedSchwa = []
    norm2schwa = {}
    freqDict = {}
    with open('wordlists/wordlist_unanalyzed.txt', 'r', encoding='utf-8') as fIn:
        for word in fIn:
            word = word.strip()
            if rxSchwa.search(word) is not None:
                unanalyzedSchwa.append(word)
    with open('wordlists/wordlist.csv', 'r', encoding='utf-8') as fIn:
        for line in fIn:
            word, freq = line.strip().split('\t')
            freqDict[word] = freq
    with open('wordlists/wordlist_schwa.csv', 'w', encoding='utf-8') as fOut:
        for word in unanalyzedSchwa:
            wordNorm = rxSchwa.sub('\\1\\2', word)
            if wordNorm not in norm2schwa:
                norm2schwa[wordNorm] = [word]
                fOut.write(wordNorm
                           + '\t' + freqDict[word] + '\n')
            else:
                norm2schwa[wordNorm].append(word)
    print('Processing schwa words...')
    a.analyze_wordlist(freqListFile='wordlists/wordlist_schwa.csv',
                       parsedFile='wordlists/wordlist_analyzed_schwa.txt',
                       unparsedFile='wordlists/wordlist_unanalyzed_schwa.txt',
                       verbose=True)
    analyzedSchwa = set()
    with open('wordlists/wordlist_analyzed_schwa.txt', 'r', encoding='utf-8') as fIn:
        lines = '\n'
        for line in fIn:
            m = re.search('^(.*>)([^<>\r\n]+)</w>', line)
            if m is None:
                continue
            wordNorm = m.group(2)
            for word in norm2schwa[wordNorm]:
                analyzedSchwa.add(word)
                lines += m.group(1) + word + '</w>\n'
    with open('wordlists/wordlist_analyzed.txt', 'a', encoding='utf-8') as fOut:
        fOut.write(lines)
    lines = []
    with open('wordlists/wordlist_unanalyzed.txt', 'r', encoding='utf-8') as fIn:
        for line in fIn:
            line = line.strip()
            if line not in analyzedSchwa:
                lines.append(line)
    with open('wordlists/wordlist_unanalyzed.txt', 'w', encoding='utf-8') as fOut:
        fOut.write('\n'.join(lines))


def process_diacritics(a):
    """
    Find unanalyzed words that contain a diacritic inside and try analyzing them
    without the diacritic. Add the results to the list of analyzed words.
    """
    rxDia = re.compile('^(\\w+)[՜՞](\\w+)$')
    unanalyzedDia = []
    norm2dia = {}
    freqDict = {}
    with open('wordlists/wordlist_unanalyzed.txt', 'r', encoding='utf-8') as fIn:
        for word in fIn:
            word = word.strip()
            if rxDia.search(word) is not None:
                unanalyzedDia.append(word)
    with open('wordlists/wordlist.csv', 'r', encoding='utf-8') as fIn:
        for line in fIn:
            word, freq = line.strip().split('\t')
            freqDict[word] = freq
    with open('wordlists/wordlist_dia.csv', 'w', encoding='utf-8') as fOut:
        for word in unanalyzedDia:
            wordNorm = rxDia.sub('\\1\\2', word)
            if wordNorm not in norm2dia:
                norm2dia[wordNorm] = [word]
                fOut.write(wordNorm
                           + '\t' + freqDict[word] + '\n')
            else:
                norm2dia[wordNorm].append(word)
    print('Processing schwa words...')
    a.analyze_wordlist(freqListFile='wordlists/wordlist_dia.csv',
                       parsedFile='wordlists/wordlist_analyzed_dia.txt',
                       unparsedFile='wordlists/wordlist_unanalyzed_dia.txt',
                       verbose=True)
    analyzedDia = set()
    with open('wordlists/wordlist_analyzed_dia.txt', 'r', encoding='utf-8') as fIn:
        lines = '\n'
        for line in fIn:
            m = re.search('^(.*>)([^<>\r\n]+)</w>', line)
            if m is None:
                continue
            wordNorm = m.group(2)
            for word in norm2dia[wordNorm]:
                analyzedDia.add(word)
                lines += m.group(1) + word + '</w>\n'
    with open('wordlists/wordlist_analyzed.txt', 'a', encoding='utf-8') as fOut:
        fOut.write(lines)
    lines = []
    with open('wordlists/wordlist_unanalyzed.txt', 'r', encoding='utf-8') as fIn:
        for line in fIn:
            line = line.strip()
            if line not in analyzedDia:
                lines.append(line)
    with open('wordlists/wordlist_unanalyzed.txt', 'w', encoding='utf-8') as fOut:
        fOut.write('\n'.join(lines))


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
    process_diacritics(a)
    process_schwa(a)


if __name__ == '__main__':
    prepare_files()
    parse_wordlists()
