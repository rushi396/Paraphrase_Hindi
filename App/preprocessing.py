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
    stopwords=["अंदर","अत","अदि","अप","अपना","अपनि","अपनी","अपने","अभि","अभी","आदि","आप","इंहिं","इंहें","इंहों","इतयादि","इत्यादि","इन","इनका","इन्हीं","इन्हें","इन्हों","इस","इसका","इसकि","इसकी","इसके","इसमें","इसि","इसी","इसे","उंहिं","उंहें","उंहों","उन","उनका","उनकि","उनकी","उनके","उनको","उन्हीं","उन्हें","उन्हों","उस","उसके","उसि","उसी","उसे","एक","एवं","एस","एसे","ऐसे","ओर","और","कइ","कई","कर","करता","करते","करना","करने","करें","कहते","कहा","का","काफि","काफ़ी","कि","किंहें","किंहों","कितना","किन्हें","किन्हों","किया","किर","किस","किसि","किसी","किसे","की","कुछ","कुल","के","को","कोइ","कोई","कोन","कोनसा","कौन","कौनसा","गया","घर","जब","जहाँ","जहां","जा","जिंहें","जिंहों","जितना","जिधर","जिन","जिन्हें","जिन्हों","जिस","जिसे","जीधर","जेसा","जेसे","जैसा","जैसे","जो","तक","तब","तरह","तिंहें","तिंहों","तिन","तिन्हें","तिन्हों","तिस","तिसे","तो","था","थि","थी","थे","दबारा","दवारा","दिया","दुसरा","दुसरे","दूसरे","दो","द्वारा","न","नहिं","नहीं","ना","निचे","निहायत","नीचे","ने","पर","पहले","पुरा","पूरा","पे","फिर","बनि","बनी","बहि","बही","बहुत","बाद","बाला","बिलकुल","भि","भितर","भी","भीतर","मगर","मानो","मे","में","यदि","यह","यहाँ","यहां","यहि","यही","या","यिह","ये","रखें","रवासा","रहा","रहे","ऱ्वासा","लिए","लिये","लेकिन","व","वगेरह","वरग","वर्ग","वह","वहाँ","वहां","वहिं","वहीं","वाले","वुह","वे","वग़ैरह","संग","सकता","सकते","सबसे","सभि","सभी","साथ","साबुत","साभ","सारा","से","सो","हि","ही","हुअ","हुआ","हुइ","हुई","हुए","हे","हें","है","हैं","हो","होता","होति","होती","होते","होना","होने"]
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