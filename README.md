# Mini Projet  
## Ghost in the Browser : Automatisation et envoi de message sur Instagram

---

## Description du projet

Ce projet est réalisé dans le cadre du **Mini Projet 4 (P4-C1 : Automatisation après authentification)**.  
Il illustre le concept de **Ghost in the Browser** : un programme automatise des actions Web après authentification
sans exploiter de vulnérabilités.

Le script développé se connecte à **Instagram** avec un compte utilisateur,  
puis accède à la messagerie privée pour **envoyer automatiquement un message** à un contact ou une conversation.

---

## Objectif pédagogique

- Démontrer comment piloter un navigateur Web authentifié
- Maintenir l’état connecté de l’utilisateur
- Automatiser l’envoi d’un message sur Instagram
- Simuler un comportement humain pour éviter la détection
- Illustrer le concept de Ghost in the Browser : le navigateur devient un relais d’identité légitime

---

## Concept : Ghost in the Browser

- Le navigateur est contrôlé par un programme après authentification
- L’utilisateur est légitime
- Les actions automatisées (ici, l’envoi de message) sont perçues comme normales par Instagram
- Aucune faille n’est exploitée

---

## Technologies utilisées

- Python
- Playwright
- Chromium / Google Chrome
- Automatisation du navigateur
- JavaScript (injection de scripts anti-détection)

---

## Fonctionnalités du script

- Connexion automatique à Instagram avec login et mot de passe
- Gestion des cookies et popups (consentement, notifications)
- Navigation vers la messagerie privée
- Ouverture d’une conversation existante ou sélection manuelle
- Envoi automatique d’un message prédéfini
- Simulation humaine :
  - Délais aléatoires
  - Frappe progressive
  - Mouvements naturels de souris
- Masquage des indicateurs d’automatisation (`navigator.webdriver`, plugins, permissions)

---

## Exécution du projet

### Prérequis
- Python 3.x
- Google Chrome installé

### Lancement
```bash
python main.py
