import praw
import urllib.request
import xmltodict
import datetime
import pickle
import pandas as pd
import os.path
import csv
import re
import nltk
import math
from Classes import Document
from Classes import Author
from Corpus import Corpus
from os import path
from nltk.corpus import stopwords

# Fonction affichage hiérarchie dict
def showDictStruct(d):
    def recursivePrint(d, i):
        for k in d:
            if isinstance(d[k], dict):
                print("-" * i, k)
                recursivePrint(d[k], i + 2)
            else:
                print("-" * i, k, ":", d[k])

    recursivePrint(d, 1)

def load_data(path_file :str):
     return pd.read_csv('corpus.csv',sep=';')
 
     
def crea_tf_tfxidf(df):
    nb_docs = len(df)
    tf={} #Dictionnaire de stockage des nombres d'apparition (articles reddit)
    doc_apparition = {} #Dictionnaire de stockage du nombre de documents dans lequels les mots apparaissent (articles reddit)
    tfxidf = {} #Dictionnaire de stockage des tfxidf (articles reddit)
    df['Words'] = df.iloc[:,0].copy()
    
    for i,texte in enumerate(df['Texte']):
        #Tokenization du texte et suppression des mots irrelevants
        texte = re.sub(r'[.,"\'-?:!;]','',texte) #Suppression des signes de ponctuation
        texte = texte.lower() #Transformation du texte en minuscule entièrement
        stripped = texte.split() #Découpage du texte
        words = [word for word in stripped if word.isalpha()] #Suppression des chiffres
        stop_words = set(stopwords.words('english')) #Enregistrement des stopwords anglais (the, for, in etc...)
        words = [w for w in words if not w in stop_words] #Suppression des stopwords 
        tokens = [word for word in words if len(word)>1] #Suppression des mots constitués de 1 seul caractère 
        df['Words'][i] = tokens #On range les mots dans une colonne du dataframe
        for token in tokens: #Parcours des mots retenus
            if token in tf.keys(): #Si le mot existe déjà dans le dictionnaire
                tf[token] += 1 #On augmente le term-frequency de 1
            else:
                tf[token] = 1 #Sinon on initialise le term_frequency à 1
    
        for word in tf.keys():
            doc_apparition[word] = 0 #Initialisation du nb de docs dans lequel il apparaît à 0
            for words_doc in df['Words']:
                if word in words_doc: #Si le mot apparaît dans les mots tokenizés d'un document
                    doc_apparition[word] += 1 #On ajoute 1
                    
            tfxidf[word] = math.log((1+nb_docs)/(1+doc_apparition[word]))
    
    return tf, tfxidf

def sort_tfxidf(dictionnaire, nb_words, desc):
    compteur = 0
    words = []
    tfxidf = []
    for word,value in dict(sorted(dictionnaire.items(), key = lambda item: item[1], reverse = desc)).items(): #liste qui trie les plus petits dfxidf
        compteur += 1
        print ("%s: %s" % (word, value))
        words.append(word)
        tfxidf.append(value)
        if compteur >= nb_words: #limite à 5
            break
    return words, tfxidf

def decoupage(df,value):
    df['Words'] = df.iloc[:,0].copy()
    data_ct=[] #Liste qui va contenir les documents contenant le mot 'value'
    data_nct=[] #Liste qui va contenir les documents qui ne contiennent pas le mot 'value'
    
    for i,texte in enumerate(df['Texte']):
        #Tokenization du texte et suppression des mots irrelevants
        texte = re.sub(r'[.,"\'-?:!;]','',texte) #Suppression des signes de ponctuation
        texte = texte.lower() #Transformation du texte en minuscule entièrement
        stripped = texte.split() #Découpage du texte
        words = [word for word in stripped if word.isalpha()] #Suppression des chiffres
        stop_words = set(stopwords.words('english')) #Enregistrement des stopwords anglais (the, for, in etc...)
        words = [w for w in words if not w in stop_words] #Suppression des stopwords 
        tokens = [word for word in words if len(word)>1] #Suppression des mots constitués de 1 seul caractère 
        df['Words'][i] = tokens #On range les mots dans une colonne du dataframe
        
        if bool(set(df['Words'][i]) & set(value)): #Si le vocabulaire du document et la liste value partage au moins un élément
            data_ct.append(df.iloc[i]) #On insère le document dans data_ct
        else:
            data_nct.append(df.iloc[i]) #On insère le document dans data_nct
    

    data_ct_value = pd.DataFrame(data_ct)
    data_nct_value = pd.DataFrame(data_nct)
            
    return data_ct_value, data_nct_value

def traitement_corpus(value_input): 
    
    corpus = load_data('corpus.csv') 
    contain_value,no_contain_value = decoupage(corpus, value_input)
    return len(contain_value),len(no_contain_value)
    
    # data_reddit = corpus[corpus['Nature']=='Reddit']
    # data_arxiv = corpus[corpus['Nature']=='ArXiv']
      
    # """Comparaisons top 10 tf/tfxidf --> A revoir"""
    # tf_arxiv, tfxidf_arxiv = crea_tf_tfxidf(data_arxiv) #Calcul des td, tfxidf de arxiv
    
    # top10_idf_arxiv = list(sort_tfxidf(tfxidf_arxiv,10,True)) #Récupération du top10 des tfxidf de arxiv
    
    # tf_reddit, tfxidf_reddit = crea_tf_tfxidf(data_reddit) #Calcul des td, tfxidf de reddit
    
    # top10_idf_arxiv.append([0]*len(top10_idf_arxiv[0])) #Initialisation d'une nouvelle colonne
    
    # for i, mot in enumerate(top10_idf_arxiv[0]): #Boucle sur les mots du top10 arxiv
    #     if mot in tfxidf_reddit.keys(): #Si présent dans le vocabulaire de reddit
    #         top10_idf_arxiv[-1][i] = tfxidf_reddit[mot] #On note le tfxidf de reddit dans la colonne créée avant la boucle
    
    # print(top10_idf_arxiv)
    # top10_idf_arxiv[2] = [b - a for b, a in zip(top10_idf_arxiv[1],top10_idf_arxiv[2])]
    
    # import matplotlib.pyplot as plt
    # plt.plot([1,2,3,4,5,6,7,8,9,10], top10_idf_arxiv[2])
    # """Comparaisons top 10 tf/tfxidf"""
    
    # """Comparaison taille de vocab"""
    # print("Taille du vocabulaire des documents Arxvi: "+str(len(tf_arxiv))+" mots")
    # print("Taille du vocabulaire des documents Reddit: "+str(len(tf_reddit))+" mots")
    # """Comparaison taille de vocab"""
    
    # """Affichage du top tfxidf des document Reddit"""
    # top20_idf_reddit = list(sort_tfxidf(tfxidf_reddit,20,True))
    # print("\n20 mots avec le plus grand tfxidf :")
    # print(top20_idf_reddit[0])
    # """Affichage du top tfxidf des document Reddit"""
    
    
    # """Affichage du top tfxidf des document Arxiv"""
    # top20_idf_arxiv = list(sort_tfxidf(tfxidf_arxiv,20,True))
    # print("\n20 mots avec le plus grand tfxidf :")
    # print(top20_idf_arxiv[0])
    # """Affichage du top tfxidf des document Arxiv"""
    
    # """Comptage des mots appartenants aux vocabulaire Arxiv et Reddit"""
    # nb_voc_commun = 0
    # for word in tfxidf_arxiv.keys():
    #     if word in tfxidf_reddit.keys():
    #         nb_voc_commun += 1
    # """Comptage des mots appartenants aux vocabulaire Arxiv et Reddit"""
    # return nb_voc_commun

# Programme qui sera lancer lorsqu'on clique sur le bouton de l'interface
def main(value_input):
    # si le corpus n'existe pas encore on le charge dans le CSV
    file = path.exists('corpus.csv')
    if not file :
    
        # Identification
        reddit = praw.Reddit(client_id='5DDK45r5absaCcU6Cwh_KQ', client_secret='M-1Sons8RJU9EAQffSfpuvJXKIYzPQ',
                             user_agent='td3_python')
        
        # Requête
        limit = 1000
        hot_posts = reddit.subreddit('football').hot(limit=limit)  # .top("all", limit=limit)#
        
        # Récupération du texte
        docs = []
        docs_bruts = []
        afficher_cles = False
        for i, post in enumerate(hot_posts):
            if i % 10 == 0: print("Reddit:", i, "/", limit)
            if afficher_cles:  # Pour connaître les différentes variables et leur contenu
                for k, v in post.__dict__.items():
                    pass
                    print(k, ":", v)    
        
            if post.selftext == "":  
                continue
            
            docs.append(post.selftext.replace("\n", " "))
            docs_bruts.append(("Reddit", post))
        
        # =============== 1.2 : ArXiv ===============
        
        # Paramètres
        query_terms = ["football"]
        max_results = len(docs) # recupère autant d'arxiv que de reddit
        
        # Requête
        url = f'http://export.arxiv.org/api/query?search_query=all:{"+".join(query_terms)}&start=0&max_results={max_results}'
        data = urllib.request.urlopen(url)
        
        # Format dict (OrderedDict)
        data = xmltodict.parse(data.read().decode('utf-8'))
        
        
        # Ajout résumés à la liste
        for i, entry in enumerate(data["feed"]["entry"]):
            if i % 10 == 0: print("ArXiv:", i, "/", limit)
            docs.append(entry["summary"].replace("\n", ""))
            docs_bruts.append(("ArXiv", entry))
            # showDictStruct(entry)
        
        # =============== 1.3 : Exploitation ===============
        print(f"# docs avec doublons : {len(docs)}")
        docs = list(set(docs))
        print(f"# docs sans doublons : {len(docs)}")
        
        for i, doc in enumerate(docs):
            print(f"Document {i}\t# caractères : {len(doc)}\t# mots : {len(doc.split(' '))}\t# phrases : {len(doc.split('.'))}")
            if len(doc) < 100:
                docs.remove(doc)
        
        longueChaineDeCaracteres = " ".join(docs)
        
        
        collection = []
        for nature, doc in docs_bruts:
            if nature == "ArXiv":  # Les fichiers de ArXiv ou de Reddit sont pas formatés de la même manière à ce stade.
        
                titre = doc["title"].replace('\n', '').replace('"','')  # On enlève les retours à la ligne
                try:
                    authors = ", ".join(
                        [a["name"] for a in doc["author"]])  # On fait une liste d'auteurs, séparés par une virgule
                except:
                    authors = doc["author"]["name"]  # Si l'auteur est seul, pas besoin de liste
                summary = doc["summary"].replace("\n", "")  # On enlève les retours à la ligne
                date = datetime.datetime.strptime(doc["published"], "%Y-%m-%dT%H:%M:%SZ").strftime(
                    "%Y/%m/%d")  # Formatage de la date en année/mois/jour avec librairie datetime
        
                doc_classe = Document(nature, titre, authors, date, doc["id"], summary)  # Création du Document
                collection.append(doc_classe)  # Ajout du Document à la liste.
        
            elif nature == "Reddit":
                titre = doc.title.replace("\n", '').replace('"','')
                auteur = str(doc.author)
                date = datetime.datetime.fromtimestamp(doc.created).strftime("%Y/%m/%d")
                url = "https://www.reddit.com/" + doc.permalink
                texte = doc.selftext.replace("\n", "")
        
                doc_classe = Document(nature, titre, auteur, date, url, texte)
        
                collection.append(doc_classe)
        
        id2doc = {}
        for i, doc in enumerate(collection):
            id2doc[i] = doc.titre
        
        
        # =============== 2.6 : DICT AUTEURS ===============
        authors = {}
        aut2id = {}
        num_auteurs_vus = 0
        
        # Création de la liste+index des Auteurs
        for doc in collection:
            if doc.auteur not in aut2id:
                num_auteurs_vus += 1
                authors[num_auteurs_vus] = Author(doc.auteur)
                aut2id[doc.auteur] = num_auteurs_vus
        
            authors[aut2id[doc.auteur]].add(doc.texte)
            
        # =============== 2.7, 2.8 : CORPUS ===============
        
        corpus = Corpus("Mon corpus")
        
        # Construction du corpus à partir des documents
        for doc in collection:
            corpus.add(doc)
            
        corpus_trie = corpus.tri_alphabetique()
               
        print("---------------- affichage du corpus -------------- \n")    
        print(corpus.__repr__())
        print("---------------- x -------------- \n")
        # =============== 2.9 : SAUVEGARDE ===============
        
        nature=corpus.values_corpus()[0]
        titre=corpus.values_corpus()[1]
        Auteur=corpus.values_corpus()[2]
        Date=corpus.values_corpus()[3]
        url=corpus.values_corpus()[4]
        texte=corpus.values_corpus()[5]
        
        df = pd.DataFrame(zip(nature,titre,Auteur,Date,url,texte), columns=['Nature','Titre','Auteur','Date','URL','Texte'])
        df.to_csv(r'corpus.csv',index=False,sep=';')
             
        print("Sauvegarde du corpus dans le CSV")
    else:
        print("\n Le fichier contenant le corpus existe deja, pas de sauvegarde de document \n")
    
   
    # Traitement corpus 
    x,y = traitement_corpus(value_input)         
    return x,y
