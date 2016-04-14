'''
Created on 27-Mar-2015

@author: Himani
'''
import re
import numpy as np
import operator    

# Bootstrapping Aspect Segmentation Parameters from paper LARA
chi_topK = 35 # Top K words to extend aspect seed words
chi_iter = 10 # Number of bootstrapping iterations to converge  
tf_cut = 10 # discard terms occurring less than 10 times in corpus


# Function to load Aspect Keywords fom a file
# We can Aspects and seed words in file to load
# it dynamically
def loadAspectKeywords(filename):

    m_aspectKeywords = dict()
    f = open(filename, 'r')
    for line in f.readlines():
        container = line.split(" ")
        keywords = []
        for i in range(1,len(container)):
            keywords.append(container[i].strip())
        asp_name = re.sub("[:]", "" , container[0])    
        m_aspectKeywords[asp_name] = keywords
        print ("keywords for ", asp_name, ":", len(keywords))
    f.close()
    return m_aspectKeywords


# Function to create empty chi-square table/matrix
# Chi-Square Matrix is MxN where M is Number of aspects
# under consideration and N is vocabulary length
def createChiTable(m_vocabulary, m_aspectkeywords):
    m_chi_table = np.zeros((len(m_aspectkeywords), len(m_vocabulary)))
    m_wordcount = np.zeros(len(m_vocabulary)) # Array to hold vocabulary word count
    m_ranklist = dict() # create empty dictionary to hold ranked chi-square values
    for vocab_key in m_vocabulary:
        m_ranklist[vocab_key] = 0.0 # initially give equal ranks to vocabulary words
        
    return m_chi_table, m_wordcount, m_ranklist


# This Function calculates the actual chi-square values and
# populates the empty chi-square table created in above step    
def chiSquareTest(m_sentences, m_vocabulary, m_aspectkeywords):
    m_chi_table, m_wordCount, m_ranklist = createChiTable(m_vocabulary, m_aspectkeywords)
    # assign the sentence an aspect label 
    Annotate(m_sentences, m_aspectkeywords)
    # populate chi-square table with word-counts
    m_chi_table = populateChiStats(m_sentences, m_vocabulary, m_chi_table)
    # calculate N as total number of word occurrences
    N = 0
    aspectCount = np.zeros(len(m_aspectkeywords))
    for i in range(len(aspectCount)):
        for j in range(len(m_wordCount)):
            aspectCount[i] += m_chi_table[i][j]
            m_wordCount[j] += m_chi_table[i][j]
            N += m_chi_table[i][j]
    
    # Compute C1 to C4         
    for i in range(len(aspectCount)):
        for j in range(len(m_wordCount)):
            C1 = m_chi_table[i][j]
            C2 = m_wordCount[j]-m_chi_table[i][j]
            C3 = aspectCount[i]-m_chi_table[i][j]
            C4 = N-m_chi_table[i][j]
            m_chi_table[i][j] = ChiSquareValue(C1, C2, C3, C4, N) 
                                                    
    return m_chi_table, m_ranklist                 

# The Function takes input as follows:
#  C1: w and a
#  C2: w and !a
#  C3: !w and a
#  C4: !w and !a
#  N: total
#  return Chi-Square value
def ChiSquareValue(C1, C2, C3, C4, N):
    denomiator = (C1+C3) * (C2+C4) * (C1+C2) * (C3+C4)
    if (denomiator > 0) and (C1+C2 > tf_cut):
        return N * (C1*C4-C2*C3) * (C1*C4-C2*C3) / denomiator;
    else:
        return 0.0           

# Annotate the sentence as aspect label by 
# ai = argmaxi Count(i) according to LARA    
def Annotate(m_sentences, m_aspectkeywords):
    for stn in m_sentences:
        maxCount = 0
        count = -1 
        selected_aspect_id = -1
        aspect_id = -1
        for asp_key in m_aspectkeywords:
            aspect_id += 1
            count = AnnotateByKeywords(stn, m_aspectkeywords[asp_key])
            if count > maxCount:
                maxCount = count
                selected_aspect_id = aspect_id
            elif count == maxCount:
                selected_aspect_id = -1
        stn.aspectID = selected_aspect_id

# Function to populate chi-square table with word
# counts belonging to an aspect ID
def populateChiStats(m_sentences, m_vocabulary, m_chi_table):
    for stn in m_sentences:
        aspID = stn.aspectID
        if aspID is not -1:
            for tkn in stn.ttoken:
                if (tkn.lemma in m_vocabulary) == False:
                    print ("Missing:",tkn.lemma)
                else:
                    wordID = m_vocabulary.get(tkn.lemma)
                    m_chi_table[aspID][wordID] += 1
    return m_chi_table               
                           
# Count the number of hits between sentence tokens and keywords 
def AnnotateByKeywords(stn, keywords):
    count = 0
    for tkn in stn.ttoken:
        if tkn.lemma in keywords:
            count += 1
    return count        

# Rank the words under each aspect with respect to their 
# Chi-Square value and join the top K words for each aspect 
# into their corresponding aspect keyword list Ai   
def rankKeywordsByChi(m_chi_table, m_vocabulary, m_aspectkeywords, m_ranklist):
    wordID = -1
    aspectID = -1 
    chiV = 0.0
    for value in m_vocabulary.values():
        wordID = value
        maxChi = 0.0
        selectedID = -1
        for aspectID in range(len(m_aspectkeywords)):
            chiV = m_chi_table[aspectID][wordID]
            if (chiV > 4.0 * maxChi):
                maxChi = chiV
                selectedID = aspectID
        for aspectID in range(len(m_aspectkeywords)):
            if aspectID is not selectedID:
                    m_chi_table[aspectID][wordID] = 0.0
    
    aspectID = 0;
    extended = False
    for asp_key, asp_values in m_aspectkeywords.items():
        oldaspectLen = len(asp_values)
        for key, value in m_ranklist.items():
            wordID = m_vocabulary[key]
            m_ranklist[key] = m_chi_table[aspectID][wordID]                       
        m_rank_list = sorted(m_ranklist.items(), key=operator.itemgetter(1), reverse=True)
        
        # Retrieve Top K words dependent on Aspect under consideration
        topK_aspect_words = [kw[0] for kw in m_rank_list[:chi_topK]]
        asp_values.extend(topK_aspect_words)
        m_aspectkeywords[asp_key] = list(set(asp_values))
        if len(list(set(asp_values))) is not oldaspectLen:
            extended = True
        aspectID += 1
            
    return extended, m_aspectkeywords       
                    
def BootStrapping(m_sentences, m_vocabulary, m_aspectkeywords):
    print ("Vocabulary Size:", len(m_vocabulary))
    it = 0
    while True:
        m_chi_table, m_ranklist = chiSquareTest(m_sentences, m_vocabulary, m_aspectkeywords)
        print ("Bootstrapping for",it,"iterations...")
        it += 1
        extended, m_aspectkeywords = rankKeywordsByChi(m_chi_table, m_vocabulary, m_aspectkeywords, m_ranklist)
        if (extended and it<chi_iter):
            continue
        else:
            print ("Aspect Keywords not changing or iteration limit exceeds. Converging Bootstrapping algorithm for",it,"iteration.")
            break
    return m_sentences, m_aspectkeywords    
