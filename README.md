# 🖥️ Projet Python – Gestion d’inventaire de matériels informatiques

## 🎯 Objectif

Ce projet consiste à créer une application en **Python** pour la **gestion d’un inventaire de matériels informatiques** (ordinateurs, périphériques, équipements…).
Les fonctionnalités principales incluent :

* Ajout, modification, suppression et affichage des matériels (CRUD)
* Stockage dans une base **SQLite**

---

## 🧱 Technologies utilisées

* **Python 3**
* **SQLite3** pour la base de données locale
* **Django** pour le framework web

---

## 👥 Répartition des rôles

| Membre       | Rôle principal                           | Détails des tâches                                                                                                                                                     |
| ------------ | ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Jonathan** | Gestion base de données                  | Crée et maintient la base **SQLite** (`inventaire.db`). Définit les tables (`materiel`, `utilisateur`). Assure l’intégrité et les tests de connexion. Gérer la base SQLite et créer les tables en suivant les étapes Django ORM , sans écrire de manuel SQL                 |
| **Andrenot** | Développeur CRUD (Ajout)                 | Implémente la fonction `add_materiel()` et gère l’insertion des nouveaux équipements dans la base. Travaille sur la validation des champs et la cohérence des données. |
| **Naftaly**  | Développeur CRUD (Modification)          | Crée la fonction `update_materiel()` pour modifier les informations d’un matériel existant. Vérifie les doublons et la fiabilité des mises à jour.                     |
| **Tendry**   | Développeur CRUD (Suppression)           | Implémente `delete_materiel()` avec confirmation avant suppression. Gère les erreurs liées aux identifiants inexistants.                                               |
| **Najoro**   | Développeur CRUD (Affichage / Recherche) | Crée la fonction `list_materiel()` et les filtres de recherche. Affiche les matériels selon plusieurs critères (type, état, disponibilité…).                           |
| **Joice**    | Interface utilisateur (UI)               | Conçoit l’interface avec, relie les fonctions CRUD à l’UI, ajoute les graphiques et le tableau de bord pour les statistiques (facultatif).                             |

---

## 🛠️ Instructions pour chaque membre

Pour que tout le monde travaille sur le même projet correctement :

### 1️⃣ Cloner le projet depuis GitHub

```bash
git clone git@github.com:ambyandrenot-cpu/Gestion_Inventaire.git
cd Gestion_Inventaire
```

### 2️⃣ Créer et activer un environnement virtuel (venv)

Chaque membre **crée son propre venv** sur sa machine :

```bash
python3 -m venv venv        # crée le venv
venv\Scripts\activate       # Windows
```

### 3️⃣ Installer les dépendances

```bash
pip install --upgrade pip
pip install django
```

> Tous les packages nécessaires doivent ensuite être ajoutés à `requirements.txt` pour que tout le monde ait les mêmes versions :

```bash
pip freeze > requirements.txt
```

Puis les autres membres peuvent installer avec :

```bash
pip install -r requirements.txt
```

### 4️⃣ Créer le projet Django (si ce n’est pas déjà fait)

```bash
django-admin startproject inventaire_informatique
cd inventaire_informatique
python manage.py startapp inventory_app
```

> Si le projet est déjà sur GitHub, **cloner et activer le venv suffit**, le projet est prêt.

### 5️⃣ Initialiser la base SQLite

```bash
python manage.py migrate
```

* Crée le fichier `db.sqlite3` automatiquement.
* Jonathan pourra gérer les migrations et vérifier l’intégrité des tables.

### 6️⃣ Lancer le serveur de développement

```bash
python manage.py runserver
```

* Vérifier que le serveur fonctionne : ouvrir `http://127.0.0.1:8000/` dans le navigateur.
* Chaque membre peut maintenant tester ses fonctionnalités CRUD.

### 7️⃣ Bonnes pratiques Git

* Ne pas pousser le venv sur GitHub (`.gitignore` inclus).
* Faire des commits **clairs et fréquents** :

```bash
git add .
git commit -m "feat: ajout de la fonction add_materiel" (exemple)
git push origin main
```

* Git fetch et Git Pull régulièrement pour récupérer les changements des autres.

---

## 📅 Durée du projet

🗓️ 10 jours intensifs (piscine d’intégration Python)
Objectif : apprendre Python, collaborer efficacement et livrer une application fonctionnelle.

---

Voici une version claire et bien structurée à mettre dans ton **README.md**, que toute l’équipe pourra comprendre 👇

---


## 🚀 Versions du projet “Gestion d’Inventaire”

### **v1 – Version initiale (CRUD de base + affichage global)**

Cette première version met en place toutes les fonctionnalités essentielles :

* Création, lecture, modification et suppression (CRUD) des matériels.
* Affichage de la **liste complète des matériels** dans le tableau principal.
* Affichage du **nombre total de matériels** en haut de la page.

> Objectif : Avoir une base stable et fonctionnelle du projet.

---

### **v2 – Gestion des emprunts et disponibilité**

Dans cette version, on améliore la visibilité et la gestion des stocks :

* Ajout de **deux nouvelles colonnes** dans l’interface :

  * *Matériels empruntés*
  * *Matériels disponibles*
* Ajout d’un **bouton “Emprunter”** à côté de chaque matériel pour marquer un emprunt.
* Mise à jour **automatique** du nombre de matériels disponibles dès qu’un emprunt est effectué.

> Objectif : Simuler une gestion réelle des emprunts et des disponibilités.

---

### **v3 – Ajustement dynamique des quantités**

Amélioration de la logique d’édition :

* Possibilité de **modifier le nombre total de matériels et le nombre de disponibles** directement depuis le formulaire de modification.
* Dans la version précédente (v2), seul le *nombre total* était modifiable.

> Objectif : Permettre une mise à jour cohérente des données lors de changements physiques du stock.

---

### **v4 – Ajout des filtres côté backend**

Mise en place d’un système de filtres pour améliorer la recherche et le tri des matériels :

* Implémentation de **filtres côté serveur (backend)** pour filtrer les matériels par type, état, disponibilité, etc.
* Affichage des options de filtre sur la page principale pour l’utilisateur.

> Objectif : Faciliter la navigation et la gestion dans de grands inventaires.

---
