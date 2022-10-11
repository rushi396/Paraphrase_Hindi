import codecs
import re

class Tokenizer():
  def __init__(self,text=None):
    if text is  not None:
      self.text=text
      self.cleanText()
    else:
      self.text=None

    self.sentences=[]
    self.tokens=[]
    self.stemmed_word=[]
    self.final_list=[]

  def gen_sentences(self):
    text=self.text
    self.sentences=text.split("। ")
    #print(self.sentences)

  def printTokens(self):
    for i in self.tokens:
      print(i)

  def spaceTok(self,sentences_list):
    tokens=[]
    for each in sentences_list:
        word_list=each.split(' ')
        word_list[-1] = word_list[-1].replace("।",'')
        tokens=tokens+word_list

    return tokens

  def cleanText(self):
    text=self.text
    text=text.strip()
    text=re.sub(r'(\d+)',r'',text)
    text=text.replace(',','')
    text=text.replace('"','')
    text=text.replace('(','')
    text=text.replace(')','')
    text=text.replace('"','')
    text=text.replace(':','')
    text=text.replace("'",'')
    text=text.replace("‘‘",'')
    text=text.replace("’’",'')
    text=text.replace("''",'')
    text=text.replace(".",'')
    text=text.replace("-",' ')
    text=text.replace("  ",' ')
    self.text=text

  def removeStopWords(self,token_list):
    f=codecs.open("stopwords.txt",encoding='utf-8')
    stopwords=[x.strip() for x in f.readlines()]
    #print(stopwords)
    #print(token_list)
    tokens=[i for i in token_list if i not in stopwords]
    self.final_tokens=tokens
    return tokens

  def stemWords(self,word):
    suffixes = {
    1: ["ो","े","ू","ु","ी","ि","ा"],
    2: ["कर","ाओ","िए","ाई","ाए","ने","नी","ना","ते","ीं","ती","ता","ाँ","ां","ों","ें"],
    3: ["ाकर","ाइए","ाईं","ाया","ेगी","ेगा","ोगी","ोगे","ाने","ाना","ाते","ाती","ाता","तीं","ाओं","ाएं","ुओं","ुएं","ुआं"],
    4: ["ाएगी","ाएगा","ाओगी","ाओगे","एंगी","ेंगी","एंगे","ेंगे","ूंगी","ूंगा","ातीं","नाओं","नाएं","ताओं","ताएं","ियाँ","ियों","ियां"],
    5: ["ाएंगी","ाएंगे","ाऊंगी","ाऊंगा","ाइयाँ","ाइयों","ाइयां"],
    }
    for L in 5, 4, 3, 2, 1:
      if len(word) > L + 1:
        for suf in suffixes[L]:
          #print type(suf),type(word),word,suf
          if word.endswith(suf):
            #print 'h'
            return word[:-L]
    return word

  def scriptValidation(self,token_list):
    tokens = []
    for tok in token_list:
      #print(i)
      for ch in tok:
        #print(x)
        if ord(ch) not in list(range(2304,2432)):
          tok = tok.replace(ch,'')
      if tok!="":
        tokens.append(tok)

    return tokens

  def tokenize(self):
    if not self.sentences:
      self.gen_sentences()
      sentences_list=self.sentences
      #print(sentences_list)
      token_list = self.spaceTok(sentences_list)
      #print(token_list)
      token_list = self.scriptValidation(token_list)
      #print(token_list)
      token_list = self.removeStopWords(token_list)
      #print(token_list)
      tokens = []
      for tok in token_list:
        tokens.append(self.stemWords(tok))
      self.tokens=tokens
      return tokens