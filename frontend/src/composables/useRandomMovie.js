import { ref } from 'vue'

export function useRandomMovie() {
  const movie = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const fetchRandomMovie = async () => {
    loading.value = true
    error.value = null

    try {
      const response = await fetch('/api/random-movie')
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

  return { movie, loading, error, fetchRandomMovie }
}
