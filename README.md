# GIA — Nanterre

**Formation Actemium — 10, 12 et 13 novembre 2026 — Redha Moulla**

Vous trouverez ici le support de cours, les exercices et les données pour reprendre les travaux pratiques de la formation.

## Ressources

| Ressource | Accès |
| --- | --- |
| Support de cours de Nanterre | [Ouvrir le PDF](GIA_Actemium_Nanterre_10_12_13_novembre_2026.pdf) |
| TP Prompting | [Lire le notebook](TP_Prompting.ipynb) · [Ouvrir dans Colab](https://colab.research.google.com/github/RMoulla/GIA_Nanterre/blob/main/TP_Prompting.ipynb) |
| Skill : du besoin aux spécifications | [SKILL.md](SKILL.md) |
| Audit de user stories avec n8n | [Workflow à importer](Audit_User_Story.json) |
| TP RAG — correction | [Lire le notebook](TP_RAG_Correction.ipynb) · [Ouvrir dans Colab](https://colab.research.google.com/github/RMoulla/GIA_Nanterre/blob/main/TP_RAG_Correction.ipynb) |
| TP Agents — assistant e-commerce avec MCP | [Lire le notebook](Copie_de_TP_Agent_LLM.ipynb) · [Ouvrir dans Colab](https://colab.research.google.com/github/RMoulla/GIA_Nanterre/blob/main/Copie_de_TP_Agent_LLM.ipynb) |
| Données immobilières | [selogerdata.csv](selogerdata.csv) |
| Données de désabonnement client | [customer_churn.csv](customer_churn.csv) |
| Catalogue du TP Agents | [products.csv](products.csv) |

## Télécharger les fichiers et préparer Colab

Ouvrez le fichier souhaité, puis cliquez sur **Download raw file** dans GitHub. Conservez son nom et son extension, sauf pour le PDF du TP RAG, à renommer comme indiqué ci-dessous.

Pour les notebooks, ouvrez le lien Colab, choisissez **Fichier → Enregistrer une copie dans Drive**, puis connectez-vous à un environnement **Python 3 avec CPU**. Aucun GPU n’est nécessaire. Exécutez les cellules de haut en bas avec **Maj + Entrée**.

Pour les TP RAG et Agents, ajoutez `OPENAI_API_KEY` dans les **Secrets** de Colab et autorisez le notebook à y accéder. Ces TP utilisent `gpt-4o` ; le workflow n8n utilise `gpt-4o-mini`. Une clé valide, l’accès au modèle et un quota API disponible sont nécessaires. Les appels API peuvent être facturés. Conservez la clé dans les secrets, sans l’écrire dans le notebook.

## Prompting et spécifications

Le TP Prompting propose quatre exercices : rédiger et réviser un post LinkedIn, comparer l’effet du ton d’un prompt, extraire des informations en JSON et analyser un jeu de données. Copiez les consignes dans votre assistant IA : ce notebook ne contient pas de code à exécuter. Pour l’exercice 4, joignez `selogerdata.csv` à la conversation.

Utilisez `SKILL.md` dans un outil prenant en charge les Skills, ou joignez son contenu à votre assistant en lui demandant d’appliquer la méthode. Il guide un entretien de cinq questions maximum pour produire une spécification avec des critères d’acceptation.

## Audit de user stories avec n8n

1. Téléchargez et importez `Audit_User_Story.json` dans n8n.
2. Sélectionnez vos propres identifiants OpenAI dans le nœud **Appel API LLM**. Aucun identifiant n’est inclus dans le workflow.
3. Lancez une exécution de test et ouvrez le **Formulaire US**.
4. Saisissez le titre et la description d’une user story, puis consultez les cinq critères, le score et les suggestions.

Le diagnostic sert de point de départ à une revue humaine.

## TP RAG — correction

Téléchargez le support de cours, **renommez-le `Cours.pdf`**, puis importez-le dans les fichiers de votre session Colab. Ouvrir le notebook n’importe pas automatiquement le PDF. Utilisez un PDF dont le texte est sélectionnable : ce TP ne fait pas de reconnaissance de texte sur les scans.

Exécutez dans l’ordre l’extraction et la segmentation, le calcul des embeddings, la recherche des passages similaires, puis la génération de la réponse. Modifiez `query` et relancez la recherche et la génération pour poser une autre question.

Utilisez une session Colab dédiée : le TP conserve `openai==0.28`. Seule la dernière étape utilise la clé API. Les passages sélectionnés et votre question sont transmis à l’API ; comparez la réponse avec le document source.

## TP Agents

Téléchargez `products.csv` et exécutez les sections 1 à 7 dans l’ordre. Importez le CSV lorsque le sélecteur apparaît. Le TP utilise les 1 000 premiers produits, construit un index FAISS et crée un serveur MCP. Vérifiez que la découverte des outils affiche `search_products`, `add_to_cart` et `view_cart`.

Après le message **Agent prêt.**, réexécutez uniquement la dernière cellule pour chaque demande :

- « Je cherche un pantalon de sport noir pour homme. »
- « Ajoute deux exemplaires du premier produit au panier. »
- « Montre-moi mon panier. »

La sortie affiche les appels MCP, les résultats des outils et les réponses de Buddy. Le panier est une simulation. Réexécuter la section 2 le vide ; réexécuter la section 6 réinitialise l’historique de conversation. Les prix conservent le format du catalogue, sans supposer leur devise.

## En cas de difficulté

| Problème | Action |
| --- | --- |
| Secret introuvable ou accès refusé | Vérifiez le nom `OPENAI_API_KEY` et activez l’accès au notebook. |
| Erreur d’authentification ou de quota | Vérifiez la clé, le quota API et l’accès au modèle. |
| PDF introuvable | Importez le support sous le nom exact `Cours.pdf`. |
| Aucun texte extrait | Utilisez un PDF avec du texte sélectionnable. |
| `products.csv` introuvable | Importez le fichier avec son nom exact, sans suffixe `(1)` ni extension `.txt`. |
| Variable inconnue ou erreur d’import | Reprenez les cellules dans l’ordre à partir de la première erreur ; redémarrez la session si nécessaire. |

Votre copie du notebook reste dans Drive. Les fichiers importés et les bibliothèques installées dépendent de la session temporaire Colab : après une réinitialisation, réimportez les fichiers et réexécutez les cellules.

Contact : **redha.moulla@axia-conseil.com**.

Pour poursuivre la veille en IA : [Courants de fond](https://redhamoulla.substack.com).
