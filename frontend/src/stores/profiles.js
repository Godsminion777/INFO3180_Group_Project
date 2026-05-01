import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import * as profilesApi from '../api/profiles'

export const useProfilesStore = defineStore('profiles', () => {
  const allProfiles = ref([])
  const savedIds = ref(JSON.parse(localStorage.getItem('savedProfiles') || '[]'))

  const savedProfiles = computed(() =>
    allProfiles.value.filter(p => savedIds.value.includes(p.id))
  )

  async function fetchAll() {
    const res = await profilesApi.getAllProfiles()
    allProfiles.value = res.data.profiles
  }

  async function fetchOne(id) {
    const res = await profilesApi.getProfile(id)
    return res.data.profile
  }

  async function fetchOneByUserId(userId) {
    const uid = Number(userId)
    if (!allProfiles.value.length) await fetchAll()
    const found = allProfiles.value.find(p => p.user_id === uid)
    if (found) return found
    const res = await profilesApi.getAllProfiles()
    allProfiles.value = res.data.profiles
    return allProfiles.value.find(p => p.user_id === uid) || null
  }

  async function update(id, data) {
    const res = await profilesApi.updateProfile(id, data)
    return res.data.profile
  }

  async function uploadPhoto(id, file) {
    const fd = new FormData()
    fd.append('photo', file)
    const res = await profilesApi.uploadPhoto(id, fd)
    return res.data.photo_url
  }

  function toggleSave(profileId) {
    const idx = savedIds.value.indexOf(profileId)
    if (idx === -1) {
      savedIds.value.push(profileId)
    } else {
      savedIds.value.splice(idx, 1)
    }
    localStorage.setItem('savedProfiles', JSON.stringify(savedIds.value))
  }

  function isSaved(profileId) {
    return savedIds.value.includes(profileId)
  }

  function searchProfiles(filters) {
    return allProfiles.value.filter(p => {
      const { location, ageMin, ageMax, interests, keyword } = filters
      if (location && !p.location?.toLowerCase().includes(location.toLowerCase())) return false
      if (ageMin && p.age < Number(ageMin)) return false
      if (ageMax && p.age > Number(ageMax)) return false
      if (interests?.length) {
        const pInterests = p.interests || []
        if (!interests.some(i => pInterests.includes(i))) return false
      }
      if (keyword) {
        const kw = keyword.toLowerCase()
        if (
          !p.first_name?.toLowerCase().includes(kw) &&
          !p.last_name?.toLowerCase().includes(kw) &&
          !p.bio?.toLowerCase().includes(kw)
        ) return false
      }
      return true
    })
  }

  return { allProfiles, savedIds, savedProfiles, fetchAll, fetchOne, fetchOneByUserId, update, uploadPhoto, toggleSave, isSaved, searchProfiles }
})
