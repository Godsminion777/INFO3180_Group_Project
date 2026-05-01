import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as matchesApi from '../api/matches'

export const useMatchesStore = defineStore('matches', () => {
  const mutualMatches = ref([])
  const potentialMatches = ref([])
  const newMatchAlert = ref(null)

  async function fetchMutual() {
    const res = await matchesApi.getMutualMatches()
    mutualMatches.value = res.data.matches
  }

  async function fetchPotential() {
    const res = await matchesApi.getPotentialMatches()
    potentialMatches.value = res.data.potential_matches
  }

  async function act(receiverId, action) {
    const res = await matchesApi.doAction(receiverId, action)
    if (res.data.match?.is_mutual) {
      newMatchAlert.value = res.data.match
    }
    potentialMatches.value = potentialMatches.value.filter(
      pm => pm.profile.user_id !== receiverId
    )
    return res.data
  }

  function clearAlert() {
    newMatchAlert.value = null
  }

  return { mutualMatches, potentialMatches, newMatchAlert, fetchMutual, fetchPotential, act, clearAlert }
})
