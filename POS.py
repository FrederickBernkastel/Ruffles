"""
    README
    Dependencies
        nltk
        textblob
"""
"""
    Constants definition
"""
from nltk.corpus import stopwords
# Use this if running nltk for the first time
"""
nltk.download('stopwords')
"""
DEBUG = True
STOP_WORDS = ['we','shall','today',"'s"]
STOP_WORDS += stopwords.words('english')
# For a full list of tags, refer to https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
NON_KEYWORD_TAGS = [
        'CC',   # conjunction ('n and both but either et for less minus neither nor or plus so therefore times v. versus vs. whether yet)
        'DT',   # determiner (all an another any both del each either every half la many much nary neither no some such that the them these this those)
        'EX',   # existential there (there)
        'POS',  # genitive marker (' 's)
        'PRP',  # pronoun, personal (hers herself him himself hisself it itself me myself one oneself ours ourselves ownself self she thee theirs them themselves they thou thy us)
        'PRP$', # pronoun, possessive (her his mine my our ours their thy your)
        'TO',   # "to", (to)
        'UH',   # interjection (Goodbye Goody Gosh Wow Jeepers Jee-sus Hubba Hey Kee-reist Oops amen huh howdy uh dammit whammo shucks heck anyways whodunnit honey golly man baby diddle hush sonuvabitch ...)
        'WDT',  # WH-determiner (that what whatever which whichever)
        'WP',   # WH-pronoun (that what whatever whatsoever which who whom whosoever)
        'WP$',  # Possessive WH-pronoun
        'WRB'   # WH-adverb (Wh-adverb)
        ]

"""
    Part-of-Speech Tagger
"""
from textblob import TextBlob
from textblob import Word
# Main POS function
def POS(string):
    blob = TextBlob(string)
    tags = process_tags(blob.tags)
    weighted_tags = {(word,tag):freq for (word,tag),freq in tags.items() if tags[(word,tag)]>1}
    
    if DEBUG:
        print("\nWeighted Nodes")
        print(sorted([(freq,word,tag) for (word,tag),freq in weighted_tags.items()],reverse=True))
        
    return weighted_tags

# Remove Stopwords, and returns frequency dictionary of tagged words in base form
posTb2Wn={'JJ':'a', 'JJR':'a', 'JJS':'a', 'RB':'r', 'RBR':'r', 'RBS':'r', 'VB':'v', 'VBD':'v', 'VBG':'v', 'VBN':'v', 'VBP':'v', 'VBZ':'v', 'NN':'n', 'NNS':'n', 'NNP':'n', 'NNPS':'n', 'n':'n', 'a':'a', 'r':'r', 'v':'v', 's':'s'}
def process_tags(word_tup_l):
    
    final_word_tup_d = {}
    # Cache to memorize NE chain ("Tham Luang Nang Non"), which will have preferential treatment (start freq = 3)
    NE_cache = []
    
    for word,tag in word_tup_l:
        # Skip non-keywords
        if tag in NON_KEYWORD_TAGS:
            continue
        # Lower-case words which are not Named Entities
        if tag not in ["NNP","NNPS"]:
            # Add NE string to word tup and flush it
            if len(NE_cache)>0:
                try:
                    final_word_tup_d[(" ".join(NE_cache),tag)] += 1
                except:
                    final_word_tup_d[(" ".join(NE_cache),tag)] = 3
                NE_cache = []
            
            word = word.lower()
            # Get base form of word
            try:
                if posTb2Wn[tag]=='n':
                    word = Word(word).stem()
                else:
                    word = Word(word).lemmatize(posTb2Wn[tag])
            except:
                pass
        else:
            NE_cache.append(word)
            
        if word not in STOP_WORDS:
            try:
                final_word_tup_d[(word,tag)] += 1
            except:
                final_word_tup_d[(word,tag)] = 1
    return final_word_tup_d
    

# POS Example
POS("""
Last Saturday, 12 young boys went to explore a cave with their coach after football practice in northern Thailand.

Their bikes were found abandoned at the entrance and shortly after, heavy rain sent torrents of water through the cave.

Over the past week, rescuers have been mounting an increasingly desperate search, in the hope the group are alive deep inside the cave but trapped by floodwaters.

Here's what the operation, in the jungle-covered hills around Chiang Rai, involves:
Expert divers

Thai navy divers been trying to access the deepest caverns of the Tham Luang Nang Non cave, the fourth longest in Thailand.

Four top British cave divers, along with some US military personnel, also joined the efforts.

The divers are swimming through tiny spaces and cannot risk going too far into flooded passages or they risk running out of air.

The search has been frustrated by rushing water and near darkness inside the cave. Debris and mud leaves divers with almost no visibility; they can only see a few centimetres in front of them.

It's been described as like swimming through cold coffee. 
""")

"""
    End of Part-of-Speech Tagger
"""


