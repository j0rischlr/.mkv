# 🎬 Random Movie Discovery App

Application web de découverte de films aléatoires basée sur l'API TMDB.

## 📋 Structure du Projet

```
.
├── backend/              # API FastAPI
│   ├── main.py          # Application principale
│   ├── requirements.txt  # Dépendances Python
│   └── .env.example      # Variables d'environnement
└── frontend/            # Application Vue.js
    ├── src/
    │   ├── components/   # Composants Vue
    │   ├── composables/  # Logique réutilisable
    │   ├── App.vue       # Composant racine
    │   ├── main.js       # Point d'entrée
    │   └── style.css     # Styles globaux
    ├── index.html        # HTML principal
    ├── vite.config.js    # Configuration Vite
    ├── tailwind.config.js # Configuration TailwindCSS
    └── package.json      # Dépendances du projet
```

## 🚀 Installation et Lancement

### Prérequis

- Python 3.9+
- Node.js 18+
- Clé API TMDB (gratuite sur https://www.themoviedb.org/settings/api)

### Backend

1. Naviguez vers le dossier backend :
```bash
cd backend
```

2. Créez un fichier `.env` avec votre clé TMDB :
```bash
cp .env.example .env
# Éditez .env et remplacez YOUR_TMDB_API_KEY_HERE par votre vraie clé
```

3. Installez les dépendances :
```bash
pip install -r requirements.txt
```

4. Lancez le serveur FastAPI :
```bash
uvicorn main:app --reload
```

Le backend sera disponible à `http://localhost:8000`

### Frontend

1. Naviguez vers le dossier frontend (dans un nouveau terminal) :
```bash
cd frontend
```

2. Installez les dépendances :
```bash
npm install
```

3. Lancez le serveur de développement :
```bash
npm run dev
```

Le frontend sera disponible à `http://localhost:5173`

## 🔌 Endpoints API

### GET /api/random-movie
Retourne un film aléatoire au format JSON.

**Réponse exemple:**
```json
{
  "id": 550,
  "title": "Fight Club",
  "backdrop_path": "/fCayJrkfRaCo5LRjZZaZCERwK1d.jpg",
  "poster_path": "/pB8BM7pdSp6B6Ih7QZ4DrQ3PchA.jpg",
  "overview": "Un homme ouvrier qui souffre d'une insomnie chronique...",
  "release_date": "1999-10-15",
  "vote_average": 8.4,
  "genres": ["Drama", "Thriller"]
}
```

## 🎨 Caractéristiques

✅ Interface full-screen immersive avec image de fond
✅ Fond flou avec overlay sombre
✅ Affichage du titre, année, note TMDB et genres
✅ Résumé (synopsis) du film
✅ Bouton "Nouveau film" pour charger un film aléatoire
✅ UI responsive et stylée avec TailwindCSS
✅ États de chargement et gestion d'erreurs
✅ Animation du bouton au survol
✅ Composables Vue pour la logique réutilisable

## 🛠️ Stack Technologique

### Backend
- **FastAPI** : Framework web asynchrone
- **httpx** : Client HTTP asynchrone pour appeler TMDB
- **uvicorn** : Serveur ASGI
- **python-dotenv** : Gestion des variables d'environnement

### Frontend
- **Vue.js 3** : Framework JavaScript avec Composition API
- **Vite** : Bundler ultra-rapide
- **TailwindCSS** : Framework CSS utilitaire
- **PostCSS** : Outil de transformation CSS

## 📝 Points Clés de l'Implémentation

### Backend (main.py)
- Route `/api/random-movie` qui :
  - Sélectionne une page aléatoire (1-500) via discover/movie
  - Choisit un film aléatoire de cette page
  - Récupère les détails complètes (genres) via l'endpoint details
  - Retourne toutes les informations en JSON

- CORS activé pour permettre les requêtes du frontend
- Gestion d'erreurs et validation avec Pydantic

### Frontend (Vue.js 3 - Composition API)
- Composable `useRandomMovie` pour la logique métier
- Composant `RandomMovie.vue` pour l'affichage
- États: chargement, erreur, film chargé, état initial
- Fetch asynchrone vers `/api/random-movie`
- Affichage de l'image via TMDB image service
- Animations et transitions avec TailwindCSS

## 🌍 Obtenir une Clé API TMDB

1. Allez sur https://www.themoviedb.org/settings/api
2. Créez un compte (gratuit)
3. Acceptez les conditions et remplissez le formulaire
4. Générez votre clé API
5. Copiez la clé dans le fichier `.env` du backend

## 🚀 Build en Production

### Backend
Le backend est prêt pour la production. Lancez-le simplement avec :
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend
Générez le build production :
```bash
npm run build
```

Servez les fichiers statiques depuis le dossier `dist/`

## 📱 Responsive Design

L'application est entièrement responsive grâce à TailwindCSS :
- Desktop (1024px+)
- Tablet (768px - 1023px)
- Mobile (< 768px)

## 🐛 Dépannage

**L'API TMDB retourne une erreur 401**
- Vérifiez que votre clé API est correcte dans le `.env`
- Régénérez votre clé depuis le dashboard TMDB si nécessaire

**Le frontend ne peut pas se connecter au backend**
- Assurez-vous que le backend s'exécute sur `localhost:8000`
- Vérifiez la configuration proxy dans `vite.config.js`

**Pas d'image de fond**
- Vérifiez que le film a une `backdrop_path` ou `poster_path`
- Assurez-vous que l'URL TMDB image est accessible

## 📄 Licence

Libre d'utilisation à titre personnel.

---

Bon visionnage ! 🍿
