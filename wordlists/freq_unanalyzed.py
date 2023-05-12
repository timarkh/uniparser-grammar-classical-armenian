import re


freqDict = {}
with open('wordlist.csv', 'r', encoding='utf-8-sig') as fIn:
    for line in fIn:
        if '\t' not in line:
            continue
        w, freq = line.strip('\r\n').split('\t')
        freqDict[w] = int(freq)

unanalyzedWords = []
with open('wordlist_unanalyzed.txt', 'r', encoding='utf-8-sig') as fIn:
    for line in fIn:
        line = line.strip()
        if len(line) <= 0:
            continue
        unanalyzedWords.append(line)

with open('wordlist_unanalyzed_freq.txt', 'w', encoding='utf-8') as fOut:
    for w in unanalyzedWords:
        fOut.write(w + '\t' + str(freqDict[w]) + '\n')


# Collect paradigm statistics
lemmaFreq = {}
paradigmFreqToken = {}
paradigmFreqTypeDict = {}
paradigmFreqTypeCorp = {}
with open('wordlist_analyzed.txt', 'r', encoding='utf-8') as fIn:
    lines = '\n'
    for line in fIn:
        m = re.search('^.*>([^<>\r\n]+)</w>', line)
        if m is None:
            continue
        word = m.group(1)
        freq = freqDict[word]
        lemmata = re.findall('lex="([^\r\n"<>]+)" gr="[NA]\\b', line)
        for lemma in lemmata:
            try:
                lemmaFreq[lemma] += freq
            except KeyError:
                lemmaFreq[lemma] = freq

with open('../xcl-lexemes.txt', 'r', encoding='utf-8') as fIn:
    text = fIn.read()
    lexemes = re.findall('-lexeme\n lex: +([^\r\n]+)\n'
                         ' stem: [^\r\n]*\n'
                         ' gramm: [NA]\\b[^\r\n]*\n'
                         ' paradigm: ([^\r\n]+)\n',
                         text, flags=re.DOTALL)
    for lemma, paradigm in lexemes:
        try:
            paradigmFreqTypeDict[paradigm] += 1
        except KeyError:
            paradigmFreqTypeDict[paradigm] = 1
        if lemma in lemmaFreq:
            try:
                paradigmFreqTypeCorp[paradigm] += 1
            except KeyError:
                paradigmFreqTypeCorp[paradigm] = 1
            try:
                paradigmFreqToken[paradigm] += lemmaFreq[lemma]
            except KeyError:
                paradigmFreqToken[paradigm] = lemmaFreq[lemma]

with open('paradigm_type_dict_freq.txt', 'w', encoding='utf-8') as fOut:
    for paradigm in sorted(paradigmFreqTypeDict,
                        key=lambda p: (-paradigmFreqTypeDict[p], p)):
        fOut.write(paradigm + '\t' + str(paradigmFreqTypeDict[paradigm]) + '\n')

with open('paradigm_type_corp_freq.txt', 'w', encoding='utf-8') as fOut:
    for paradigm in sorted(paradigmFreqTypeCorp,
                        key=lambda p: (-paradigmFreqTypeCorp[p], p)):
        fOut.write(paradigm + '\t' + str(paradigmFreqTypeCorp[paradigm]) + '\n')

with open('paradigm_token_corp_freq.txt', 'w', encoding='utf-8') as fOut:
    for paradigm in sorted(paradigmFreqToken,
                        key=lambda p: (-paradigmFreqToken[p], p)):
        fOut.write(paradigm + '\t' + str(paradigmFreqToken[paradigm]) + '\n')
