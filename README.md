 ----------------------------------------------------------------------
				EvalExplo

 		Programme de création d'une fiche d'évaluation 
 		pour les enseignements d'exploration en 2nde

-----------------------------------------------------------------------

 Frédéric Muller (Lycée Arbez Carme, Bellignat)

 maths.muller@gmail.com

 Projet démarré le 03/09/2015
 Dernière maj : 12/10/2015

 Licence CC BY-NC-SA

 N'hésitez pas à me signaler par mail tout bug ou amélioration possible ;-)

-----------------------------------------------------------------------
				Documentation
-----------------------------------------------------------------------

 Installation sous win 7 :
 -------------------------
 1) Détecter sa version de windows (32 bit ou 64 bit).

 2) Installer Python 2.7 :
		https://www.python.org/downloads/release/python-2710/

	Important : cocher "Ajouter python.exe au path" pendant l'install

 3) Installer MikTex (Basic Installer qui fait 180 Mo) :
		http://miktex.org/download

	Important : Sous Win7, lancer l'installeur en mode de compatibilité Windows Vista

 4) Installer les paquets Latex suivant avec MikTek Package Manager (Admin) :
	- babel-french
	- pgf
	- ms
	- xcolor
	- colortbl
	- mptopdf

 5) Installer Evince :
		https://wiki.gnome.org/Apps/Evince/Downloads

 6) Copier ce fichier (EvalExplo.pyw) et ListeEleve.csv dans le 
	répertoire "Exploration", créé dans votre dossier personnel :
		Par ex C:\\Users\Toto\Exploration

 7) Double-cliquer sur EvalExplo.pyw pour le lancer et essayer de créer
	une fiche pour tester si tout va bien.

 Utilisation :
 -------------
 - Au lancement, choir son enseignement, la classe pour laquelle vous
 	voulez faire les fiches (ça peut être "Toutes") ainsi que le trimestre.

 - Remplissez vos fiches, vous pouvez changer d'élève avec CTRL + Flèches

 - Votre session est automatiquement sauvegardée quand vous quitez
	et rechargée au lancement, dans le dossier "Exploration".
	Le fichier de sauvegarde a pour schéma :
			Année-Trimestre-Classe-Option.csv
	Vous pouvez effacer (ou renommer) ce fichier pour reprendre à zéro.
	Vous pouvez également vous transmettre ce fichier pour travailler à plusieurs.

 - Vous pouvez créer chaque fiche individuellement, ou créer d'un coup 
	toutes les fiches de votre session. Les pdf générés sont stockés
	dans votre dossier "Exploration"

 - Vous pouvez générer un fichier texte avec toutes vos appréciations
	pour les copier-coller dans Pronote.

 - Il y a un bloc note à droite pour copier-coller vos appréciations ou
	prendre des notes. Il est sauvegardé dans "Appréciations.txt".

 Aspects techniques :
 --------------------
 - Le fichier ListeEleve.csv contient sur chaque ligne les infos des 
	élèves. Chaque ligne est sous le modèle :
		Nom,Prénom,Classe(juste le numéro),Option
	Par exemple :
		Durant,Pierre,3,MPS

	Un .csv est un fichier tableur au format texte. Chaque ligne de ce
	fichier correspond à une ligne du tableau. 
	Pour ListeEleves.csv le séparateur est la virgule : ,
	Vous pouvez le générer avec un tableur en choisissant le format CSV
	au moment de la sauvegarde.

 - La session est sauvegardée dans un fichier .csv dont le séparateur est 
	Chaque ligne est sous le modèle :
		NomPrénomClasseOptionAnnéeTrimestreNote1Note2Note3Note4Appréciation
	(Note va de 0 à 3)
	Vous pouvez donc éditer votre session au tableur

 - Vous pouvez modifier les critères et les items en changeant les variables 
	CRITERE1, CRITERE2, CRITERE3 et CRITERE4 ci-dessous.
	Le 1er terme de la liste est le nom du critère et les 4 suivants 
	sont les items classés du plus faible au plus fort

 - Vous pouvez également changer les différentes variables globales 
	pour adapter à vos besoin (CLASSE, OPTIONS), ainsi que la mise en
	page de la fiche (voir descriptions).
