import numpy as np
import pandas as pd
import codecs
import pyiwn
iwn = pyiwn.IndoWordNet()
from preprocessing import Tokenizer


def cosine_similarity(token_list1,token_list2):
  l1 =[]
  l2 =[]
  token_list1 = set(token_list1)
  token_list2 = set(token_list2)
  # form a set containing keywords of both strings 
  rvector = token_list1.union(token_list2)
  
  #print(rv)
  for w in rvector:
      if w in token_list1: l1.append(1) # create a vector
      else: l1.append(0)
      
      if w in token_list2: l2.append(1)
      else: l2.append(0)

  #print(l1,l2)
  c = 0
    
  # cosine formula 
  for i in range(len(rvector)):
          c+= l1[i]*l2[i] 

  #print(c)

  try:
    cosine = round(c / float((sum(l1)**0.5)*(sum(l2)**0.5)),2)
    global cosine_value 
    cosine_value = cosine   
  except:
    return 0
  else:
    if cosine >= 0 and cosine <= 0.33:
      return 0
    elif cosine >= 0.34 and cosine <= 0.67:
      return 1
    elif cosine >= 0.68:
      return 2
    #print("similarity: ", cosine)


def jaccard_similarity(x,y):
  x = set(x)
  y = set(y)
  """ returns the jaccard similarity between two lists """
  intersection_cardinality = len(x.intersection(y))
  union_cardinality = len(x.union(y))

  try:
    jaccard = round(intersection_cardinality/union_cardinality,2)
    global jaccard_value 
    jaccard_value = jaccard
  except:
    return 0
  else:
    if jaccard >= 0 and jaccard <= 0.33:
      return 0
    elif jaccard >= 0.34 and jaccard <= 0.67:
      return 1
    elif jaccard >= 0.68:
      return 2

def syno_match(token_list1,token_list2):
  count = 0
  for each in token_list1:
    #print("each: ",each)
    if each in token_list2:
      #print("count++: ",each)
      count+=1
    else:
      try:
        word = iwn.synsets(each)
      except:
        #print("error")
        pass
      else:
        syn_words = []
        for i in range(0,len(word)):
          syn_words.append(word[i].head_word())
        #print(syn_words)
        for w in syn_words:
          if w in token_list2:
            count+=1
            #print("count++: ",each)
  try:
  #print(count)
    sim = round(count/(max(len(token_list1),len(token_list2))),2)
    global syno_value
    syno_value = sim
  except:
    return 0
  else:
    if sim >= 0 and sim <= 0.33:
      return 0
    elif sim >= 0.34 and sim <= 0.67:
      return 1
    elif sim >= 0.68:
      return 2
    #print(sim)

def bigram_similarity(token_list1,token_list2):
  bigram_list1,bigram_list2 = [],[]
  for i in range(0,len(token_list1)-1):
    bigram_list1.append([token_list1[i],token_list1[i+1]])

  for i in range(0,len(token_list2)-1):
    bigram_list2.append([token_list2[i],token_list2[i+1]])

  nt1 = map(tuple, bigram_list1)
  nt2 = map(tuple, bigram_list2)

  st1 = set(nt1)
  st2 = set(nt2)

  rvector = st1.intersection(st2)
  #print(rvector)
  try:
    bigram = round(len(rvector)/(len(bigram_list1)+len(bigram_list2)),2)
    global bigram_value
    bigram_value = bigram
  except:
    return 0
  else:
    if bigram >= 0 and bigram <= 0.33:
      return 0
    elif bigram >= 0.34 and bigram <= 0.67:
      return 1
    elif bigram >= 0.68:
      return 2

def features_extraction(txt1,txt2):
  corpus = []
  cosine_data,jaccard_data,bigram_data,syno_data = [],[],[],[]
  for i in range(0,1):
    #print("iter: ",i)
    #print(df['SENTENCE2'][i])
    t1 = Tokenizer(txt1)
    t2 = Tokenizer(txt2)

    token_list1 = t1.tokenize()
    token_list2 = t2.tokenize()
    try:
      token_list1 = token_list1.remove(" ")
      token_list2 = token_list2.remove(" ")
    except:
      pass

    #print(token_list1)
    cosine_data.append(cosine_similarity(token_list1,token_list2))
    jaccard_data.append(jaccard_similarity(token_list1,token_list2))
    bigram_data.append(bigram_similarity(token_list1,token_list2))
    syno_data.append(syno_match(token_list1,token_list2))


    token_list1 = ' '.join(' '.join(token_list1).split())
    token_list2 = ' '.join(' '.join(token_list2).split())

    corpus.append([token_list1,token_list2])

  #print(corpus)
  features = pd.DataFrame({"cosine_similarity":cosine_data,
                          "jaccard_similarity":jaccard_data,
                          "bigram_matching":bigram_data,
                          "syno_match":syno_data})
  
  print(features.head())
  print(len(features))
  print(max(syno_data),min(syno_data))

  data = {
    "features":features,
    "cosine_similarity":cosine_data,
    "jaccard_similarity":jaccard_data,
    "bigram_matching":bigram_data,
    "syno_match":syno_data,
    "cosine_value":cosine_value,
    "jaccard_value":jaccard_value,
    "bigram_value":jaccard_value,
    "syno_value":syno_value
  }
  return data