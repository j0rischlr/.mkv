<template>
  <div class="h-screen bg-[#f8f9fa] text-gray-900 overflow-y-auto">
    <!-- Conteneur centré -->
    <div class="flex justify-center px-4">
      <div class="w-full max-w-6xl">
        <!-- Bouton retour -->
        <div class="py-4 sticky top-0 bg-[#f8f9fa]/80 backdrop-blur border-b border-gray-200 z-10 -mx-4 px-4">
          <router-link
            to="/"
            class="px-4 py-2 btn-gradient-shift rounded-lg transition-all inline-block text-sm text-white hover:brightness-110"
          >
            ← Retour
          </router-link>
        </div>
      </div>
    </div>
    
    <!-- État de chargement -->
    <div v-if="loading" class="h-96 flex items-center justify-center">
      <div class="text-center">
        <div class="loader-dots mb-4">
          <div class="loader-dot bg-blue-600"></div>
          <div class="loader-dot bg-purple-600"></div>
          <div class="loader-dot bg-blue-600"></div>
        </div>
        <p class="text-lg text-gray-600">Chargement...</p>
      </div>
    </div>
    
    <!-- Section avec background sombre pour la photo de l'acteur -->
    <div v-if="!loading && actor" class="w-full bg-gray-900 py-12">
      <div class="flex justify-center px-4">
        <div class="w-full max-w-6xl">
          <!-- En-tête : Photo + Infos -->
          <div class="flex items-start gap-8">
            <!-- Photo -->
            <div class="flex-shrink-0">
              <img
                v-if="actor.profile_path"
                :src="`https://image.tmdb.org/t/p/w342${actor.profile_path}`"
                :alt="actor.name"
                class="w-64 h-96 rounded-lg object-cover shadow-lg"
              />
              <div v-else class="w-64 h-96 rounded-lg bg-gray-800 flex items-center justify-center shadow-lg">
                <span class="text-gray-500">Pas d'image</span>
              </div>
            </div>

            <!-- Infos -->
            <div class="flex-1 pt-4">
              <h1 class="text-5xl font-bold mb-2 text-white">{{ actor.name }}</h1>
              <p v-if="actor.character" class="text-2xl text-gray-400">{{ actor.character }}</p>
              <div class="mt-6 text-gray-300">
                <p v-if="actor.birth_date" class="text-lg"><span class="font-semibold">Né(e) le:</span> {{ formatDate(actor.birth_date) }}</p>
                <p v-if="actor.birthplace" class="text-lg"><span class="font-semibold">Lieu:</span> {{ actor.birthplace }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Filmographie -->
    <div v-if="!loading && actor" class="flex justify-center px-4">
      <div class="w-full max-w-6xl py-8">
          <div>
            <h2 class="text-3xl font-bold mb-8">Filmographie</h2>
            <div v-if="actor.filmography && actor.filmography.length > 0" class="grid grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-6 pb-8">
              <router-link
                v-for="film in actor.filmography"
                :key="film.id"
                :to="`/movie/${film.id}`"
                class="bg-gray-900 rounded-xl overflow-hidden hover:bg-gray-800 transition-all hover:scale-105 cursor-pointer"
              >
                <img
                  v-if="film.poster_path"
                  :src="`https://image.tmdb.org/t/p/w185${film.poster_path}`"
                  :alt="film.title"
                  class="w-full h-full object-cover aspect-[2/3]"
                />
                <div v-else class="w-full aspect-[2/3] bg-gray-800 flex items-center justify-center">
                  <span class="text-gray-500 text-xs">Pas d'image</span>
                </div>
              </router-link>
            </div>
            <div v-else class="text-center text-gray-400 py-20">
              <p class="text-xl">Aucun film trouvé pour cet acteur</p>
            </div>
          </div>
      </div>
    </div>

        <!-- Erreur -->
        <div v-if="error" class="flex justify-center px-4">
          <div class="w-full max-w-6xl py-20 text-center">
          <p class="text-xl text-red-500 mb-4">Erreur: {{ error }}</p>
          <router-link to="/" class="text-blue-600 hover:text-blue-400">
            Retourner à l'accueil
          </router-link>
        </div>
        </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const actor = ref(null)
const loading = ref(true)
const error = ref(null)

const fetchActorDetails = async () => {
  const actorId = route.params.id
  try {
    const response = await fetch(`/api/actor/${actorId}`)
    if (!response.ok) {
      throw new Error('Erreur lors de la récupération des données')
    }
    actor.value = await response.json()
  } catch (err) {
    error.value = err.message
    console.error('Erreur:', err)
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('fr-FR', { year: 'numeric', month: 'long', day: 'numeric' })
}

onMounted(() => {
  fetchActorDetails()
})
</script>
