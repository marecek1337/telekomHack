<template>
  <div class="container">
    <h1 class="title">TreeSearch - (Later)</h1>
    <form @submit.prevent="onSearch">
      <input
        type="text"
        v-model="query"
        placeholder="Insert prompt"
      />
      <button type="submit">Search</button>
    </form>
    <button @click="onImportData" class="import-button">Import Data</button>
    <input type="file" ref="fileInput" @change="onFileChange" style="display: none;" multiple />
  </div>
</template>

<script>
export default {
  name: "SearchPage",
  data() {
    return {
      query: "",
      files: [],
    };
  },
  methods: {
    onSearch() {
      // Tu môžete pridať funkciu na spracovanie vyhľadávania
      console.log("Hľadám:", this.query);
    },
    onImportData() {
      this.$refs.fileInput.click();
    },
    onFileChange(event) {
      this.files = Array.from(event.target.files);
      console.log("Súbory importované:", this.files);
      // Tu môžete pridať logiku na spracovanie importovaných súborov
    },
  },
};
</script>

<style scoped>
.container {
  text-align: center;
  margin-top: 10%;
}

.title {
  font-size: 3rem;
  margin-bottom: 1rem; /* Znížená medzera z 2rem na 1rem */
}

form {
  display: flex;
  justify-content: center;
}

input[type="text"] {
  width: 50%;
  padding: 0.5rem;
  font-size: 1rem;
}

button {
  margin-left: 0.5rem;
  padding: 0.5rem 1rem;
  font-size: 1rem;
}

.import-button {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  font-size: 1rem;
}

@media (max-width: 768px) {
  .title {
    font-size: 2rem;
  }

  input[type="text"] {
    width: 70%;
  }
}
</style>
