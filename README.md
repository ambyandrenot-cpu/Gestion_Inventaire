Voici un **README court et clair**, parfait pour ton dépôt GitHub.
Il explique brièvement le projet, son but, les technologies, et le rôle détaillé de chaque membre 👇

---

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
* **Git & GitHub** pour la collaboration

---

## 👥 Répartition des rôles

| Membre       | Rôle principal                           | Détails des tâches                                                                                                                                                     |
| ------------ | ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Membre 1** | Développeur CRUD (Ajout)                 | Implémente la fonction `add_materiel()` et gère l’insertion des nouveaux équipements dans la base. Travaille sur la validation des champs et la cohérence des données. |
| **Membre 2** | Développeur CRUD (Modification)          | Crée la fonction `update_materiel()` pour modifier les informations d’un matériel existant. Vérifie les doublons et la fiabilité des mises à jour.                     |
| **Membre 3** | Développeur CRUD (Suppression)           | Implémente `delete_materiel()` avec confirmation avant suppression. Gère les erreurs liées aux identifiants inexistants.                                               |
| **Membre 4** | Développeur CRUD (Affichage / Recherche) | Crée la fonction `list_materiel()` et les filtres de recherche. Affiche les matériels selon plusieurs critères (type, état, disponibilité…).                           |
| **Membre 5** | Gestion base de données                  | Crée et maintient la base **SQLite** (`inventaire.db`). Définit les tables (`materiel`, `utilisateur`). Assure l’intégrité et les tests de connexion.                  |
| **Membre 6** | Interface utilisateur (UI)               | Conçoit l’interface avec, relie les fonctions CRUD à l’UI, ajoute les graphiques et le tableau de bord pour les statistiques (facultatif).                            |

---


## 📅 Durée du projet

🗓️ 10 jours intensifs (piscine d’intégration Python)
Objectif : apprendre Python, collaborer efficacement et livrer une application fonctionnelle.

