freqDict = {}
with open('wordlist.csv', 'r', encoding='utf-8') as fIn:
    for line in fIn:
        if '\t' not in line:
            continue
        w, freq = line.strip('\r\n').split('\t')
        freqDict[w] = freq

unanalyzedWords = []
with open('wordlist_unanalyzed.txt', 'r', encoding='utf-8') as fIn:
    for line in fIn:
        line = line.strip()
        if len(line) <= 0:
            continue
        unanalyzedWords.append(line)

with open('wordlist_unanalyzed_freq.txt', 'w', encoding='utf-8') as fOut:
    for w in unanalyzedWords:
        fOut.write(w + '\t' + freqDict[w] + '\n')
