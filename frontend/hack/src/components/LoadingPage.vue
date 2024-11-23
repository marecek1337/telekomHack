<template>
    <div class="loading-page" :style="backgroundStyle">
      <h1 class="title">Loading Tree Structure</h1>
      <div v-if="currentLineIndex < lines.length" class="text-display">
        {{ lines[currentLineIndex] }}
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        lines: [
          "├── README.md",
          "├── abc.txt",
          "├── backend",
          "│   ├── db.sqlite3",
          "│   ├── manage.py",
          "│   ├── prog",
          "│   │   ├── __init__.py",
          "│   │   ├── __pycache__",
          "│   │   ├── settings.py",
          "│   │   ├── urls.py",
          "│   │   └── views.py",
          "│   └── test_views.py"
        ], // Prvých pár riadkov z vášho súboru
        currentLineIndex: 0,
        interval: null,
      };
    },
    computed: {
      backgroundStyle() {
        return {
          backgroundImage: "url('@/assets/back.jpg')",
          backgroundSize: "cover",
          backgroundPosition: "center",
          height: "100vh",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
        };
      },
    },
    mounted() {
      // Spúšťanie riadkov po jednom
      this.interval = setInterval(() => {
        if (this.currentLineIndex < this.lines.length - 1) {
          this.currentLineIndex++;
        } else {
          clearInterval(this.interval);
        }
      }, 500); // Zobrazuje nový riadok každú sekundu
  
      // Presmerovanie na /report po 10 sekundách
      setTimeout(() => {
        this.$router.push("/report");
      }, 5000);
    },
    beforeUnmount() {
      clearInterval(this.interval);
    },
  };
  </script>
  
  <style scoped>
  .loading-page {
    position: relative;
    overflow: hidden;
  }
  .title {
    font-size: 2.5rem;
    color: white;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
    margin-bottom: 20px;
  }
  .text-display {
    font-size: 1.5rem;
    color: white;
    text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.5);
    animation: fadeIn 1s;
  }
  @keyframes fadeIn {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }
  </style>
  