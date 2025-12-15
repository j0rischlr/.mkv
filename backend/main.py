import httpx
import random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY", "YOUR_TMDB_API_KEY_HERE")
TMDB_BASE_URL = "https://api.themoviedb.org/3"

app = FastAPI(title="Random Movie API")

# Configuration CORS pour permettre les requêtes du frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À limiter en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MovieResponse(BaseModel):
    id: int
    title: str
    backdrop_path: Optional[str]
    poster_path: Optional[str]
    overview: str
    release_date: str
    vote_average: float
    genres: list[str]
    trailer_url: Optional[str]
    runtime: Optional[int]
    cast: list[dict]  # Liste des acteurs avec nom, photo et ID


class ActorResponse(BaseModel):
    id: int
    name: str
    profile_path: Optional[str]
    character: Optional[str]
    birth_date: Optional[str]
    birthplace: Optional[str]
    filmography: list[dict]


@app.get("/api/random-movie", response_model=MovieResponse)
async def get_random_movie():
    """
    Retourne un film aléatoire provenant de TMDB.
    Utilise discover/movie avec une page aléatoire et un index aléatoire.
    Retourne uniquement les films ayant un résumé non-vide.
    """
    try:
        async with httpx.AsyncClient() as client:
            max_attempts = 10
            attempts = 0
            
            while attempts < max_attempts:
                attempts += 1
                
                # Étape 1: Découvrir les films avec une page aléatoire
                random_page = random.randint(1, 500)
                
                discover_url = f"{TMDB_BASE_URL}/discover/movie"
                discover_params = {
                    "api_key": TMDB_API_KEY,
                    "page": random_page,
                    "sort_by": "popularity.desc",
                    "language": "fr-FR",
                }
                
                discover_response = await client.get(discover_url, params=discover_params)
                discover_response.raise_for_status()
                discover_data = discover_response.json()
                
                # Étape 2: Sélectionner un film aléatoire de la liste
                if not discover_data.get("results"):
                    raise ValueError("Aucun film trouvé")
                
                random_movie = random.choice(discover_data["results"])
                movie_id = random_movie["id"]
                
                # Étape 3: Récupérer les détails complets du film (genres)
                details_url = f"{TMDB_BASE_URL}/movie/{movie_id}"
                details_params = {
                    "api_key": TMDB_API_KEY,
                    "language": "fr-FR",
                }
                
                details_response = await client.get(details_url, params=details_params)
                details_response.raise_for_status()
                details_data = details_response.json()
                
                # Étape 4: Vérifier que le film a un résumé non-vide
                overview = details_data.get("overview", "").strip()
                if not overview:
                    # Pas de résumé, continuer la boucle
                    continue
                
                # Étape 5: Récupérer la bande annonce (videos)
                videos_url = f"{TMDB_BASE_URL}/movie/{movie_id}/videos"
                videos_params = {
                    "api_key": TMDB_API_KEY,
                    "language": "fr-FR",
                }
                
                trailer_url = None
                try:
                    videos_response = await client.get(videos_url, params=videos_params)
                    videos_response.raise_for_status()
                    videos_data = videos_response.json()
                    
                    # Chercher un trailer YouTube
                    for video in videos_data.get("results", []):
                        if video.get("type") == "Trailer" and video.get("site") == "YouTube":
                            trailer_url = f"https://www.youtube.com/watch?v={video.get('key')}"
                            break
                except:
                    trailer_url = None
                
                # Étape 6: Récupérer les acteurs (credits)
                credits_url = f"{TMDB_BASE_URL}/movie/{movie_id}/credits"
                credits_params = {
                    "api_key": TMDB_API_KEY,
                    "language": "fr-FR",
                }
                
                cast = []
                try:
                    credits_response = await client.get(credits_url, params=credits_params)
                    credits_response.raise_for_status()
                    credits_data = credits_response.json()
                    
                    # Récupérer les 8 premiers acteurs avec leur photo et ID
                    for actor in credits_data.get("cast", [])[:8]:
                        if actor.get("profile_path"):
                            cast.append({
                                "id": actor.get("id", ""),
                                "name": actor.get("name", ""),
                                "profile_path": actor.get("profile_path", ""),
                                "character": actor.get("character", "")
                            })
                except:
                    cast = []
                
                # Étape 7: Construire la réponse
                genres = [genre["name"] for genre in details_data.get("genres", [])]
                
                return MovieResponse(
                    id=movie_id,
                    title=details_data.get("title", "Titre inconnu"),
                    backdrop_path=details_data.get("backdrop_path"),
                    poster_path=details_data.get("poster_path"),
                    overview=overview,
                    release_date=details_data.get("release_date", "Date inconnue"),
                    vote_average=details_data.get("vote_average", 0),
                    genres=genres,
                    trailer_url=trailer_url,
                    runtime=details_data.get("runtime"),
                    cast=cast,
                )
            
            # Si on a épuisé les tentatives
            raise ValueError("Impossible de trouver un film avec un résumé après 10 tentatives")
            
    except Exception as e:
        print(f"Erreur lors de la récupération du film: {e}")
        raise


@app.get("/health")
async def health_check():
    """Endpoint de vérification de santé."""
    return {"status": "ok"}


@app.get("/api/movie/{movie_id}", response_model=MovieResponse)
async def get_movie_details(movie_id: int):
    """Retourne les détails d'un film spécifique par son ID."""
    try:
        async with httpx.AsyncClient() as client:
            # Récupérer les détails complets du film
            details_url = f"{TMDB_BASE_URL}/movie/{movie_id}"
            details_params = {
                "api_key": TMDB_API_KEY,
                "language": "fr-FR",
            }
            
            details_response = await client.get(details_url, params=details_params)
            details_response.raise_for_status()
            details_data = details_response.json()
            
            # Récupérer la bande annonce (videos)
            videos_url = f"{TMDB_BASE_URL}/movie/{movie_id}/videos"
            videos_params = {
                "api_key": TMDB_API_KEY,
                "language": "fr-FR",
            }
            
            trailer_url = None
            try:
                videos_response = await client.get(videos_url, params=videos_params)
                videos_response.raise_for_status()
                videos_data = videos_response.json()
                
                # Chercher un trailer YouTube
                for video in videos_data.get("results", []):
                    if video.get("type") == "Trailer" and video.get("site") == "YouTube":
                        trailer_url = f"https://www.youtube.com/watch?v={video.get('key')}"
                        break
            except:
                trailer_url = None
            
            # Récupérer les acteurs (credits)
            credits_url = f"{TMDB_BASE_URL}/movie/{movie_id}/credits"
            credits_params = {
                "api_key": TMDB_API_KEY,
                "language": "fr-FR",
            }
            
            cast = []
            try:
                credits_response = await client.get(credits_url, params=credits_params)
                credits_response.raise_for_status()
                credits_data = credits_response.json()
                
                # Récupérer les 8 premiers acteurs avec leur photo et ID
                for actor in credits_data.get("cast", [])[:8]:
                    if actor.get("profile_path"):
                        cast.append({
                            "id": actor.get("id", ""),
                            "name": actor.get("name", ""),
                            "profile_path": actor.get("profile_path", ""),
                            "character": actor.get("character", "")
                        })
            except:
                cast = []
            
            # Construire la réponse
            genres = [genre["name"] for genre in details_data.get("genres", [])]
            
            return MovieResponse(
                id=movie_id,
                title=details_data.get("title", "Titre inconnu"),
                backdrop_path=details_data.get("backdrop_path"),
                poster_path=details_data.get("poster_path"),
                overview=details_data.get("overview", ""),
                release_date=details_data.get("release_date", "Date inconnue"),
                vote_average=details_data.get("vote_average", 0),
                genres=genres,
                trailer_url=trailer_url,
                runtime=details_data.get("runtime"),
                cast=cast,
            )
            
    except Exception as e:
        print(f"Erreur lors de la récupération du film: {e}")
        raise


@app.get("/api/actor/{actor_id}", response_model=ActorResponse)
async def get_actor_details(actor_id: int):
    """Retourne les détails d'un acteur et sa filmographie."""
    try:
        async with httpx.AsyncClient() as client:
            # Récupérer les détails de l'acteur
            actor_url = f"{TMDB_BASE_URL}/person/{actor_id}"
            actor_params = {
                "api_key": TMDB_API_KEY,
                "language": "fr-FR",
            }
            
            actor_response = await client.get(actor_url, params=actor_params)
            actor_response.raise_for_status()
            actor_data = actor_response.json()
            
            # Récupérer la filmographie de l'acteur
            filmography_url = f"{TMDB_BASE_URL}/person/{actor_id}/movie_credits"
            filmography_params = {
                "api_key": TMDB_API_KEY,
                "language": "fr-FR",
            }
            
            filmography_response = await client.get(filmography_url, params=filmography_params)
            filmography_response.raise_for_status()
            filmography_data = filmography_response.json()
            
            # Construire la liste des films (limité aux 50 premiers avec ou sans affiche)
            filmography = []
            for film in filmography_data.get("cast", [])[:50]:
                # Inclure les films même s'ils n'ont pas d'affiche
                filmography.append({
                    "id": film.get("id", ""),
                    "title": film.get("title", "Titre inconnu"),
                    "poster_path": film.get("poster_path", ""),  # Peut être None
                    "character": film.get("character", ""),
                    "release_date": film.get("release_date", "Date inconnue")
                })
            
            return ActorResponse(
                id=actor_id,
                name=actor_data.get("name", "Acteur inconnu"),
                profile_path=actor_data.get("profile_path"),
                character="",  # Le rôle n'est pas disponible ici
                birth_date=actor_data.get("birthday"),
                birthplace=actor_data.get("place_of_birth"),
                filmography=filmography
            )
            
    except Exception as e:
        print(f"Erreur lors de la récupération de l'acteur: {e}")
        raise


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
