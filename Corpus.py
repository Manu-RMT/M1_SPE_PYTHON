from Classes import Author

# =============== 2.7 : CLASSE CORPUS ===============
class Corpus:
    def __init__(self, nom):
        self.nom = nom
        self.authors = {}
        self.aut2id = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0
    
    # ajout d'un document dans le corpus     
    def add(self, doc):
        if doc.auteur not in self.aut2id:
            self.naut += 1
            self.authors[self.naut] = Author(doc.auteur)
            self.aut2id[doc.auteur] = self.naut
        self.authors[self.aut2id[doc.auteur]].add(doc.texte)

        self.ndoc += 1
        self.id2doc[self.ndoc] = doc
    
    # tri du titre des documents
    def tri_alphabetique(self, n_docs=-1):
        docs = list(self.id2doc.values())
        docs = list(sorted(docs, key=lambda x: x.titre.lower()))
        return docs
    
    # affichage des documents
    def show(self, n_docs=-1, tri="abc"):
        docs = list(self.id2doc.values())
        if tri == "abc":  # Tri alphabÃ©tique
            docs = list(sorted(docs, key=lambda x: x.titre.lower()))[:n_docs]
        elif tri == "123":  # Tri temporel
            docs = list(sorted(docs, key=lambda x: x.date))[:n_docs]

        print("\n".join(list(map(repr, docs))))
    
    # representation des documents
    def __repr__(self):
        docs = list(self.id2doc.values())
        docs = list(sorted(docs, key=lambda x: x.titre.lower()))

        return "\n".join(list(map(str, docs)))
    
    # recupèration des champs d'un document
    def values_corpus(self):
        lst1 = []
        lst2 = []
        lst3 = []
        lst4 = []
        lst5 = []
        lst6 = []
        for key in self.id2doc.keys():
            lst1.append(self.id2doc[key].nature)
            lst2.append(self.id2doc[key].titre)
            lst3.append(self.id2doc[key].auteur)
            lst4.append(self.id2doc[key].date)
            lst5.append(self.id2doc[key].url)
            lst6.append(self.id2doc[key].texte)
        return lst1,lst2,lst3,lst4,lst5,lst6      
        

