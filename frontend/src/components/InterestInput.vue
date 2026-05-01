<template>
  <div>
    <div class="flex flex-wrap gap-2 mb-2">
      <span
        v-for="interest in modelValue"
        :key="interest"
        class="flex items-center gap-1 px-3 py-1 bg-pink-50 dark:bg-pink-900/30 text-pink-600 dark:text-pink-300 rounded-full text-sm"
      >
        {{ interest }}
        <button type="button" @click="remove(interest)" class="hover:text-red-500 font-bold">×</button>
      </span>
    </div>
    <div class="flex gap-2">
      <input
        v-model="inputVal"
        type="text"
        placeholder="Add interest..."
        class="flex-1 px-3 py-1.5 border border-gray-300 dark:border-gray-600 rounded-lg text-sm bg-white dark:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-pink-300"
        @keydown.enter.prevent="add"
        @keydown.comma.prevent="add"
      />
      <button type="button" @click="add" class="px-3 py-1.5 bg-pink-500 text-white rounded-lg text-sm hover:bg-pink-600">Add</button>
    </div>
    <p class="text-xs text-gray-400 mt-1">Minimum 3 interests. Press Enter or comma to add.</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({ modelValue: { type: Array, default: () => [] } })
const emit = defineEmits(['update:modelValue'])
const inputVal = ref('')

function add() {
  const val = inputVal.value.trim().toLowerCase().replace(/,$/, '')
  if (val && !props.modelValue.includes(val)) {
    emit('update:modelValue', [...props.modelValue, val])
  }
  inputVal.value = ''
}

function remove(interest) {
  emit('update:modelValue', props.modelValue.filter(i => i !== interest))
}
</script>
