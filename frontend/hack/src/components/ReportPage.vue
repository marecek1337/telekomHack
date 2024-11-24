<script>
import axios from "axios";
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

export default {
  name: "ReportPage",
  data() {
    return {
      infoContent: "", // Na dynamické načítanie informácií z API
      loadingChart: true, // Stav načítavania grafu
      chartInstance: null, // Ukladá inštanciu grafu Chart.js
      query: "", // Načítané query z localStorage alebo manuálne zadanie
    };
  },
  methods: {
    log(message) {
      console.log(`[LOG] ${new Date().toISOString()}: ${message}`);
    },
    fetchQueryFromLocalStorage() {
      const storedQuery = localStorage.getItem("query");
      if (storedQuery) {
        this.query = storedQuery;
        this.log(`Načítané query z localStorage: ${this.query}`);
      } else {
        this.query = ""; // Ak nie je query, pole zostane prázdne
        this.log("Nebolo nájdené žiadne query v localStorage.");
      }
    },
    saveQueryToLocalStorage() {
      if (this.query) {
        localStorage.setItem("query", this.query);
        this.log(`Query uložené do localStorage: ${this.query}`);
      }
    },
    fetchInfo() {
      if (!this.query) {
        this.log("Query nie je dostupné.");
        return;
      }

      this.log(`Začiatok volania API pre informácie s query: ${this.query}`);

      axios
        .post("http://localhost:8000/get-info/", { query: this.query }) // API endpoint pre informácie
        .then((response) => {
          this.infoContent = response.data.message;
          this.log("Úspešné načítanie informácií.");
        })
        .catch((error) => {
          console.error("Chyba pri načítaní informácií:", error);
          this.infoContent = "Nepodarilo sa načítať informácie.";
          this.log("Chyba pri načítaní informácií.");
        });
    },
    renderChart() {
      if (!this.query) {
        this.log("Query nie je dostupné.");
        return;
      }

      this.loadingChart = true;
      this.log(`Začiatok volania API pre graf s query: ${this.query}`);

      axios
        .post("http://localhost:8000/get-chart/", { query: this.query }) // API endpoint pre graf
        .then((response) => {
          const chartCode = response.data;
          this.log("Získaný kód pre graf:");
          console.log(chartCode);

          this.loadingChart = false;

          this.$nextTick(() => {
            const canvasElement = document.getElementById("myChart");

            if (!canvasElement) {
              console.error("Canvas element s ID 'myChart' neexistuje.");
              return;
            }

            if (this.chartInstance) {
              this.chartInstance.destroy();
              this.log("Starý graf bol zničený.");
            }

            try {
              const script = new Function("Chart", "document", chartCode);
              script(Chart, document);
              this.chartInstance = Chart.getChart("myChart");
              this.log("Úspešné načítanie a vykreslenie grafu.");
            } catch (error) {
              console.error("Chyba pri vykresľovaní grafu:", error);
              this.log("Chyba pri vykresľovaní grafu.");
            }
          });
        })
        .catch((error) => {
          console.error("Chyba pri volaní API pre graf:", error);
          this.log("Chyba pri volaní API pre graf.");
          this.loadingChart = false;
        });
    },
    handleQueryChange() {
      this.saveQueryToLocalStorage();
      this.fetchInfo();
      this.renderChart();
    },
    exportPageAsHTML() {
      const htmlContent = document.documentElement.outerHTML;
      const blob = new Blob([htmlContent], { type: "text/html" });
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = "report.html";
      link.click();
    },
  },
  mounted() {
    this.log("Komponent bol načítaný.");
    this.fetchQueryFromLocalStorage();
    this.fetchInfo();
    this.renderChart();
  },
};
</script>

<template>
  <div class="report-page">
    <!-- Horný panel -->
    <div class="top-bar">
      <div class="top-bar-right">
        <button @click="exportPageAsHTML">Export</button>
      </div>
    </div>

    <!-- Nadpis a vstupné pole -->
    <div class="prompt-section">
      <h2>Zadané query: {{ query }}</h2>
      <input
        type="text"
        v-model="query"
        placeholder="Zadajte nové query..."
        @change="handleQueryChange"
      />
    </div>

    <!-- Hlavný obsah -->
    <div class="content">
      <!-- Ľavý panel -->
      <div class="left-panel">
        <h2>Informácie</h2>
        <p>{{ infoContent }}</p>
      </div>

      <!-- Pravý panel -->
      <div class="right-panel">
        <h2>Graf</h2>
        <div v-if="loadingChart">Načítava sa graf...</div>
        <div v-else>
          <canvas id="myChart"></canvas>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
/* Štýly */
body {
  background: url("~@/assets/back.jpg") no-repeat center center fixed;
  background-size: cover;
  margin: 0;
  padding: 0;
  height: 100vh;
}

.top-bar {
  width: 100%;
  height: 60px;
  background-color: rgb(219, 0, 123);
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding: 0 20px;
  position: fixed;
  top: 0;
  z-index: 1000;
}

.top-bar button {
  padding: 10px 20px;
  font-size: 1rem;
  background-color: white;
  color: rgb(219, 0, 123);
  border: 2px solid rgb(219, 0, 123);
  border-radius: 5px;
  cursor: pointer;
  transform: translateX(-50%); /* Posun tlačidla o 10% doľava */
}


.prompt-section {
  margin-top: 80px;
  text-align: center;
}

.prompt-section h2 {
  color: rgb(219, 0, 123);
  font-size: 1.5rem;
}

.prompt-section input {
  width: 60%;
  padding: 10px;
  font-size: 1rem;
  border: 2px solid rgb(219, 0, 123);
  border-radius: 5px;
  margin-top: 10px;
}

.content {
  display: flex;
  gap: 20px;
  height: 50%;
  width: 80%;
  margin: 40px auto 0;
  justify-content: center;
  align-items: stretch;
}

.left-panel,
.right-panel {
  flex: 1;
  padding: 20px;
  background-color: white;
  border-radius: 15px;
  border: 2px solid rgb(219, 0, 123);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  max-width: 45%;
}

.left-panel h2,
.right-panel h2 {
  color: rgb(219, 0, 123);
}

@media (max-width: 768px) {
  .content {
    flex-direction: column;
    width: 90%;
    margin: 20px 0 0;
  }

  .left-panel,
  .right-panel {
    width: 100%;
    height: auto;
    border-radius: 0;
    border-left: none;
    border-right: none;
  }
}
</style>
