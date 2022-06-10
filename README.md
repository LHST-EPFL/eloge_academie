# La construction de la grandeur savante XVIIIème-XIXème siècle

Ce git contient tout le code qui a été utilisé pour le projet sur la construction de la grandeur savante au dix-huitième et dix-neuvième siècle.

La hiérarchie de ce projet se divise en deux. Le dossier Code et le dossier Data.

## Code

Ce dossier comprends 5 dossiers :

### Comparison

Ce dossier contient le code qui a servi à la comparaison pré et post Révolution. Dedans on retrouve les fichiers :

* Adding_eulogies : notebook servant à rajouter les éloges au fur et à mesure au dataframe principal
* Comparison : notebook contenant la comparaison des éloges avant et après la Révolution
* adverbs_eda : script python qui contient la méthode servant à sortir les phrases les plus représentatives de chaque adverbe
* eda : script python contenant les différentes méthodes servant à l'eda
* percent : script python contenant les méthodes permettant de diviser et de plotter les éloges par 10%
* pre_process : script python contenant les différentes méthodes servant au pre_processing des éloges


### Condorcet

Ce dossier contient le code qui a servi à la phase exploratoire du projet. On y retrouve les fichiers suivants :

* Condorcet : notebook contenant une eda préliminaire sur le corpus de Condorcet
* Condorcet_Advanced : notebook contenant le topic modeling effectué sur Condorcet
* Mairan : notebook contenant quelques analyses sur le corpus de Mairan
* Stylométrie : notebook contenant une analyse stylométrique de comparaison entre Mairan et Condorcet

Les scripts python dans ce dossier sont les mêmes que dans le dossier Comparison et ont été recopiés dans ce fichier pour faciliter leur import


### Dataframe

Ce dossier contient les notebooks qui ont permis la création du DataFrame contenant les éloges, les fichiers suivants y sont présents :

* Checking : ce notebook permet de vérifier que tous les éloges y sont bien présents
* Parsing : ce notebook a créé et ajouté certaines éloges à un premier dataframe
* Sec_Perpetuel : ce notebook contient la création du dataframe sur les secrétaires perpétuels de l'Académie
* Update_DF : ce notebook fait l'ajout des éloges de Fontenelle au dataframe



### EDA

Ce dossier ne contient qu'un seul notebook qui fait une analyse préliminaire sur tout le dataframe

### TreeTagger

Ce dossier est récupéré directement du site de TreeTagger et recopié ici pour pouvoir faire du Part-Of-Speech dans les éloges



## Data

Ce dossier contient toutes les données qui ont servies ou été créées dans ce projet.

### Dataframes

Ce dossier contient tous les dataframes intermédiaires ainsi que ces 3 dataframes :

* all_eul.csv : ce csv contient tous le éloges
* eulogies.csv : ce csv contient les éloges ayant servis à la comparaison avant et après la Révolution
* sec_perp.csv : ce csv contient les données sur les secrétaires


### Txt

Ce dossier contient tous les txt à l'origine du dataframe contenant les éloges

### POS-tags.csv

C'est un dataframe contenant l'équivalence entre les tags de TreeTagger et la nature des mots


### Éloges 19e s.xlsx

C'est un fichier contenant une liste d'éloges publiés au XIXème siècle pour vérifier s'ils sont présents dans le dataframe


### Results

C'est un fichier qui contient des résultats créés suite à ce projet
