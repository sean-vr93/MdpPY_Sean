import random
#from cryptography.fernet import Fernet

class CreationMdp(object):
    def __init__(self):
        self.mdp_lenght = 16
        self.mdp = ""
        self.grandes_lettres = "AZERTYUIOPQSDFGHJKLMWXCVBN"
        self.petites_lettres = "azertyuiopqsdfghjklmwxcvbn"
        self.nombres = "0123456789"
        self.symboles = "(),.;/:=+*-[]%#@&<>!?_"
        self.all = str(self.grandes_lettres+self.petites_lettres+self.nombres+self.symboles)

    def melangeur_mdp(self):
        self.mdp = ""
        for loop in range(self.mdp_lenght):
            self.mdp += random.choice(self.all)
        print(self.mdp)
