import math

class Contenu:
    def __init__(self,title,categorie,rating):
        self.title = title
        self.categorie = categorie
        self.rating = rating
        self.votes_num = 1
    
    def update_rating(self, note):
        self.rating = (self.rating * self.votes_num + note) / (self.votes_num + 1)
        self.votes_num += 1

    def __str__(self):
        return f"{self.title}/{self.categorie}/{self.rating:.2f}/{self.votes_num}votes"
    
    def __eq__(self, other):
        return self.categorie == other.categorie  # egalité entre les contenus signifie qu'ils ont la meme categorie
    
    def __lt__(self, other):
        return self.rating < other.rating    # un contenu est sup à un autre si c le cas pour son rating 
    
    def similarite(self,other):
        score = 0                      # max 4
        if(type(self) == type(other)): #film , cours , .....
            #score += 1
            if isinstance(self,Film):
                score += 1 - abs(self.duration - other.duration)/100

            if isinstance(self,Cours):
                if self.level == other.level :
                    score += 1
            
            if isinstance(self,Livre):
                if self.auteur == other.auteur :
                    score += 1
        
        if(self.categorie == other.categorie): #drama,action,...
            score += 1
        
        score += 1 - abs(self.rating - other.rating)/10  #la difference entre les notes augmente-->la similarité diminue

        return score 
        

class Film(Contenu):
    def __init__(self, title, categorie, rating,duration):
        super().__init__(title, categorie, rating)
        self.duration = duration
    
class Livre(Contenu):
    def __init__(self,title,categorie,rating,auteur):
        super().__init__(title,categorie,rating)
        self.auteur = auteur 

class Cours(Contenu):
    def __init__(self, title, categorie, rating,level):
        super().__init__(title, categorie, rating)
        self.level = level

# INTERACTION

class Interaction:
    def __init__(self, content):
        self.content = content
        self.consulted = False
        self.note = None

class User : 
    def __init__(self,preferences):
        self.preferences = preferences
        self.historique={}
    
    def consulter(self,content):
       if content.title not in self.historique:
            self.historique[content.title] = Interaction(content)
       self.historique[content.title].consulted = True

    def noter(self,content,note):
       if content.title not in self.historique:
            self.historique[content.title] = Interaction(content)
       self.historique[content.title].consulted = True  # car impossible de noter sans consulter 
       self.historique[content.title].note = note
       content.update_rating(note)
    
    def note_system(self,note):
        return note
    
    def __add__(self,content):      # u1 + film = u1.consulter(film)
        self.consulter(content)
        return self
    
    def __contains__(self,content):
        return content.title in self.historique      # film in u1   True / False
    
    def pref_score(self,content):
        return 1 if content.categorie in self.preferences else 0.5
    
    def rating_score(self, content):
        return content.rating / 10
    
    def history_similarity(self,content):
        liked = []
        for inter in self.historique.values():
            note_transformee = self.note_system(inter.note)
            if note_transformee is not None and note_transformee >= 7 : 
                liked.append(inter.content)
        total = 0
        for c in liked:
            total += content.similarite(c)
        if len(liked)==0 :
            return 0
        return total / len(liked) 
    
    def score(self,content):
        P = self.pref_score(content)
        R = self.rating_score(content)
        H = self.history_similarity(content) / 3 
        return (0.5 * H + 0.3 * P + 0.2 * R)*math.exp(H-1)
    
    def recommender(self,contenues):
        recomendations=[]
        for content in contenues : 
            if content.title in self.historique : #deja consulter
                continue
            score = self.score(content)
            recomendations.append((content,score))
        recomendations.sort(key=lambda x: x[1], reverse=True)
        return [c for c, s in recomendations]

class UserExigeant(User):
    def note_system(self,note):
        return min(10,note+1)

class UserGenereux(User):
    def note_system(self,note):
        return max(0,note-1)

########### Test ######################

# SCENARIO 1 : L'utilisateur a un historique clair → le système doit recommander des contenus similaires

f1 = Film("Inception",    "sci-fi", 8, 148)
f2 = Film("Interstellar", "sci-fi", 9, 169)
f3 = Film("Avengers",     "action", 8, 140)
l1 = Livre("Dune",        "sci-fi", 9.1, "Herbert")
c1 = Cours("Astrophysique","sci-fi", 7.5, "advanced")

catalogue = [f1, f2, f3, l1, c1]

u = User(["sci-fi"])
u.noter(f1, 9)   # a adoré Inception (sci-fi)
print("============================ SCENARIO 1 : Fan de sci-fi ==========")
for c in u.recommender(catalogue):
    print(c.title)

# SCENARIO 2 : Deux utilisateurs, mêmes préférences,mais comportements opposés
print("\n======================== SCENARIO 2 : ExiGeant vs Généreux ===")

catalogue = [f1, f2, f3]

u_e = UserExigeant(["sci-fi"])
u_g = UserGenereux(["sci-fi"])

# Les deux donnent la même note
u_e.noter(f1, 6)   #   7 (Inception compte comme "aimé")
u_g.noter(f1, 6)   #  5 
rec_e = u_e.recommender(catalogue)
rec_g = u_g.recommender(catalogue)

print("\n******Recommandations ExiGeant :")
for c in rec_e:
    print(c.title)

print("*********Recommandations Généreux ")
for c in rec_g:
    print(c.title)

# SCENARIO 3 : Utilisateur avec goûts mixtes le système doit équilibrer les recommandations
print("\n=== SCENARIO 3 : Goûts mixtes ===")

f1 = Film("Avengers",     "action",  8.0, 140)
f2 = Film("The killer",    "action",   7.8, 195)
l1 = Livre("Harry Potter","fantasy", 9.0, "Rowling")
l2 = Livre("Clean Code",  "tech",    8.7, "Martin")
c1 = Cours("AI Basics",   "tech",    9.2, "advanced")

catalogue = [f1, f2, l1, l2, c1]

u = User(["action", "tech"])
u.noter(f1, 8)   # aime l'action
u.noter(l2, 9)   # aime aussi la tech
for c in u.recommender(catalogue):
    print(c.title)
