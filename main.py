from tkinter import font
from dir import CreationMdp
import json
from tkinter import *
import tkinter.messagebox
import pyperclip
#from cryptography.fernet import Fernet
#La librairie "cryptography" me permettera d'ecnrypter les données présentes
#Le mdp global est "123" et se trouve aussi dans "config.json"

class Programme_Main(object):
    def __init__(self):
        # Declaration fenetre main
        self.fenetre1 = Tk()
        self.config = "config.json"
        self.fenetre1.title("Gestionnaire de Password 6TT")
        with open (self.config, "r") as f:
            temp = json.load(f)
            self.dict = temp[0]
            self.nom_utilisateur = self.dict["nom_utilisateur"]
        if self.dict["lightordark"] == "1":
            self.current_bg = "#0F0E0E"
            self.current_fg = "#ffffff"
        else:
            self.current_bg = "#ffffff"
            self.current_fg = "#0F0E0E"
        self.fenetre1.config(bg =self.current_bg, padx = 5, pady = 5)
        self.fichier = "infos.json"
        self.mdp_char_limit = 30
        self.plat_char_limit = 15
        # Barre Menu
        self.barremenu = Menu(self.fenetre1)
        self.fenetre1.config(menu = self.barremenu)
        self.fichier_menu = Menu(self.barremenu, tearoff = 0)
        self.barremenu.add_cascade(label = "Programme", menu = self.fichier_menu)
        self.fichier_menu.add_command(label = "Nouveau MDP [Ctrl + N]", command=self.nouveau_mdp)
        self.fichier_menu.add_command(label = "Actualiser [Ctrl + R]", command=self.actualiser_mdps)
        self.fichier_menu.add_separator()
        self.fichier_menu.add_command(label = "Quitter [Escape]", command=self.quitter)
        
        self.apparence_menu = Menu(self.barremenu, tearoff = 0)
        self.barremenu.add_cascade(label = "Apparence", menu = self.apparence_menu)
        self.apparence_menu.add_command(label = "Mode clair", command=self.go_lightmode)
        self.apparence_menu.add_command(label = "Mode sombre", command=self.go_darkmode)
        
        self.user_menu = Menu(self.barremenu, tearoff = 0)
        self.barremenu.add_cascade(label = "Utilisateur", menu = self.user_menu)
        self.user_menu.add_command(label = "Changer Nom Utilisateur", command=self.changer_username)
        self.user_menu.add_command(label = "Changer MDP global", command=self.changer_mdp_global)

        self.apropos_menu = Menu(self.barremenu, tearoff = 0)
        self.barremenu.add_cascade(label = "À propos", menu = self.apropos_menu)
        self.apropos_menu.add_command(label = "Informations", command=self.informations)

        self.frame_dessus1 = Frame(self.fenetre1,bg=self.current_bg)
        self.frame_dessus1.pack(side=TOP,padx=5,pady=5)
        #
        self.texte_dessus1 = Label(self.frame_dessus1,text=(f"Bienvenue {self.nom_utilisateur} !"), font=(30), bg=self.current_bg, fg=self.current_fg)
        self.texte_dessus1.pack(side=TOP,padx=5,pady=5) 
        #
        self.frame_milieu = Frame(self.fenetre1,bg=self.current_bg)
        self.frame_milieu.pack(side=TOP,padx=5,pady=5)
        # 
        self.texte_milieu_1 = Label(self.frame_milieu,text="Aucune Plateforme et MDP sauvegardés", font=(15), bg=self.current_bg, fg=self.current_fg)
        self.texte_milieu_1.pack(side=LEFT,padx=5,pady=5) 
        #
        self.canvas1 = Canvas(self.fenetre1, width = 400, height = 200, bg=self.current_bg, )
        self.canvas1.pack()
        self.canvas1.create_text(100, 20, text="Entrez le numéro du MDP :", fill=self.current_fg, font=(5))
        self.entry1 = Entry(self.fenetre1)
        self.canvas1.create_window(100, 45, window=self.entry1)
        self.button2 = Button(text='Aléatoiriser le MDP', command=self.aleatoire_mdp)
        self.canvas1.create_window(100, 75, window=self.button2)
        self.button5 = Button(text='Copier le MDP', command=self.copier_mdp)
        self.canvas1.create_window(100, 105, window=self.button5)
        self.button1 = Button(text='Supprimer', command=self.supprimer_mdp)
        self.canvas1.create_window(100, 135, window=self.button1)

        self.entry3 = Entry(self.fenetre1)
        self.entry4 = Entry(self.fenetre1)
        self.entry3.focus()
        self.canvas1.create_text(300, 20, text="Entrez votre nouveau MDP :", fill=self.current_fg, font=(20))
        self.canvas1.create_text(300, 40, text="Plateforme :", fill=self.current_fg, font=(12))
        self.canvas1.create_window(300, 60, window=self.entry3)
        self.canvas1.create_text(300, 80, text="Mot de passe :", fill=self.current_fg, font=(12))
        self.canvas1.create_window(300, 100, window=self.entry4)
        self.boutton3 = Button(text='Enter', command=self.nouveau_mdp_main)
        self.canvas1.create_window(300, 130, window=self.boutton3)
        self.var1 = IntVar()
        self.checkbox1 = Checkbutton(self.fenetre1, text='Mot de passe aléatoire',variable=self.var1, onvalue=1, offvalue=0, command=None)
        self.canvas1.create_window(300, 160, window=self.checkbox1)
        self.a = ""
        self.b = ""  
        self.fenetre1.bind("<Escape>",self.vers_quitter)   
        self.fenetre1.bind("<Delete>",self.go_supprimer_mdp)  
        self.fenetre1.bind("<Tab>",self.go_aleatoire_mdp) 
        self.fenetre1.bind("<Return>",self.go_nouveau_mdp_main)   
        self.fenetre1.bind("<Control_L>"+"<n>",self.vers_nouveau_mdp)  
        self.fenetre1.bind("<Control_L>"+"<r>",self.vers_actualiser_mdp)    

    def vers_actualiser_mdp(self, event):
        self.actualiser_mdps

    def actualiser_mdps(self):
        self.x = 1
        with open (self.fichier, "r") as f:
            self.temp = json.load(f)
            if self.temp == []:
                self.texte_milieu_1.config(text="Aucune Plateforme et MDP sauvegardés", justify='left')
                pass
            for i in self.temp:
                self.a += str(self.x) + ") " + (("  Plateforme : ") + str(i["plateforme"]) + (("    Mdp : ") + str(i["mdp"])) + "\n")
                self.texte_milieu_1.config(text=str("\n" + self.a), justify='left')
                self.x += 1
            self.a = ""
    
    def go_supprimer_mdp(self, event):
        self.supprimer_mdp()
    
    def supprimer_mdp(self):
        self.nouv_donne = []
        with open (self.fichier, "r") as j:
            self.temp = json.load(j)
            self.x = 1
        for item in self.temp:
            if str(self.x) == str(self.entry1.get()):
                pass
                self.x += 1
            else:
                self.nouv_donne.append(item)
                self.x += 1
        with open (self.fichier, "w") as j:
            json.dump(self.nouv_donne, j, indent=4)
        
        self.actualiser_mdps()
    
    def vers_nouveau_mdp(self, event):
        self.nouveau_mdp()

    def nouveau_mdp(self):
        self.fenetre3 = Toplevel(self.fenetre1)
        with open (self.config, "r") as f:
            temp = json.load(f)
            self.dict = temp[0]
        if self.dict["lightordark"] == "1":
            self.current_bg = "#0F0E0E"
            self.current_fg = "#ffffff"
        else:
            self.current_bg = "#ffffff"
            self.current_fg = "#0F0E0E"
        self.creationmdp = CreationMdp()
        self.fenetre3.title("Gestionnaire de Password 6TT")
        self.fenetre3.config(bg=self.current_bg, padx = 5, pady = 5)
        self.canvas4 = Canvas(self.fenetre3, width = 400, height = 200, bg=self.current_bg)
        self.canvas4.pack()
        self.entry10 = Entry(self.fenetre3)
        self.entry11 = Entry(self.fenetre3)
        self.entry10.focus()
        self.canvas4.create_text(200, 20, text="Entrez votre nouveau MDP :", fill=self.current_fg, font=(20))
        self.canvas4.create_text(200, 40, text="Plateforme :", fill=self.current_fg, font=(12))
        self.canvas4.create_window(200, 60, window=self.entry10)
        self.canvas4.create_text(200, 80, text="Mot de passe :", fill=self.current_fg, font=(12))
        self.canvas4.create_window(200, 100, window=self.entry11)
        self.var2 = IntVar()
        self.checkbox2 = Checkbutton(self.fenetre3, text='Mot de passe aléatoire',variable=self.var2, onvalue=1, offvalue=0, command=None)
        self.canvas4.create_window(200, 160, window=self.checkbox2)
        self.boutton7 = Button(self.canvas4, text='Enter', command=self.nouveau_mdp_topniveau)
        self.canvas4.create_window(200, 130, window=self.boutton7)

    def nouveau_mdp_topniveau(self):
        self.mdp = {}
        if self.var2.get() == 0:
            if len(self.entry11.get()) <= self.mdp_char_limit and len(self.entry10.get()) <= self.plat_char_limit:
                with open (self.fichier, "r") as f:
                    self.temp = json.load(f)
                    self.mdp["plateforme"] = self.entry10.get()
                    self.mdp["mdp"] = self.entry11.get()
                    self.temp.append(self.mdp)
        
                with open (self.fichier, "w") as j:
                    json.dump(self.temp, j, indent=4)
            else:
                print("Mdp ou plateforme trop long. (-= 45 char oblg")
        
        else:
            if len(self.entry10.get()) <= self.plat_char_limit:
                with open (self.fichier, "r") as f:
                    self.temp = json.load(f)
                    self.mdp["plateforme"] = self.entry10.get()
                    self.creationmdp.melangeur_mdp()
                    self.mdp["mdp"] = self.creationmdp.mdp
                    self.temp.append(self.mdp)
        
                with open (self.fichier, "w") as j:
                    json.dump(self.temp, j, indent=4)
            else:
                print("Plateforme trop longue (-= 15 char oblg).")
        
        self.actualiser_mdps()

    def go_aleatoire_mdp(self, event):
        self.aleatoire_mdp()
    
    def aleatoire_mdp(self):
        self.lolmdp = CreationMdp()
        self.nouv_donne = []
        with open (self.fichier, "r") as j:
            self.temp = json.load(j)
            self.x = 1
        for self.item in self.temp:
            if str(self.x) == str(self.entry1.get()):
                self.nouv_item = {}
                self.lolmdp.melangeur_mdp()
                self.nouv_item["plateforme"] = self.item["plateforme"]
                self.nouv_item["mdp"] = self.lolmdp.mdp
                self.nouv_donne.append(self.nouv_item)
                self.x += 1
            else:
                self.nouv_donne.append(self.item)
                self.x += 1
        with open (self.fichier, "w") as j:
            json.dump(self.nouv_donne, j, indent=4)
        self.actualiser_mdps()
    
    def go_nouveau_mdp_main(self, event):
        self.nouveau_mdp_main()

    def nouveau_mdp_main(self):
        self.creationmdp = CreationMdp()
        self.mdp = {}
        if self.var1.get() == 0:
            if len(self.entry4.get()) <= self.mdp_char_limit and len(self.entry3.get()) <= self.plat_char_limit:
                with open (self.fichier, "r") as f:
                    self.temp = json.load(f)
                    self.mdp["plateforme"] = self.entry3.get()
                    self.mdp["mdp"] = self.entry4.get()
                    self.temp.append(self.mdp)
        
                with open (self.fichier, "w") as j:
                    json.dump(self.temp, j, indent=4)
            else:
                print("Mdp ou plateforme trop long. (-= 45 char oblg")
        
        else:
            if len(self.entry1.get()) <= self.plat_char_limit:
                with open (self.fichier, "r") as f:
                    self.temp = json.load(f)
                    self.mdp["plateforme"] = self.entry3.get()
                    self.creationmdp.melangeur_mdp()
                    self.mdp["mdp"] = self.creationmdp.mdp
                    self.temp.append(self.mdp)
        
                with open (self.fichier, "w") as j:
                    json.dump(self.temp, j, indent=4)
            else:
                print("Plateforme trop longue (-= 15 char oblg).")
        
        self.actualiser_mdps()
    
    def copier_mdp(self):
        with open (self.fichier, "r") as j:
            self.temp = json.load(j)
        self.x = 1
        for item in self.temp:
            if str(self.x) == str(self.entry1.get()):
                self.data = item["mdp"]
                pyperclip.copy(item["mdp"])
                break
            else:
                self.x += 1
    
    def vers_quitter(self,event):
        self.quitter()
    
    def quitter(self):
        self.fenetre1.quit()
        self.fenetre1.destroy()
    
    def go_darkmode(self):
        self.liste = []
        self.nouvelle_donnee = {}
        with open (self.config, "r") as f:
            temp = json.load(f)
            self.dict = temp[0]
            self.nouvelle_donnee["mdp_global"] = self.dict["mdp_global"]     
            self.nouvelle_donnee["lightordark"] = "1"   
            self.nouvelle_donnee["nom_utilisateur"] = self.dict["nom_utilisateur"]    
            self.liste.append(self.nouvelle_donnee)
        with open (self.config, "w") as f:
            json.dump(self.liste, f, indent=4)
        self.fenetre1.destroy()
        self.__init__()
        self.actualiser_mdps()

    def go_lightmode(self):
        self.liste = []
        self.nouvelle_donnee = {}
        with open (self.config, "r") as f:
            temp = json.load(f)
            self.dict = temp[0]
            self.nouvelle_donnee["mdp_global"] = self.dict["mdp_global"]     
            self.nouvelle_donnee["lightordark"] = "2"   
            self.nouvelle_donnee["nom_utilisateur"] = self.dict["nom_utilisateur"]    
            self.liste.append(self.nouvelle_donnee)
        with open (self.config, "w") as f:
            json.dump(self.liste, f, indent=4)
        self.fenetre1.destroy()
        self.__init__()
        self.actualiser_mdps()
    
    def changer_username(self):
        self.fenetre7 = Toplevel(self.fenetre1)
        with open (self.config, "r") as f:
            temp = json.load(f)
            self.dict = temp[0]
        if self.dict["lightordark"] == "1":
            self.current_bg = "#0F0E0E"
            self.current_fg = "#ffffff"
        else:
            self.current_bg = "#ffffff"
            self.current_fg = "#0F0E0E"
        self.fenetre7.title("Gestionnaire de Password 6TT")
        self.fenetre7.config(bg=self.current_bg, padx = 5, pady = 5)
        self.canvas5 = Canvas(self.fenetre7, width = 200, height = 110, bg=self.current_bg)
        self.canvas5.pack()
        self.entry15 = Entry(self.fenetre7)
        self.entry15.focus()
        self.canvas5.create_text(100, 20, text="Entrez votre nom :", fill=self.current_fg, font=(20))
        self.canvas5.create_window(100, 45, window=self.entry15)
        self.boutton15 = Button(self.canvas5, text='Enter', command=self.go_changer_username)
        self.canvas5.create_window(100, 80, window=self.boutton15)
    
    def go_changer_username(self):
        self.liste1 = []
        self.nouvelle_donnee1 = {}
        with open (self.config, "r") as f:
            temp1 = json.load(f)
            self.dict1 = temp1[0]
            self.nouvelle_donnee1["mdp_global"] = self.dict1["mdp_global"]     
            self.nouvelle_donnee1["lightordark"] = self.dict1["lightordark"]   
            self.nouvelle_donnee1["nom_utilisateur"] = self.entry15.get()    
            self.liste1.append(self.nouvelle_donnee1)
        with open (self.config, "w") as f:
            json.dump(self.liste1, f, indent=4)
        self.fenetre1.destroy()
        self.__init__()
        self.actualiser_mdps()
    
    def changer_mdp_global(self):
        self.fenetre8 = Toplevel(self.fenetre1)
        with open (self.config, "r") as f:
            temp = json.load(f)
            self.dict = temp[0]
        if self.dict["lightordark"] == "1":
            self.current_bg = "#0F0E0E"
            self.current_fg = "#ffffff"
        else:
            self.current_bg = "#ffffff"
            self.current_fg = "#0F0E0E"
        self.fenetre8.title("Gestionnaire de Password 6TT")
        self.fenetre8.config(bg=self.current_bg, padx = 5, pady = 5)
        self.canvas6 = Canvas(self.fenetre8, width = 250, height = 110, bg=self.current_bg)
        self.canvas6.pack()
        self.entry16 = Entry(self.fenetre8)
        self.entry16.focus()
        self.canvas6.create_text(125, 20, text="Entrez votre nouveau MDP :", fill=self.current_fg, font=(20))
        self.canvas6.create_window(125, 45, window=self.entry16)
        self.boutton16 = Button(self.canvas6, text='Enter', command=self.go_changer_mdp_global)
        self.canvas6.create_window(125, 80, window=self.boutton16)
    
    def go_changer_mdp_global(self):
        self.liste2 = []
        self.nouvelle_donnee2 = {}
        with open (self.config, "r") as f:
            temp2 = json.load(f)
            self.dict2 = temp2[0]
            self.nouvelle_donnee2["mdp_global"] = self.entry16.get()    
            self.nouvelle_donnee2["lightordark"] = self.dict2["lightordark"]   
            self.nouvelle_donnee2["nom_utilisateur"] = self.dict2["nom_utilisateur"]
            self.liste2.append(self.nouvelle_donnee2)
        with open (self.config, "w") as f:
            json.dump(self.liste2, f, indent=4)
        self.fenetre1.destroy()
        self.__init__()
        self.actualiser_mdps()

    def informations(self):
        tkinter.messagebox.showinfo(title="Gestionnaire de Password 6TT", message="Réalisé par Sean vergauwen")

class Login_Page(object):
    def __init__(self):
        self.config = "config.json"
        with open (self.config, "r") as f:
            temp = json.load(f)
            self.dict = temp[0]
        if self.dict["lightordark"] == "1":
            self.current_bg = "#0F0E0E"
            self.current_fg = "#ffffff"
        else:
            self.current_bg = "#ffffff"
            self.current_fg = "#0F0E0E"
        self.login = True
        # importation des librairies
        self.creation_mdp_obj = CreationMdp()
        # Interface graphique
        self.fenetre = Tk()
        self.fenetre.title("Gestionnaire de Password 6TT")
        self.fenetre.config(bg=self.current_bg, padx = 5, pady = 5)
        self.fenetre.geometry("400x300")
        # declaration Canvas
        self.canvas1 = Canvas(self.fenetre, width = 400, height = 300, bg=self.current_bg)
        self.canvas1.pack()
        self.canvas1.create_text(200, 100, text="Entrez votre MDP global :", fill=self.current_fg, font=(20))
        self.entry1 = Entry(self.fenetre)
        self.entry1.focus()
        self.canvas1.create_window(200, 140, window=self.entry1)
        self.button1 = Button(text='Enter', command=self.verification)
        self.canvas1.create_window(200, 180, window=self.button1)
        self.fenetre.bind("<Return>",self.vers_verification) 

    def vers_verification(self, event):
        self.verification()

    def verification(self):
        self.mdp_general_input = self.entry1.get()
        with open (self.config, "r") as f:
            temp = json.load(f)
            self.dict = temp[0]
            if self.mdp_general_input == self.dict["mdp_global"]:
                self.fenetre.quit()
                self.fenetre.destroy()
                self.login = False
            else:
                print("Le MDP est 123")

if __name__ == "__main__":
    programme_login = Login_Page()
    programme_login.fenetre.mainloop()
    if programme_login.login == False:
        programme_obj = Programme_Main()
        programme_obj.actualiser_mdps()
        programme_obj.fenetre1.mainloop()
        