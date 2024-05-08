import re



def GetAllNLetterWord(n):
    global cipher
    global words
    return [word for word in words if len(word) == n]

def IsMostlyDecrypted(chiper_word):
    global dic
    count = 0
    for ch in chiper_word.lower():
        if ch.isalpha():
            if dic[ch] != 0:
                count += 1
    return count + 1 == len(chiper_word)


def DecryptWord(word):
    global dic
    dyct_word = dict()
    for ch in word:
        ch = ch.lower()
        if dic[ch] != 0:
            dyct_word += dic[ch] #type:ignore
        else:
            dyct_word += f"_{ch}_"#type:ignore
    
    return dyct_word

def LocateInDictionary(word):
    #will find words in the dicionary that have only one letter differnce
    
    list = []
    for dict_word in dict_words:
        differentLetters = 0
        if len(dict_word) == len(word):
            for i in range(len(word)):
                if word[i] != dict_word[i].lower():
                    differentLetters += 1
    
            if differentLetters < 2:
                list.append(dict_word)
        
    return list
    
def PrintAll(): #this prints every word that is nearly completed to manuely fill in the missing letter
    global words
    for word in words:
        if IsMostlyDecrypted(word):
            print(DecryptWord(word))
        

def PrintWordsFromLetter(letter):
    global words
    for word in words:
        if letter in word :
            print(DecryptWord(word))


def PrintRemainingLetters():
    global dic
    print([k for k,v in dic.items() if v == 0])

cipher = """
'Eilj l wtcsptr yaamsxu!' rlso Lmswa; 'S ntrj fa ritjjsxu tb mska l
jamarwpba.'

Lxo rp sj elr sxoaao: ria elr xpe pxmh jax sxwiar isui, lxo iac ylwa
fcsuijaxao tb lj jia jiptuij jilj ria elr xpe jia csuij rsza ypc upsxu
jicptui jia msjjma oppc sxjp jilj mpqamh ulcoax. Yscrj, ipeaqac, ria
elsjao ypc l yae nsxtjar jp raa sy ria elr upsxu jp ricsxk lxh ytcjiac:
ria yamj l msjjma xacqptr lfptj jisr; 'ypc sj nsuij axo, hpt kxpe,' rlso
Lmswa jp iacramy, 'sx nh upsxu ptj lmjpuajiac, mska l wlxoma. S epxoac
eilj S riptmo fa mska jiax?' Lxo ria jcsao jp ylxwh eilj jia ymlna py l
wlxoma sr mska lyjac jia wlxoma sr fmpex ptj, ypc ria wptmo xpj cananfac
aqac ilqsxu raax rtwi l jisxu.

Lyjac l eisma, ysxosxu jilj xpjisxu npca ilbbaxao, ria oawsoao px upsxu
sxjp jia ulcoax lj pxwa; ftj, lmlr ypc bppc Lmswa! eiax ria upj jp jia
oppc, ria yptxo ria ilo ypcupjjax jia msjjma upmoax kah, lxo eiax ria
eaxj flwk jp jia jlfma ypc sj, ria yptxo ria wptmo xpj bprrsfmh calwi
sj: ria wptmo raa sj dtsja bmlsxmh jicptui jia umlrr, lxo ria jcsao iac
farj jp wmsnf tb pxa py jia maur py jia jlfma, ftj sj elr jpp rmsbbach;
lxo eiax ria ilo jscao iacramy ptj esji jchsxu, jia bppc msjjma jisxu
rlj opex lxo wcsao.

'Wpna, jiaca'r xp tra sx wchsxu mska jilj!' rlso Lmswa jp iacramy,
cljiac rilcbmh; 'S loqsra hpt jp malqa pyy jisr nsxtja!' Ria uaxaclmmh
ulqa iacramy qach uppo loqswa, (jiptui ria qach ramopn ypmmpeao sj),
lxo rpnajsnar ria rwpmoao iacramy rp raqacamh lr jp fcsxu jalcr sxjp
iac ahar; lxo pxwa ria cananfacao jchsxu jp fpg iac pex alcr ypc ilqsxu
wialjao iacramy sx l ulna py wcpdtaj ria elr bmlhsxu lulsxrj iacramy,
ypc jisr wtcsptr wismo elr qach ypxo py bcajaxosxu jp fa jep bapbma.
'Ftj sj'r xp tra xpe,' jiptuij bppc Lmswa, 'jp bcajaxo jp fa jep bapbma!
Eih, jiaca'r ilcomh axptui py na mayj jp nlka PXA carbawjlfma bacrpx!'

Rppx iac aha yamm px l msjjma umlrr fpg jilj elr mhsxu txoac jia jlfma:
ria pbaxao sj, lxo yptxo sx sj l qach rnlmm wlka, px eiswi jia epcor
'ALJ NA' eaca faltjsytmmh nlckao sx wtcclxjr. 'Eamm, S'mm alj sj,' rlso
Lmswa, 'lxo sy sj nlkar na ucpe mlcuac, S wlx calwi jia kah; lxo sy sj
nlkar na ucpe rnlmmac, S wlx wcaab txoac jia oppc; rp asjiac elh S'mm
uaj sxjp jia ulcoax, lxo S opx'j wlca eiswi ilbbaxr!'`
"""
with open("ex4_dictionary.txt", 'r') as file:
    dict_words = file.read().split()

#solution:
dic: dict[str,str] = {chr(x):0 for x in range(ord('a'),ord('z') + 1)} # type:ignore
dic['s'] = 'i' #only possible option for S to be a valid word
dic['l'] = 'a' 
#opx'j = don't
dic['o'] = 'd'
dic['p'] = 'o'
dic['x'] = 'n'
dic['j'] = 't'


words = re.split(r"\W", cipher)
threeLetersWords = GetAllNLetterWord(3)

frequency = {}

for word in threeLetersWords:
    if word in frequency:
        frequency[word] += 1
    else:
        frequency[word] = 1


threeLetterWordsfrequency = {k:v for k,v in sorted(frequency.items(), key = lambda x:x[1],reverse=True)}

#most frequent 3 letter words in english are (by decesnding order):
# the, and,you ,are , for
#the most frequent in the cipher are:
#ria ,jia, lxo, elr

#j -> t so jia => the
dic['i'] = 'h' 
dic['a'] = 'e'

dic['r'] = 's' #ria -> _he so r -> s

#l -> a so lxo -> and
dic['x'] = 'n'
dic['o'] = 'd'

#PrintAll()
dic['c'] = 'r'

#print(LocateInDictionary("ehe")) #h is k,r,v,w,y

#PrintAll()
dic ['u'] = 'g'
dic['w'] = 'c'
#PrintAll()
dic['e'] = 'w'
dic ['b'] = 'p'

letterFreq = {chr(x):0 for x in range(ord('a'),ord('z') + 1)}
for word in words:
    for ch in word:
        if ch.isalpha():
            letterFreq[ch.lower()] += 1

letterFreq = {k:v for k,v in sorted(letterFreq.items(), key = lambda x:x[1],reverse=True)}
print(letterFreq)

dic['a'] = 'e'
dic['p'] = 'o'


#PrintWordsFromLetter('d')
dic['d'] = 'q'
dic ['t'] = 'u'

#PrintWordsFromLetter('z')

dic['z'] = 'z'

#PrintWordsFromLetter('q')
dic['q'] = 'v'




#we found a pattern that looks like .eauti.u... that applyes only to beauitflly so
dic['f'] = 'b'
dic ['y'] = 'f'
dic['m'] = 'l'
dic['h'] = 'y'


dic['v'] = ' ' #v doesn't appear at all

#PrintWordsFromLetter('n')
dic['n'] = 'm'

#PrintRemainingLetters()

#PrintWordsFromLetter('g')
dic['g'] = 'x'

#PrintWordsFromLetter('k')
dic['k'] = 'k'

with open("ex4_ansewr.txt", 'w') as file:
    for ch in cipher:
        if ch.isupper():
            file.write(dic.get(ch.lower(),ch).upper())
        else:
            file.write(dic.get(ch,ch))
        
