<template>
  <div class="container">
    <img alt="Logo" src="@/assets/logo.png" class="logo" />
    <h1 class="title">TreeSearch - (Later)</h1>
    <form @submit.prevent="onSearch">
      <input type="text" v-model="query" placeholder="Insert prompt" />
      <button type="submit">Search</button>
    </form>
    <div class="button-group">
      <button @click="onImportData" class="import-button">Import Data</button>
      <button @click="showSettings = true" class="settings-button">
        Search Settings
      </button>
      <button @click="openDownloadModal" class="settings-button">Download File</button>
    </div>
    <input
      type="file"
      ref="fileInput"
      @change="onFileChange"
      style="display: none;"
      multiple
    />

    <!-- Modálne okno -->
    <div v-if="showSettings" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <h2>Search Settings</h2>
        <form>
          <div class="checkbox-group">
            <label><input type="checkbox" v-model="settings.option1" /> Option 1</label>
            <label><input type="checkbox" v-model="settings.option2" /> Option 2</label>
            <label><input type="checkbox" v-model="settings.option3" /> Option 3</label>
          </div>
          <button type="button" @click="saveSettings">Save</button>
        </form>
      </div>
    </div>
    <div v-if="showDownloadModal" class="bg-white p-8 rounded shadow-lg w-11/12 max-w-lg">
    <h2 class="text-2xl mb-4">Import file</h2>
    <div v-if="!isDownloading">
      <form @submit.prevent="downloadFile">
        <input
          type="text"
          v-model="fileUrl"
          placeholder="Enter File URL"
          class="border border-gray-300 rounded-lg p-2 w-full mb-4"
        />
        <button type="submit" class="bg-blue-500 text-white rounded p-2">
          Download
        </button>
      </form>
    </div>
    <div v-else class="text-center text-gray-700">
      <p>{{ downloadStatus }}</p>
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
      query: '', // Uchováva text z inputu
      files: [],
      downloadStatus: 'Downloading file...',
      isDownloading: false,
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
    if (this.query) {
      // Uložíme query do localStorage
      localStorage.setItem('query', this.query);
      console.log('Query uložené do localStorage:', this.query);

      // Zavoláme endpoint /validate-query/
      const response = await axios.post('http://localhost:8000/validate-query/', {
        query: this.query,
      });

      // Spracovanie odpovede
      if (response.data.valid) {
        console.log('Query validné. Presmerovanie na /loading.');
        this.$router.push({ path: '/loading' });
      } else {
        console.log('Query nevalidné. Presmerovanie na /error.');
        this.$router.push({ path: '/error' });
      }
    } else {
      alert('Prosím, zadajte query do inputu.');
    }
  } catch (error) {
    console.error('Chyba pri validácii query:', error);
    this.$router.push({ path: '/error' }); // Presmerovanie na /error pri chybe
  }
},

    onImportData() {
      this.$refs.fileInput.click();
    },
    onFileChange(event) {
      this.files = Array.from(event.target.files);
      console.log('Súbory importované:', this.files);
    },
    closeModal() {
      this.showSettings = false;
    },
    saveSettings() {
      console.log('Nastavenia uložené:', this.settings);
      this.closeModal();
    },
    closeDownloadModal() {
      this.showDownloadModal = false;
    },
    openDownloadModal() {
      this.isDownloading = false;
      this.downloadStatus = 'Downloading file...';
      this.showDownloadModal = true;
    },
    async downloadFile() {
      this.isDownloading = true;
      try {
        const response = await axios.post('http://localhost:8000/download-file/', {
          url: this.fileUrl,
        });
        console.log(response.data.message);
      } catch (error) {
        console.error('Error downloading file:', error);
      }
      this.downloadStatus = 'File imported successfully!';
      setTimeout(() => {

          this.closeDownloadModal(); // Close modal after a brief delay
        }, 2000);
    },
  },
};
</script>

<style>
/* Odstránili sme 'scoped', aby sa štýly aplikovali globálne */

body {
  background: url('~@/assets/back.jpg') no-repeat center center fixed;
  background-size: cover;
  margin: 0;
  height: 100vh;
}

.container {
  text-align: center;
  margin-top: 5%;
}

.logo {
  width: 150px;
  height: auto;
  margin-bottom: 1rem;
}

.title {
  font-size: 3rem;
  margin-bottom: 0.5rem;
  color: #808080; /* Sivá farba textu */
}

form {
  display: flex;
  justify-content: center;
}

input[type='text'] {
  width: 50%;
  padding: 0.5rem;
  font-size: 1rem;
}

button {
  margin-left: 0.5rem;
  padding: 0.5rem 1rem;
  font-size: 1rem;
}

.button-group {
  margin-top: 0.5rem;
}

.import-button,
.settings-button {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  margin: 0 0.5rem;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: #fff;
  padding: 2rem;
  width: 80%;
  max-width: 500px;
  border-radius: 8px;
}

.modal-content h2 {
  margin-top: 0;
}

.checkbox-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 1rem;
}

.checkbox-group label {
  margin-bottom: 0.5rem;
}

@media (max-width: 768px) {
  .title {
    font-size: 2rem;
  }

  input[type='text'] {
    width: 70%;
  }
}
</style>
