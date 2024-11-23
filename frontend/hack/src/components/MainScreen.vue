<template>
  <div class="container mx-auto text-center mt-20">
    <img alt="Logo" src="@/assets/logo.png" class="logo mx-auto mb-4" />
    <h1 class="text-4xl font-bold text-gray-700 mb-4">TreeSearch - (Later)</h1>
    <form @submit.prevent="onSearch" class="flex flex-col sm:flex-row justify-center mb-4 gap-2 sm:gap-4">
      <input
        type="text"
        v-model="query"
        placeholder="Insert prompt"
        class="border border-gray-300 rounded-lg p-2 w-full sm:w-1/2 focus:outline-none focus:ring-2 focus:ring-blue-400"
      />
      <button
        type="submit"
        class="bg-blue-500 text-white rounded-lg p-2 w-full sm:w-auto sm:px-6 hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-400"
      >
        Search
      </button>
    </form>

    <div class="button-group mb-4">
      <button @click="onImportData" class="bg-green-500 text-white rounded p-2 mx-2">Import Data</button>
      <button @click="showSettings = true" class="bg-yellow-500 text-white rounded p-2 mx-2">Search Settings</button>
      <button @click="showDownloadModal = true" class="bg-red-500 text-white rounded p-2 mx-2">Download File</button>
    </div>

    <!-- Download File Modal -->
    <div v-if="showDownloadModal" class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center" @click.self="closeDownloadModal">
      <div class="bg-white p-8 rounded shadow-lg w-11/12 max-w-lg">
        <h2 class="text-2xl mb-4">Import file</h2>
        <form @submit.prevent="downloadFile">
          <input
            type="text"
            v-model="fileUrl"
            placeholder="Enter File URL"
            class="border border-gray-300 rounded-lg p-2 w-full mb-4"
          />
          <button type="submit" class="bg-blue-500 text-white rounded p-2">Download</button>
        </form>
      </div>
    </div>

    <input
      type="file"
      ref="fileInput"
      @change="onFileChange"
      style="display: none;"
      multiple
    />

    <!-- Modal -->
    <div v-if="showSettings" class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center" @click.self="closeModal">
      <div class="bg-white p-8 rounded shadow-lg w-11/12 max-w-lg">
        <h2 class="text-2xl mb-4">Search Settings</h2>
        <form>
          <div class="checkbox-group mb-4">
            <label class="block mb-2"><input type="checkbox" v-model="settings.option1" /> Option 1</label>
            <label class="block mb-2"><input type="checkbox" v-model="settings.option2" /> Option 2</label>
            <label class="block mb-2"><input type="checkbox" v-model="settings.option3" /> Option 3</label>
          </div>
          <button type="button" @click="saveSettings" class="bg-blue-500 text-white rounded p-2">Save</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'MainScreen',
  data() {
    return {
      query: '',
      files: [],
      showDownloadModal: false,
      showSettings: false,
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
        const response = await axios.get('http://localhost:8000/current-date/');
        const data = response.data;
        this.$router.push({ path: '/report', query: { data: JSON.stringify(data) } });
      } catch (error) {
        console.error('Error fetching data:', error);
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

        const response = await axios.post('http://localhost:8000/download-file/',
          { url: this.fileUrl },
        );
        console.log(response.data.message);
      } catch (error) {
        console.error('Error downloading file:', error);
      }
      this.closeDownloadModal();
  },
  },
};
</script>

<style>
.logo {
  width: 150px;
  height: auto;
}
</style>