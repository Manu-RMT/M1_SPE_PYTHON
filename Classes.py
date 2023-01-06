import datetime

# =============== La classe Document ===============
class Document:
    # Initialisation des variables de la classe
    def __init__(self,nature ="", titre="", auteur="", date="", url="", texte=""):
        self.nature = nature
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte


    # Fonction qui renvoie le texte à afficher lorsqu'on tape repr(classe)
    def __repr__(self):
        return f"Titre : {self.titre}\tAuteur : {self.auteur}\tDate : {self.date}\tURL : {self.url}\tTexte : {self.texte}\t"
    
    # Fonction qui renvoie le texte à afficher lorsqu'on tape str(classe)
    def __str__(self):
        return f"{self.nature} ; {self.titre} ; {self.auteur} ; {self.date} ; {self.url} ; {self.texte}"
    


# ===============  La classe Author ===============
class Author:
    def __init__(self, name):
        self.name = name
        self.ndoc = 0
        self.production = []
    
    # ajout d'un document dans la liste de production d'un auteur + gere le nombre    
    def add(self, production):
        self.ndoc += 1
        self.production.append(production)
    
    # Fonction qui renvoie le texte à afficher lorsqu'on tape str(classe)
    def __str__(self):
        return f"Auteur : {self.name}\t# productions : {self.ndoc}"
    
    
# ============== H�ritage de document  ===============
class RedditDocument(Document):
    def __init__(self, titre: str, auteur: str, date: datetime, url: str, texte: str, type_source: str,
                 nb_commentaire: int):
        super().__init__(titre, auteur, date, url, texte, type_source)
        self.nb_commentaire = nb_commentaire

    def getNbComm(self):
        return self.nb_commentaire

    def setNbComm(self, nb_comm: int):
        self.nb_commentaire = nb_comm

    def getType(self):
        return self.type_source

    def __str__(self):
        self.getNbComm()


# Herite de document qui gere en plus les articles de co-auteurs
class ArxivDocument(Document):
    def __init__(self, titre: str, auteur: str, date: datetime, url: str, texte: str, type_source: str,
                 array_nom_auteur: list):
        Document.__init__(self, titre, auteur, date, url, texte, type_source)
        self.nom_co_auteur = array_nom_auteur

    def getType(self):
        return self.type_source
    