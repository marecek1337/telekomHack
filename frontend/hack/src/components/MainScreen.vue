<template>
  <div class="min-h-screen bg-cover bg-center flex flex-col items-center justify-start" style="background-image: url('src/assets/back.jpg');">
    <img alt="Logo" src="@/assets/logo.png" class="w-36 h-auto mb-4" />
    <h1 class="text-3xl font-bold text-gray-500 mb-4">TreeSearch - (Later)</h1>
    <form @submit.prevent="onSearch" class="flex justify-center items-center w-full max-w-3xl mb-4">
      <input
        type="text"
        v-model="query"
        placeholder="Insert prompt"
        class="flex-1 p-2 text-lg border border-gray-300 rounded-l focus:outline-none focus:ring-2 focus:ring-blue-400"
      />
      <button
        type="submit"
        class="p-2 text-lg bg-blue-500 text-white rounded-r hover:bg-blue-600 focus:outline-none"
      >
        Search
      </button>
    </form>
    <div class="flex space-x-4 mb-8">
      <button
        @click="onImportData"
        class="px-4 py-2 text-lg bg-green-500 text-white rounded hover:bg-green-600 focus:outline-none"
      >
        Import Data
      </button>
      <button
        @click="showSettings = true"
        class="px-4 py-2 text-lg bg-yellow-500 text-white rounded hover:bg-yellow-600 focus:outline-none"
      >
        Search Settings
      </button>
      <button
        @click="showDownloadModal = true"
        class="px-4 py-2 text-lg bg-purple-500 text-white rounded hover:bg-purple-600 focus:outline-none"
      >
        Download File
      </button>
    </div>
    <input type="file" ref="fileInput" @change="onFileChange" class="hidden" multiple />

    <!-- Settings Modal -->
    <div
      v-if="showSettings"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center"
      @click.self="closeModal"
    >
      <div class="bg-white p-8 rounded-lg w-11/12 max-w-lg shadow-lg">
        <h2 class="text-2xl font-bold mb-4">Search Settings</h2>
        <form>
          <div class="flex flex-col space-y-2 mb-4">
            <label class="flex items-center space-x-2">
              <input type="checkbox" v-model="settings.option1" class="rounded" />
              <span>Option 1</span>
            </label>
            <label class="flex items-center space-x-2">
              <input type="checkbox" v-model="settings.option2" class="rounded" />
              <span>Option 2</span>
            </label>
            <label class="flex items-center space-x-2">
              <input type="checkbox" v-model="settings.option3" class="rounded" />
              <span>Option 3</span>
            </label>
          </div>
          <button
            type="button"
            @click="saveSettings"
            class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 focus:outline-none"
          >
            Save
          </button>
        </form>
      </div>
    </div>

    <!-- Download Modal -->
    <div
      v-if="showDownloadModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center"
      @click.self="closeDownloadModal"
    >
      <div class="bg-white p-8 rounded-lg w-11/12 max-w-lg shadow-lg">
        <h2 class="text-2xl font-bold mb-4">Import File</h2>
        <form @submit.prevent="downloadFile">
          <input
            type="text"
            v-model="fileUrl"
            placeholder="Enter File URL"
            class="w-full p-2 border border-gray-300 rounded-lg mb-4 focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <button
            type="submit"
            class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 focus:outline-none"
          >
            Download
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'SearchPage',
  data() {
    return {
      query: '',
      files: [],
      showSettings: false,
      showDownloadModal: false,
      fileUrl: '',
      settings: {
        option1: false,
        option2: false,
        option3: false,
      },
    };
  },
  methods: {
    async onSearch() {
      try {
        this.$router.push({ path: '/loading' });
      } catch (error) {
        console.error('Error loading data:', error);
      }
    },
    onImportData() {
      this.$refs.fileInput.click();
    },
    onFileChange(event) {
      this.files = Array.from(event.target.files);
      console.log('Files imported:', this.files);
    },
    closeModal() {
      this.showSettings = false;
    },
    saveSettings() {
      console.log('Settings saved:', this.settings);
      this.closeModal();
    },
    closeDownloadModal() {
      this.showDownloadModal = false;
    },
    async downloadFile() {
      try {
        const response = await axios.post('http://localhost:8000/download-file/', {
          url: this.fileUrl,
        });
        console.log(response.data.message);
      } catch (error) {
        console.error('Error downloading file:', error);
      }
      this.closeDownloadModal();
    },
  },
};
</script>
