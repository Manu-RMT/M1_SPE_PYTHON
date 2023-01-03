import praw
import urllib.request
from Classes import Document
from Classes import Author
from Corpus import Corpus
from os import path
from fastbm25 import fastbm25
import datetime
import pickle
import pandas as pd
import os.path


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
    df = pd.read_csv('corpus.csv', sep=';',engine='python')
    return df

def nombre_apparition_mot(): 
    corpus = load_data('corpus.csv')    
    # tokenized_corpus = [doc.lower().split(" ") for doc in corpus]
    # model = fastbm25(tokenized_corpus)
    # query = "Spanish"
    # result = model.top_k_sentence(query,k=1)
    #print(result)
    
    # tokenized_corpus = [doc.split(" ") for doc in arary_corpus.shape(1)]
    # print(tokenized_corpus)
    # model = fastbm25(tokenized_corpus)
    # query = "football"
    # result = model.top_k_sentence(query,k=1)
    # print(result)
    

# Programme qui sera lancer lorsqu'on clique sur le bouton de l'interface
def main():
    # si le corpus n'existe pas encore on le charge dans le CSV
    file = path.exists('corpus.csv')
    if not file :
    
        # Identification
        reddit = praw.Reddit(client_id='5DDK45r5absaCcU6Cwh_KQ', client_secret='M-1Sons8RJU9EAQffSfpuvJXKIYzPQ',
                             user_agent='td3_python')
        
        # Requête
        limit = 100
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
    nombre_apparition_mot()         

main()