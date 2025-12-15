<template>
  <div
    class="min-h-screen relative overflow-hidden"
    :style="{
      backgroundImage: movie ? `url('https://image.tmdb.org/t/p/original${movie.backdrop_path || movie.poster_path}')` : '',
      backgroundSize: 'cover',
      backgroundPosition: 'center',
    }"
  >
    <!-- Overlay dégradé du bas vers haut (plus prononcé) -->
    <div class="absolute inset-0 bg-gradient-to-t from-black via-black/50 to-transparent"></div>

    <!-- Contenu principal -->
    <div class="relative z-10 w-full h-screen flex flex-col justify-end p-8 md:p-12">
      <!-- Bouton retour en haut à gauche -->
      <div class="absolute top-8 left-8 md:top-12 md:left-12">
        <router-link
          to="/"
          class="px-6 py-3 btn-gradient-shift rounded-lg transition-all inline-block text-sm text-white hover:brightness-110"
        >
          ← Retour
        </router-link>
      </div>

      <!-- Note en haut à droite -->
      <div v-if="movie" class="absolute top-8 right-8 md:top-12 md:right-12">
        <div class="flex items-center gap-2 text-white text-xl md:text-2xl font-semibold">
          <img src="/data/icones/icone_tmdb.svg" alt="Note" class="h-8 md:h-10 w-8 md:w-10" />
          <span>{{ movie.vote_average.toFixed(1) }}</span>
        </div>
      </div>

      <!-- État de chargement -->
      <div v-if="loading" class="text-center py-20">
        <div class="loader-dots mb-4 justify-center">
          <div class="loader-dot bg-white"></div>
          <div class="loader-dot bg-white"></div>
          <div class="loader-dot bg-white"></div>
        </div>
        <p class="text-white text-xl mt-4">Chargement du film...</p>
      </div>

      <!-- Film chargé -->
      <div v-else-if="movie" class="mb-8">
        <!-- Titre -->
        <h1 class="text-5xl md:text-6xl lg:text-7xl font-bold text-white drop-shadow-2xl mb-6">
          {{ movie.title }}
        </h1>

        <!-- Année et Genres entre le titre et le résumé -->
        <div class="flex flex-wrap items-center gap-4 mb-6 text-white text-sm md:text-base">
          <div class="flex items-center gap-2">
            <span class="text-lg md:text-xl font-semibold">{{ movie.release_date.split('-')[0] || 'Inconnue' }}</span>
          </div>
          <div class="flex flex-wrap gap-2">
            <span
              v-for="genre in movie.genres"
              :key="genre"
              class="px-3 py-1 text-white rounded-full text-xs font-medium backdrop-blur-sm"
              :style="{ backgroundColor: '#E57300', opacity: '0.5' }"
            >
              {{ genre }}
            </span>
          </div>
        </div>

        <!-- Résumé dessous -->
        <div class="mb-8 max-w-3xl">
          <p class="text-white text-base md:text-lg leading-relaxed drop-shadow-lg line-clamp-4">
            {{ movie.overview }}
          </p>
        </div>

        <!-- Boutons et Acteurs sur la même ligne -->
        <div class="flex items-end justify-between gap-8">
          <!-- Bouton "Bande annonce" si disponible -->
          <div class="flex gap-4">
            <a
              v-if="movie && movie.trailer_url"
              :href="movie.trailer_url"
              target="_blank"
              rel="noopener noreferrer"
              class="btn-gradient-shift px-8 py-3 text-white font-bold rounded-lg shadow-xl backdrop-blur-sm transition-all inline-flex items-center"
            >
              🎥 Bande annonce
            </a>
          </div>

          <!-- Acteurs à droite -->
          <div v-if="movie && movie.cast && movie.cast.length > 0" class="flex gap-8">
            <router-link
              v-for="actor in movie.cast"
              :key="actor.name"
              :to="`/actor/${actor.id}`"
              class="flex flex-col items-center gap-2 hover:opacity-80 transition-opacity"
            >
              <div class="actor-card cursor-pointer">
                <img
                  v-if="actor.profile_path"
                  :src="`https://image.tmdb.org/t/p/w185${actor.profile_path}`"
                  :alt="actor.name"
                  class="w-20 h-20 rounded-full object-cover shadow-lg"
                />
              </div>
            </router-link>
          </div>
        </div>
      </div>

      <!-- Erreur -->
      <div v-else-if="error" class="mb-8">
        <p class="text-white text-xl mb-4 drop-shadow-lg">❌ Erreur: {{ error }}</p>
        <router-link
          to="/"
          class="px-6 py-2 bg-red-600 bg-opacity-80 text-white font-bold rounded-lg hover:bg-red-700 transition-all backdrop-blur-sm inline-block"
        >
          Retour à l'accueil
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const movie = ref(null)
const loading = ref(true)
const error = ref(null)

const fetchMovieDetails = async () => {
  const movieId = route.params.id
  loading.value = true
  error.value = null
  
  try {
    const response = await fetch(`/api/movie/${movieId}`)
    if (!response.ok) {
      throw new Error('Erreur lors de la récupération du film')
    }
    movie.value = await response.json()
  } catch (err) {
    error.value = err.message
    console.error('Erreur:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchMovieDetails()
})

// Watcher pour mettre à jour quand l'ID du film change
watch(() => route.params.id, () => {
  fetchMovieDetails()
})
</script>
