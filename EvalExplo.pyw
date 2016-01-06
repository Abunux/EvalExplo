#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, csv, time, re, subprocess
from threading import *
from Tkinter import *
from ttk import Frame, Button, Label, Style, Combobox, Entry
import tkMessageBox, Tkconstants, tkFileDialog

# ----------------------------------------------------------------------
#							EvalExplo
#
# 		Programme de création d'une fiche d'évaluation 
# 		pour les enseignements d'exploration en 2nde
#
#-----------------------------------------------------------------------
#
# Frédéric Muller (Lycée Arbez Carme, Bellignat)
#
# maths.muller@gmail.com
#
__version__ = "0.0.22"
# Projet démarré le 03/09/2015
# Dernière maj : 12/10/2015
#
# Licence CC BY-NC-SA
#
# N'hésitez pas à me signaler par mail tout bug ou amélioration possible ;-)
#
#-----------------------------------------------------------------------
#							Documentation
#-----------------------------------------------------------------------
#
# Installation sous win 7 :
# -------------------------
# 1) Détecter sa version de windows (32 bit ou 64 bit).
#
# 2) Installer Python 2.7 :
#		https://www.python.org/downloads/release/python-2710/
#
#	Important : cocher "Ajouter python.exe au path" pendant l'install
#
# 3) Installer MikTex (Basic Installer qui fait 180 Mo) :
#		http://miktex.org/download
#
#	Important : Sous Win7, lancer l'installeur en mode de compatibilité Windows Vista
#
# 4) Installer les paquets Latex suivant avec MikTek Package Manager (Admin) :
#	- babel-french
#	- pgf
#	- ms
#	- xcolor
#	- colortbl
#	- mptopdf
#
# 5) Installer Evince :
#		https://wiki.gnome.org/Apps/Evince/Downloads
#
# 6) Copier ce fichier (EvalExplo.pyw) et ListeEleve.csv dans le 
#	répertoire "Exploration", créé dans votre dossier personnel :
#		Par ex C:\\Users\Toto\Exploration
#
# 7) Double-cliquer sur EvalExplo.pyw pour le lancer et essayer de créer
#	une fiche pour tester si tout va bien.
#
# Utilisation :
# -------------
# - Au lancement, choir son enseignement, la classe pour laquelle vous
# 	voulez faire les fiches (ça peut être "Toutes") ainsi que le trimestre.
#
# - Remplissez vos fiches, vous pouvez changer d'élève avec CTRL + Flèches
#
# - Votre session est automatiquement sauvegardée quand vous quitez
#	et rechargée au lancement, dans le dossier "Exploration".
#	Le fichier de sauvegarde a pour schéma :
#			Année-Trimestre-Classe-Option.csv
#	Vous pouvez effacer (ou renommer) ce fichier pour reprendre à zéro.
#	Vous pouvez également vous transmettre ce fichier pour travailler à plusieurs.
#
# - Vous pouvez créer chaque fiche individuellement, ou créer d'un coup 
#	toutes les fiches de votre session. Les pdf générés sont stockés
#	dans votre dossier "Exploration"
#
# - Vous pouvez générer un fichier texte avec toutes vos appréciations
#	pour les copier-coller dans Pronote.
#
# - Il y a un bloc note à droite pour copier-coller vos appréciations ou
#	prendre des notes. Il est sauvegardé dans "Appréciations.txt".
#
# Aspects techniques :
# --------------------
# - Le fichier ListeEleve.csv contient sur chaque ligne les infos des 
#	élèves. Chaque ligne est sous le modèle :
#		Nom,Prénom,Classe(juste le numéro),Option
#	Par exemple :
#		Durant,Pierre,3,MPS
#
#	Un .csv est un fichier tableur au format texte. Chaque ligne de ce
#	fichier correspond à une ligne du tableau. 
#	Pour ListeEleves.csv le séparateur est la virgule : ,
#	Vous pouvez le générer avec un tableur en choisissant le format CSV
#	au moment de la sauvegarde.
#
# - La session est sauvegardée dans un fichier .csv dont le séparateur est #
#	Chaque ligne est sous le modèle :
#		Nom#Prénom#Classe#Option#Année#Trimestre#Note1#Note2#Note3#Note4#Appréciation
#	(Note va de 0 à 3)
#	Vous pouvez donc éditer votre session au tableur
#
# - Vous pouvez modifier les critères et les items en changeant les variables 
#	CRITERE1, CRITERE2, CRITERE3 et CRITERE4 ci-dessous.
#	Le 1er terme de la liste est le nom du critère et les 4 suivants 
#	sont les items classés du plus faible au plus fort
#
# - Vous pouvez également changer les différentes variables globales 
#	pour adapter à vos besoin (CLASSE, OPTIONS), ainsi que la mise en
#	page de la fiche (voir descriptions).
#
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
# 				Variables globales de configuration
#				(à terme dans un fichier de config)
# ----------------------------------------------------------------------

	# Organisation
	# ------------
OPTIONS_FAC = ["MPS", "ICN", "SI", "CIT"] 	# Facultatives
OPTIONS_OBLIG = ["CME"]						# Obligatoires

TRIMESTRES = ["1", "2", "3"]
CLASSES = ["1", "2", "3", "4", "5", "6"]

LYCEE = "Lycée Arbez Carme"

	# Critères d'évaluation (uniquement 4 pour l'instant)
	# ---------------------------------------------------
# La liste des 4 critères, dans l'ordre dans lequel ils apparaissent dans le tableau
CRITERE1 = ["Autonomie", "Dépendant", "Interventions fréquentes", "Quelques questions", "Autonome"]
CRITERE2 = ["Implication", "Passivité", "Minimale", "Scolaire", "Proactive"]
CRITERE3 = ["Qualité du compte rendu", "Bâclé", "Minimaliste", "Quelques imprécisions", "Complet et rigoureux"]
CRITERE4 = ["Attitude", "Indisciplinée", "Dispersée", "Correcte", "Positive"]
#~ CRITERE1 = ["Autonomie", "Dépendant", "Questions fréquentes", "Quelques questions", "Autonome"]
#~ CRITERE2 = ["Implication", "Passivité", "Minimale", "Perfectible", "Investi"]
#~ CRITERE3 = ["Communication", "Bâclé", "Brouillon", "Quelques imprécisions", "Complet et rigoureux"]
#~ CRITERE4 = ["Projet", "Insuffisant", "Correct", "Bon", "Très bon"]
#~ CRITERE4 = ["Démarche d'investigation", "Inexistante", "Désorganisée", "De bonnes idées", "Structurée"]


	# Mise page de la fiche
	#----------------------
# Echelle du radar (sur la base de 3 cm de rayon)
SCALE_FIG = 1 			# Pour les cercles
SCALE_TXT = 1 			# Pour le texte des critères

# Ordre des critères sur le radar (Nord, Est, Sud et Ouest) 
CRIT_N = 2		# Ici le critère affiché au Nord sera le CRITERE2
CRIT_E = 4
CRIT_S = 3
CRIT_O = 1

# Taille des boîtes, en cm, contenant les intitulés des critères sur le radar
# Nord, Est, Sud et Ouest (en cas de coupures de mots désagréables sur le radar)
SIZE_NODE_N = 3
SIZE_NODE_E = 3
SIZE_NODE_S = 3
SIZE_NODE_O = 3

# Taille des colonnes du tableau en cm (idem en cas de coupures de mots désagréables)
SIZE_COL1 = 3.5
SIZE_COL2 = 3.5
SIZE_COL3 = 3.5
SIZE_COL4 = 3.5

# Intensité du gris dans les cases du tableau (0=Noir, 1=Blanc)
GRAY = 0.8			# Pour la qualité d'impression

	# Fichiers
	# --------
REP_TRAVAIL = "Exploration"			# Répertoire de travail
FILE_ELEVES = "ListeEleves.csv"		# Liste des élèves (pérécédé de l'année)
FILE_BN = "Appreciations.txt"		# Bloc note pour les appréciations

	# Options de compilation
	# ----------------------
CLEAN_TMP = True 		# Efface les fichiers temporaires créés à la compilation Latex
SHOW_PDF = True			# Affiche le pdf créé
SHOW_TXT = True			# Affiche le .txt des appréciations


	# Mise à jours d'autres variables globales à partir des précédentes (Ne pas modifier) :
	# -------------------------------------------------------------------------------------
OPTIONS = OPTIONS_FAC+OPTIONS_OBLIG

CRITERES = [CRITERE1, CRITERE2, CRITERE3, CRITERE4]
NBCRIT = len(CRITERES)

LENMAX_ITEM = max([len(c) for i in range(NBCRIT) for c in CRITERES[i][1:] ])

REP_HOME = os.path.expanduser("~")
DEFPATH = os.path.join(REP_HOME,REP_TRAVAIL)

#-----------------------------------------------------------------------
# 		Variables globales système d'exploitation - Commandes
#-----------------------------------------------------------------------

# CODAGE : Encodage du fichier tex
# PDFLATEX : Compilateur pdflatex
# PDFREADER : Lecteur de pdf 
# TXTEDIT : Éditeur de textes
# CMDRM : Commande pour effacer un fichier
# NULL : Trou noir pour rediriger la sortie de pdflatex
# CHAR : Caractère de retour chariot

if sys.platform.startswith('linux'):
	# Sous Linux
	CODAGE = 'utf8'
	PDFLATEX = "pdflatex --shell-escape --enable-write18 -synctex=1 -interaction=nonstopmode " 
	PDFREADER = "evince " 
	TXTEDIT = "gedit "
	CMDRM = "rm "
	NULL = "/dev/null"
	CHAR = "\n"
	
elif sys.platform.startswith('win'):
	# Sous Windows
	CODAGE = 'utf8'
	PDFLATEX = "pdflatex --shell-escape --enable-write18 -synctex=1 -interaction=nonstopmode "
	PDFREADER = REP_HOME+r"\AppData\Local\Apps\Evince-2.32.0.145\bin\evince.exe "
	TXTEDIT = "notepad "
	CMDRM = "del "
	NULL = "nul"
	CHAR = "\r\n"
	
elif sys.platform.startswith('darwin'):
	# Sous MacOS (pas fait encore)
	# Commenter le 2 lignes suivantes pour les tests sous mac
	tkMessageBox.showerror("Erreur","Système Mac non encore pris en charge")
	quit()
	
	CODAGE = 'utf8'
	PDFLATEX = "pdflatex --shell-escape --enable-write18 -synctex=1 -interaction=nonstopmode "
	PDFREADER = "evince "
	TXTEDIT = "gedit "
	CMDRM = "rm "
	NULL = "/dev/null"
	CHAR = "\n"

else : 
	# Autres systèmes
	tkMessageBox.showerror("Erreur","Système non pris en charge")
	quit()

#-----------------------------------------------------------------------
# 						Ressources texte
#-----------------------------------------------------------------------

	# Boîtes de texte
	# ---------------
TXT_HELP="""
    Raccoucis clavier :    
      - CTRL + <− : Fiche précédente    
      - CTRL + −> : Fiche suivante    
      - CTRL + F  : Compiler la Fiche en cours    
      - CTRL + T  : Compiler Toutes les fiches    
      - CTRL + A  : Générer les Appréciations    
    """

TXT_ABOUT="""
    EvalExplo, version """+__version__+"""        

    Frédéric Muller, lycée Arbez Carme    
    maths.muller@gmail.com    

    Licence : CC By-NC-SA, 2015    
    """  

	# LaTeX
	# -----
# Préambule (classe, packages,...)
PREAMBULE_TEX = r"""\documentclass[a4paper,12pt,fleqn]{article}
\usepackage["""+CODAGE+r"""]{inputenc}
\usepackage[frenchb]{babel}
\usepackage[T1]{fontenc}
\usepackage{tikz}
\usetikzlibrary{automata,positioning}
\usepackage{colortbl}
\usepackage{xcolor}
\usepackage{array}
\newcolumntype{M}[1]{>{\centering\arraybackslash}m{#1}}
\usepackage[margin=1.5cm]{geometry}
\pagestyle{empty}
\begin{document}
"""
# Nouvelle page
NP_TEX=r"\newpage"

# Fin du document tex
FIN_TEX=r"\end{document}"

#-----------------------------------------------------------------------
# 						Fonctions système
# ----------------------------------------------------------------------

# Récupérer l'année scolaire en cours
# -----------------------------------
def get_annee():
	"""Récupère l'année scolaire en cours"""
	# Récupération du mois et de l'anné en cours
	m, y = int(time.strftime("%m", time.gmtime())), int(time.strftime("%Y", time.gmtime()))
	# Avant Août prendre l'année courante, sinon prendre l'année n+1
	return y if m<8 else y+1

FILE_ELEVES = str(get_annee())+"-"+FILE_ELEVES

# Lancer la compilation latex
# ---------------------------
def exec_os(commande):
	""" Exécute une commande système"""
	#~ os.system(commande)
	subprocess.call(commande, shell=True)

def launch_compile_latex(source, path, filename):
	"""Compilation Latex"""
	# Chemin complet
	pathfile = os.path.join(path, filename)
	# Pdflatex
	exec_os(PDFLATEX+' -output-directory "'+path+'" "'+pathfile+'.tex" 1>'+NULL)
	# Nettoyage des fichiers temporaires
	if CLEAN_TMP :
		for ext in [".aux", ".log", ".synctex.gz", ".tex"] :
			exec_os(CMDRM+'"'+pathfile+ext+'"')
	# Affichage du pdf
	if SHOW_PDF :
		exec_os(PDFREADER+' "'+pathfile+'.pdf"')

def compile_tex(source, path=DEFPATH, filename="tmptex"):
	"""Lancement de la compil Latex"""
	pathfile = os.path.join(path, filename)
	# Création du fichier .tex
	f = open(pathfile+".tex","w")
	f.write(source)
	f.close()
	# Lancement du thread de compilation
	Thread(target=launch_compile_latex, args=(source,path,filename)).start()


# Sauvegarder un fichier texte
# ----------------------------

def save_txt_file(text, path=DEFPATH, filename="tmptxt"):
	if os.path.splitext(filename)[1] != ".txt" :
		filename+=".txt"
	filetxt = open(os.path.join(path, filename),"w")
	filetxt.write(text)
	filetxt.close()

# Afficher un fichier texte
# -------------------------
def launch_notepad(path, filename):
	"""Lancement de l'éditeur de textes"""
	pathfile = os.path.join(path, filename)
	exec_os(TXTEDIT+' "'+pathfile+'"')
	
def show_txt_file(path, filename) :
	# Création du Thread
	Thread(target=launch_notepad, args=(path,filename)).start()



#-----------------------------------------------------------------------
# 						Classes de structure
#-----------------------------------------------------------------------

# Classe Elève
# ------------
class Eleve():
	"""Stock les infos de chaque élève (nom, prénom,...)"""
	
	def __init__(self, nom, prenom, classe, option):
		# Infos de l'élève
		self.nom = nom
		self.prenom = prenom
		self.classe = classe
		self.nom_complet = "2nde %s - %s %s"%(classe, nom.upper(), prenom)
		self.option = option

# Classe Fiche
# ------------
class Fiche():
	"""Fiche d'évaluation d'un élève"""
	
	def __init__(self, eleve, option, trimestre):
		# Infos de l'élève et administratives
		self.eleve = eleve
				
		self.option = option
		self.trimestre = trimestre
		self.annee = get_annee()
		
		# Évaluation
		self.criteres = [-1]*len(CRITERES) # Chaque Note de 0 à 3, -1=pas fait
		self.appreciation = ""
		
		# Nom du fichier de la fiche (sans extension)
		self.filename = str(get_annee())+"-T"+self.trimestre+"-20"+self.eleve.classe+"-"+self.option+"-"+self.eleve.nom+"-"+self.eleve.prenom
		
		# Source latex de la fiche de l'élève
		self.source_tex = ""

	def test_fiche(self):
		"""Test si la fiche est terminée"""
		if -1 in self.criteres or self.appreciation == "" :
			return False
		else :
			return True

	def make_tex_eleve(self):
		"""Crée la partie du fichier source .tex de la fiche de l'élève avec
		les infos rentrées (le coeur du programme...)"""
		
		# Cadre de titre (Nom, classe, année,...)
		self.source_tex_eleve = r"""
\begin{center}
\begin{tabular}{|p{17cm}|}
\hline
\begin{center}
\LARGE{\textbf{\textsc{"""+self.eleve.nom[0].upper()+self.eleve.nom[1:].lower()+r"} "+self.eleve.prenom+r" - 2\up{nde}\ "+self.eleve.classe+r"""}}\\
\Large{\textbf{Trimestre """+self.trimestre+" - "+r"%d/%d"%(int(self.annee)-1, int(self.annee))+r"""}}\\
\ \\
\LARGE{\textbf{Enseignement d'exploration """+self.option+r"""}}\\
\end{center}\\
\hline
\end{tabular}
\end{center}

\bigskip"""

		# Création du radar
		self.source_tex_eleve+=r"""
\begin{center}
\begin{tikzpicture}[scale="""+str(SCALE_FIG)+r" ,every node/.style={scale="+str(SCALE_TXT)+r"""}, text centered]
\draw (0,0) circle(3cm);
\draw (0,0) circle(2cm);
\draw (0,0) circle(1cm);
\draw[latex-latex] (0,-3.5)--(0,3.5);
\draw[latex-latex] (-3.5,0)--(3.5,0);
\draw (0,3.5) node[above, text width="""+str(SIZE_NODE_N)+r"cm]{\textbf{"""+CRITERES[CRIT_N-1][0]+r"""}};
\coordinate (A) at (0,"""+str(self.criteres[CRIT_N-1])+r""");
\draw (3.5,0) node[right, text width="""+str(SIZE_NODE_E)+r"cm]{\textbf{"""+CRITERES[CRIT_E-1][0]+r"""}};
\coordinate (B) at ("""+str(self.criteres[CRIT_E-1])+r""",0);
\draw (0,-3.5) node[below, text width="""+str(SIZE_NODE_S)+r"cm]{\textbf{"""+CRITERES[CRIT_S-1][0]+r"""}};
\coordinate (C) at (0,-"""+str(self.criteres[CRIT_S-1])+r""");
\draw (-3.5,0) node[left, text width="""+str(SIZE_NODE_O)+r"cm]{\textbf{"""+CRITERES[CRIT_O-1][0]+r"""}};
\coordinate (D) at (-"""+str(self.criteres[CRIT_O-1])+r""",0);
\draw[very thick] (A)--(B)--(C)--(D)--(A);
\fill (A) circle(3pt);
\fill (B) circle(3pt);
\fill (C) circle(3pt);
\fill (D) circle(3pt);
\end{tikzpicture}

\bigskip
\bigskip
\bigskip"""

		# Création du Tableau
		self.source_tex_eleve+=r"""
\begin{tabular}{|M{"""+str(SIZE_COL1)+"cm}|M{"+str(SIZE_COL2)+"cm}|M{"+str(SIZE_COL3)+"cm}|M{"+str(SIZE_COL4)+r"""cm}|}
\hline
\textbf{"""+CRITERES[0][0]+r"""} & \textbf{"""+CRITERES[1][0]+r"""} & \textbf{"""+CRITERES[2][0]+r"""} & \textbf{"""+CRITERES[3][0]+r"""} \\
"""
		self.source_tex_eleve+=r"""\hline
\hline
"""
		# Remplissage du tableau (cases grisées)
		for i in range(4)[::-1]:  	# [::-1] parcours à l'envers (critères meilleurs en haut du tableau)
			for j in range(3):
				if self.criteres[j] == i : 
					self.source_tex_eleve+=r"\cellcolor[gray]{"+str(GRAY)+"}"+CRITERES[j][i+1]+"&"
				else :
					self.source_tex_eleve+=CRITERES[j][i+1]+"&"
			if self.criteres[3] == i : 
				self.source_tex_eleve+=r"\cellcolor[gray]{"+str(GRAY)+"}"+CRITERES[3][i+1]+r"\\"+r"""
\hline
"""
			else :
				self.source_tex_eleve+=CRITERES[3][i+1]+r"\\"+r"""
\hline
"""
		self.source_tex_eleve+=r"""\end{tabular}
\end{center}

\bigskip
\bigskip"""

		# Cadre appréciations
		self.source_tex_eleve+=r"""
\textbf{Appréciation générale :}

\begin{tabular}{|p{17cm}|}
\hline
\\"""
		self.source_tex_eleve+=self.appreciation.replace(CHAR,r" ")
		self.source_tex_eleve+=r"""\\
\\
\hline
\end{tabular}"""

		# Nom du lycée en bas
		self.source_tex_eleve+=r"""
\vfill
\begin{flushright}
\begin{small}
\textsc{"""+LYCEE+r"""}
\end{small}
\end{flushright}
"""

	def compile_tex(self):
		"""Compile la fiche d'un élève"""
		self.make_tex_eleve()
		# Pour avoir le source complet, on rajoute le préambule et la fin
		self.source_tex = PREAMBULE_TEX+self.source_tex_eleve+FIN_TEX
		compile_tex(self.source_tex, filename=self.filename)

# Classe Session :
#-----------------
class Session():
	"""Stock une session de travail (ensemble de fiches)"""
	
	def __init__(self, option, trimestre, classe="Toutes"):
		# Paramètres de la session
		self.option = option
		self.trimestre = trimestre
		# On peut choisir Toutes les classes
		self.classe = classe
		if self.classe == "Toutes" :
			self.classe_nom = "Toutes"
		else:
			self.classe_nom = "20"+classe
		self.annee = get_annee()
		
		self.filename = str(self.annee)+"-T"+trimestre+"-"+self.classe_nom+"-"+option
		
		# Création des fiches
		self.init_message = self.init_session()
		
		# Récupération du plus long nom (pour la gui)
		if len(self.fiches)!=0:
			self.lenmax_nom = max(len(f.eleve.nom_complet) for f in self.fiches)
		else :
			self.lenmax_nom = 20
		
	def add_fiche(self, eleve):
		"""Ajoute une fiche à la session"""
		self.fiches.append(Fiche(eleve, self.option, self.trimestre))
	
	def update_fiche(self, num, criteres, appreciation):
		"""Met à jour la fiche"""
		self.fiches[num].criteres = criteres
		self.fiches[num].appreciation = appreciation
	
	def test_fiches(self):
		"""Test s'il manque des fiches
		- Affiche un avertissement s'il reste des fiches non terminées
		- Retourne False si aucune fiche n'a été faite, sinon True"""
		# On teste d'abord si aucune fiche n'est terminée pour avorter l'opération en cours
		empty = True
		for f in self.fiches :
			if f.test_fiche() :
				empty = False
		if empty :
			tkMessageBox.showerror("Erreur", "Aucune fiche terminée")
			return False
			
		# On teste s'il manque au moins une fiche pour afficher un avertissement
		for f in self.fiches :
			if not f.test_fiche() :
				tkMessageBox.showwarning("Erreur", "Il reste des fiches non terminées")
				break
		return True
	
	def read_liste_eleves(self, file_eleves=FILE_ELEVES):
		"""Lit le fichier de la liste des élèves"""
		# Lignes du csv : Nom,Prénom,Classe,Option
		self.liste_eleves = []
		with open(os.path.join(DEFPATH, file_eleves), 'r') as csvfile:
			filecsv = csv.reader(csvfile, delimiter=",")
			for row in filecsv :
				# On ajoute les élèves pour chaque ligne du .csv
				if self.classe == "Toutes" or self.classe == row[2]:
					if row[3] == self.option or self.option in OPTIONS_OBLIG :
						self.liste_eleves.append(Eleve(row[0], row[1], row[2], row[3]))
	
	def cree_fiches_vierges(self):
		self.fiches = []
		self.read_liste_eleves()
		for e in self.liste_eleves :
			self.add_fiche(e)
	
	def save_session(self, filename=""):
		"""Sauvegarde la session de travail"""
		# Lignes du .csv : Nom,Prénom,Classe,Option,Année,Trimestre,Note1,Note2,Note3,Note4,Appréciation
		if not filename :
			filename = self.filename+".csv"
		with open(os.path.join(DEFPATH, filename), 'w') as csvfile:
			filecsv = csv.writer(csvfile, delimiter="#")
			for f in self.fiches :
				filecsv.writerow([f.eleve.nom, f.eleve.prenom, f.eleve.classe, f.option, self.annee, self.trimestre, 
					str(f.criteres[0]), str(f.criteres[1]), str(f.criteres[2]), str(f.criteres[3]), f.appreciation])
	
	def load_session(self, filename=""):
		"""Charge la session de travail"""
		# Lignes du .csv : Nom,Prénom,Classe,Option,Année,Trimestre,Note1,Note2,Note3,Note4,Appréciation
		if not filename :
			filename = self.filename+".csv"
		self.fiches = []
		with open(os.path.join(DEFPATH, filename), 'r') as csvfile:
			filecsv = csv.reader(csvfile, delimiter="#")
			for row in filecsv :
				# Pour chaque ligne du .csv on crée la fiche
				eleve = Eleve(row[0], row[1], row[2], row[3])
				self.add_fiche(eleve)
				self.fiches[-1].annee = row[4]
				self.fiches[-1].trimestre = row[5]
				self.fiches[-1].criteres = [int(row[6]), int(row[7]), int(row[8]), int(row[9])]
				self.fiches[-1].appreciation = row[10]
				
	def init_session(self):
		"""Initialise la liste des fiches"""
		if os.path.exists(os.path.join(DEFPATH, self.filename+".csv")):
			self.load_session()
			message = "Session chargée avec succès"
		else :
			self.cree_fiches_vierges()
			message = "Nouvelle session crée"
		return message 
		
	def compile_tex_all(self):
		"""Compile toutes les fiches de la session"""
		# Création du source tex avec toutes les fiches terminées et changement de pages entre les fiches 
		source = PREAMBULE_TEX
		for f in self.fiches[:-1] :
			if f.test_fiche() :
				f.make_tex_eleve()
				source+=f.source_tex_eleve
				source+=CHAR+NP_TEX+CHAR # Changement de page
		if self.fiches[-1].test_fiche():
			self.fiches[-1].make_tex_eleve()
			source+=self.fiches[-1].source_tex_eleve
		source+=CHAR+FIN_TEX
		# Finalement on compile le tout
		compile_tex(source, filename=self.filename)

	def generate_apprec(self):
		"""Génère le fichier txt des appréciations"""
		# Génration du .txt des appréciations
		text = "Appréciations en %s pour le trimestre %s"%(self.option, self.trimestre)+"""
---------------------------------------------------------------
"""
		for f in self.fiches :
			if f.test_fiche():
				text+="2nde%s - %s %s"%(f.eleve.classe, f.eleve.nom, f.eleve.prenom)+CHAR
				text+=CHAR
				text+=f.appreciation
				text+="""
---------------------------------------------------------------
"""
		save_txt_file(text, path=DEFPATH, filename=self.filename+"-Appreciations")


#-----------------------------------------------------------------------
# 						Interface graphique
#-----------------------------------------------------------------------

# Fenêtre des paramètres
# ----------------------
class Pref(Frame):
	"""Fenêtre des paramètres"""
	
	def __init__(self,parent):
		
		Frame.__init__(self, parent)
		parent.title("Paramètres")
		parent.resizable(False, False)
		self.pack()
		
		self.lb1 = Label(self, text="Année : %d"%get_annee())
		self.lb1.grid(row=0, column=0, sticky="W", padx=5, pady=5)
		
		self.lb2 = Label(self, text="Enseignement : ")
		self.lb2.grid(row=1, column=0, sticky="W", padx=5, pady=5)
		
		self.option = StringVar()
		self.cb_option = Combobox(self, textvar=self.option, state="readonly")
		self.cb_option['value'] = OPTIONS
		self.cb_option.grid(row=1, column=1,sticky="W", padx=5, pady=5)
		self.option.set(OPTIONS[0])
		
		self.lb3 = Label(self, text="Classe de 2nde : ")
		self.lb3.grid(row=2, column=0, sticky="W", padx=5, pady=5)
		
		self.classe = StringVar()
		self.cb_classe = Combobox(self, textvar=self.classe, state="readonly")
		self.cb_classe['value'] = ["Toutes"]+CLASSES
		self.cb_classe.grid(row=2, column=1, sticky="W", padx=5, pady=5)
		self.classe.set("Toutes")
		 
		self.lb4 = Label(self, text="Trimestre :")
		self.lb4.grid(row=3, column=0, sticky="W", padx=5, pady=5)
		
		self.trimestre = StringVar()
		self.cb_trimestre = Combobox(self, textvar=self.trimestre, state="readonly")
		self.cb_trimestre['value'] = ["1", "2", "3"]
		self.cb_trimestre.grid(row=3, column=1, sticky="W", padx=5, pady=5)
		self.trimestre.set("1")
		
		self.bt_ok = Button(self, text="Terminé", command=self.termine)
		self.bt_ok.grid(row=4, column=0, columnspan=2, padx=5, pady=10)
	
	def termine(self):
		"""Valide les paramètres"""
		if self.trimestre.get() != "" and  self.option.get() != "" :
			# Création de la session avec les infos
			self.session = Session(self.option.get(), self.trimestre.get(), self.classe.get())
			self.quit()

# Fenêtre de remplissage des fiches
# ---------------------------------
class App(Frame) :
	"""Fenêtre principale"""
	
	def __init__(self,parent, session):
		
		# Initialisation session
		# ----------------------
		self.session = session
		self.index = 0	# Numéro de la fiche en cours
		
		if len(self.session.fiches) == 0:
			tkMessageBox.showerror("Erreur", "Aucun élève avec ces critères dans la base")
			quit()
		
		lenmax = max(LENMAX_ITEM, self.session.lenmax_nom) # Plus grande longueur de texte à afficher dans la 2e colonne
		
		# Initialisation fenêtre graphique
		# --------------------------------
		self.parent = parent
		Frame.__init__(self, self.parent)
		self.pack()
		
		self.parent.title(self.session.filename)
		self.parent.protocol("WM_DELETE_WINDOW", self.quit)
		self.parent.resizable(False, False)
		# Binding des raccourcis claviers
		self.parent.bind("<Control-Right>", self.suiv)
		self.parent.bind("<Control-Left>", self.prec)
		self.parent.bind("<Control-f>", self.compile_tex)
		self.parent.bind("<Control-F>", self.compile_tex)
		self.parent.bind("<Control-t>", self.compile_tex_all)
		self.parent.bind("<Control-T>", self.compile_tex_all)
		self.parent.bind("<Control-a>", self.generate_apprec)
		self.parent.bind("<Control-A>", self.generate_apprec)
		
		# Barre de menu
		# -------------
		self.menubar = Menu(self)
		self.filemenu = Menu(self.menubar, tearoff=0)
		self.filemenu.add_command(label="Générer la fiche élève", command=self.compile_tex)
		self.filemenu.add_command(label="Générer toutes les fiches élève", command=self.compile_tex_all)
		self.filemenu.add_command(label="Générer les appréciations", command=self.generate_apprec)
		self.filemenu.add_separator()
		self.filemenu.add_command(label="Quitter", command=self.quit)
		
		self.aboutmenu = Menu(self.menubar, tearoff=0)
		self.aboutmenu.add_command(label="Raccourcis clavier", command=self.help)
		self.aboutmenu.add_command(label="À propos", command=self.about)
		
		
		self.menubar.add_cascade(label="Fichier", menu=self.filemenu)
		self.menubar.add_cascade(label="Aide", menu=self.aboutmenu)
		self.parent.config(menu=self.menubar)
		
		
		# Frame principale
		self.frame0=Frame(self)
		
		# Frame de rentrée des évaluations
		# --------------------------------
		self.frame1 = Frame(self.frame0)
		
		self.nom = StringVar()
		self.lb_nom = Label(self.frame1, textvariable=self.nom, width=lenmax+5, font=('bold'))
		self.update_nom()
		self.lb_nom.grid(row=0, column=1, padx=5, pady=5,sticky="W")
		
		self.bt_prec = Button(self.frame1, text="Précédent", command=self.prec)
		self.bt_prec.grid(row=0, column=0, padx=5, pady=5)
		
		self.bt_suiv = Button(self.frame1, text="Suivant", command=self.suiv)
		self.bt_suiv.grid(row=0, column=2, padx=5, pady=5)
		
		# Création des critères
		self.lb_crit = []
		self.cb_crit = []
		self.crit = []
		for i in range(NBCRIT) :
			self.lb_crit.append(Label(self.frame1, text=CRITERES[i][0]+" : "))
			self.lb_crit[-1].grid(row=i+1, column=0, padx=5, pady=5, sticky="W")
			
			self.crit.append(StringVar())
			self.cb_crit.append(Combobox(self.frame1, textvariable=self.crit[-1], state="readonly", width=lenmax+5))
			self.cb_crit[-1]['value'] = CRITERES[i][:0:-1]
			self.cb_crit[-1].grid(row=i+1, column=1, padx=5, pady=5, sticky="W")
		
		self.lb_app = Label(self.frame1, text="Appréciation : ")
		self.lb_app.grid(row=NBCRIT+1, column=0, padx=5, pady=5, sticky="W")
		
		self.txt_app = Text(self.frame1,height=4, width=lenmax+30, wrap=WORD)
		self.txt_app.grid(row=NBCRIT+1, column=1, padx=5, pady=5, columnspan=2, sticky="W")
		
		# Boutons en bas
		self.bt_pdf = Button(self.frame1, text="Générer la fiche", command=self.compile_tex)
		self.bt_pdf.grid(row=NBCRIT+2, column=0, padx=5, pady=10)
		
		self.bt_allpdf = Button(self.frame1, text="Générer toutes les fiches", command=self.compile_tex_all)
		self.bt_allpdf.grid(row=NBCRIT+2, column=1, padx=5, pady=10)
		
		self.bt_app = Button(self.frame1, text="Appréciations", command=self.generate_apprec)
		self.bt_app.grid(row=NBCRIT+2, column=2, padx=5, pady=10)
		
		self.frame1.pack(side=LEFT)

		Frame(self.frame0, width=20).pack(side=LEFT)
		# Bloc note à droite
		# ------------------
		self.frame2 = Frame(self.frame0)
		
		Label(self.frame2, text="Bloc note pour copier-coller vos appréciations :").grid(row=0, column=0, padx=5, pady=5)
		
		self.txt_bn = Text(self.frame2, width=40, height=16, wrap=WORD)
		self.txt_bn.grid(row=1, column=0)
		
		self.frame2.pack()
		
		self.frame0.pack(side=TOP)
		
		# Satus Bar
		# ---------
		self.status = StringVar()
		self.lb_status = Label(self, relief=SUNKEN, anchor=W, textvar=self.status, borderwidth=1)
		self.lb_status.pack(fill=X)
		
		# Lancement de la session
		# -----------------------
		self.load_session()
	
	# Navigation entre les fiches
	# ---------------------------
	def prec(self, event=None):
		"""Fiche précédente"""
		self.update_fiche()
		self.update_gui()
		if self.index > 0 :
			self.index-=1
		else :
			self.index = len(self.session.fiches)-1
		self.update_nom()
		self.update_gui()
		
	def suiv(self,event=None):
		"""Fiche suivante"""
		self.update_fiche()
		self.update_gui()
		if self.index < len(self.session.fiches)-1 :
			self.index+=1
		else : 
			self.index = 0
		self.update_nom()
		self.update_gui()
	
	# Actualisations
	# --------------
	def update_nom(self):
		"""Met à jour le nom de l'élève"""
		eleve = self.session.fiches[self.index].eleve
		self.nom.set(eleve.nom_complet)
		
	def update_gui(self):
		"""Met à jour l'interface graphique avec les données de la fiche"""
		# Mise à jour ces Combobox des critères
		for i in range(NBCRIT):
			if self.session.fiches[self.index].criteres[i] != -1:
				self.cb_crit[i].set(CRITERES[i][self.session.fiches[self.index].criteres[i]+1])
			else :
				self.cb_crit[i].set("")
		# Mise à jour de l'appréciation
		self.txt_app.delete(1.0, END)
		app = self.session.fiches[self.index].appreciation
		self.txt_app.insert(END, self.session.fiches[self.index].appreciation)
		# Mise à jour du nom
		self.update_nom()
		
	def update_fiche(self):
		"""Met à jour la fiche avec les infos de l'interface graphique"""
		# Récupération des notes
		crit_gui = [c.get() for c in self.crit]
		crit = []
		for k in range(NBCRIT) :
			found = False
			for j in range(len(CRITERES[k][1:])):
				if crit_gui[k] == CRITERES[k][j+1].decode('utf-8') :
					crit.append(j)
					found=True
			if not found :
				crit.append(-1)
		# Récupération de l'appréciation
		appr = self.txt_app.get(1.0, END)[:-1]
		appr = appr.replace(CHAR,r" ").encode('utf-8')
		# Mise à jour de la fiche
		self.session.update_fiche(self.index, crit, appr)

	# Création des documents
	# ----------------------
	def compile_tex(self, event=""):
		"""Compile la fiche en cours"""
		self.update_fiche()
		f = self.session.fiches[self.index]
		if f.test_fiche():
			f.compile_tex()
			self.status.set("Fiche sauvegardée dans : %s"%os.path.join(DEFPATH, f.filename+".pdf"))
		else :
			tkMessageBox.showerror("Erreur","Fiche non terminée")

	def compile_tex_all(self, event=""):
		"""Compile toutes les fiches de la session"""
		self.update_fiche()
		# Si aucune fiche n'est faite, annuler
		if not self.session.test_fiches() :
			return
		self.session.compile_tex_all()
		self.status.set("Fiches sauvegardées dans : %s"%os.path.join(DEFPATH, self.session.filename+".pdf"))

	def generate_apprec(self, event=""):
		"""Génère le fichier txt des appréciations"""
		self.update_fiche()
		# Si aucune fiche n'est faite, annuler
		if not self.session.test_fiches() :
			return

		self.session.generate_apprec()
		self.status.set("Appréciations sauvegardées dans : %s"%os.path.join(DEFPATH, self.session.filename+"-Appreciations.txt"))

		if SHOW_TXT:
			show_txt_file(DEFPATH, self.session.filename+"-Appreciations.txt")
	
	# Fenêtres d'aide
	# ---------------
	def about(self):
		"""Fenêtre À propos"""
		about_win = Toplevel(self)
		about_win.title("À propos")
		Label(about_win, text=TXT_ABOUT, background="white").pack()
		Button(about_win, text="Fermer", command=about_win.destroy).pack()
		
	def help(self):
		"""Fenêtre d'aide"""
		help_win = Toplevel(self)
		help_win.title("Aide")
		Label(help_win, text=TXT_HELP, background="white").pack()
		Button(help_win, text="Fermer", command=help_win.destroy).pack()
	
	
	# Sauvegarde et chargement de la session
	# --------------------------------------
	def save_session(self):
		"""Sauve la session"""
		self.update_fiche()
		self.update_gui()
		self.session.save_session()
		self.save_bn()
		tkMessageBox.showinfo("Info","Session sauvegardée dans :\n%s"%self.session.filename+".csv")

	def load_session(self):
		"""Charge la session"""
		# Chargement du bloc note
		if os.path.exists(os.path.join(DEFPATH, FILE_BN)):
			f = open(os.path.join(DEFPATH, FILE_BN),'r')
			for line in f.readlines() :
				self.txt_bn.insert(END, line)
			f.close()
		# Chargement de la session
		self.status.set(self.session.init_message)
		self.update_gui()
	
	def save_bn(self):
		"""Sauvegarde le bloc note"""
		save_txt_file(self.txt_bn.get(1.0, END)[:-1], path=DEFPATH, filename=FILE_BN)
	
	def quit(self):
		"""Sauvegarder et quitter l'appli"""
		# On sauve la session
		self.save_session()
		# Fermeture de tous les threads en cours
		for thread in enumerate():
			if thread.isAlive():
				try:
					thread._Thread__stop()
				except:
					print("Erreur")
		# On ferme la fenêtre
		self.parent.quit()


#-----------------------------------------------------------------------
# 								Main
#-----------------------------------------------------------------------

def main():
	"""Programme principal"""
	root = Tk()
	# Lancement de la fenêtre des paramètres
	pref = Pref(root)
	root.mainloop()
	# Récupération des paramètres et création de la session
	try :
		session = pref.session
	except:
		quit()
	pref.destroy()
	# Lancement de l'appli principale
	app = App(root, pref.session)
	root.mainloop()

if __name__ == '__main__':
	main()
