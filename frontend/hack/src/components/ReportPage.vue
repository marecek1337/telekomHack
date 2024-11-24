  <!-- src/components/ReportPage.vue -->

<template>
  <div class="report-page">
    <!-- Horný panel -->
    <div class="top-bar">
      <div class="top-bar-right">
        <select v-model="selectedOption">
          <option disabled value="">Prosím vyberte</option>
          <option>Možnosť 1</option>
          <option>Možnosť 2</option>
          <option>Možnosť 3</option>
        </select>
        <button @click="handleButtonClick">Klikni ma</button>
      </div>
    </div>

    <!-- Nadpis a vstupné pole -->
    <div class="prompt-section">
      <h2>Vyhľadaj údaje v Telekome o používaní MacBookov medzi developermi</h2>
      <input type="text" placeholder="Pokračuj v prompte..." />
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

<script>
import axios from "axios";
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

export default {
  name: "ReportPage",
  data() {
    return {
      infoContent: "", // Na dynamické načítanie informácií z API
      selectedOption: "",
      loadingChart: true, // Stav načítavania grafu
      chartInstance: null, // Ukladá inštanciu grafu Chart.js
    };
  },
  methods: {
    log(message) {
      console.log(`[LOG] ${new Date().toISOString()}: ${message}`);
    },
    fetchInfo() {
      this.log("Začiatok volania API pre informácie.");
      axios
        .get("http://localhost:8000/get-info/") // API endpoint pre informácie
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
  this.loadingChart = true; // Začiatok načítavania grafu
  this.log("Začiatok volania API pre graf.");

  axios
    .get("http://localhost:8000/get-chart/") // API endpoint pre graf
    .then((response) => {
      // Logovanie celého JSON pre graf
      this.log("Celý JSON odpovede z API pre graf:");
      console.log(response.data);

      const chartCode = response.data; // Oprava tu

      // Logovanie získaného kódu grafu pre kontrolu
      this.log("Získaný kód pre graf:");
      console.log(chartCode);

      // Nastavíme loadingChart na false, aby sa `<canvas>` element zobrazil
      this.loadingChart = false;

      // Počkáme na aktualizáciu DOM
      this.$nextTick(() => {
        const canvasElement = document.getElementById("myChart");

        if (!canvasElement) {
          console.error("Canvas element s ID 'myChart' neexistuje.");
          return;
        }

        // Zničenie predchádzajúceho grafu, ak už existuje
        if (this.chartInstance) {
          this.chartInstance.destroy();
          this.log("Starý graf bol zničený.");
        }

        try {
          // Vykonanie JavaScriptového kódu pre graf
          const script = new Function("Chart", "document", chartCode);
          script(Chart, document);

          // Uloženie novej inštancie grafu
          this.chartInstance = Chart.getChart("myChart");
          this.log("Úspešné načítanie a vykreslenie grafu.");
        } catch (error) {
          console.error("Chyba pri vykresľovaní grafu:", error);
          this.log("Chyba pri vykresľovaní grafu.");
        }
      });
    })
    .catch((error) => {
      // Logovanie chyby
      console.error("Chyba pri volaní API pre graf:", error);
      if (error.response && error.response.data) {
        this.log("JSON odpovede v prípade chyby:");
        console.log(error.response.data);
      }
      this.log("Chyba pri volaní API pre graf.");
      this.loadingChart = false; // Ukončenie načítavania pri chybe
    });
},

    handleButtonClick() {
      alert("Tlačidlo bolo kliknuté!");
    },
  },
  mounted() {
    this.log("Komponent bol načítaný.");
    this.fetchInfo(); // Načítanie informácií pri načítaní komponentu
    this.renderChart(); // Vykreslenie grafu pri načítaní komponentu
  },
};
</script>


<style>
/* Globálne štýly */
body {
  background: url("~@/assets/back.jpg") no-repeat center center fixed;
  background-size: cover;
  margin: 0;
  padding: 0;
  height: 100vh;
}

/* Horný panel */
.top-bar {
  width: 100%;
  height: 60px;
  background-color: rgb(219, 0, 123); /* Magenta Telekom */
  display: flex;
  align-items: center;
  justify-content: flex-end;
  margin: 0;
  padding: 0;
  position: fixed;
  top: 0;
  z-index: 1000;
}

/* Sekcia s promptom */
.prompt-section {
  margin-top: 80px; /* Posunutie pod horný panel */
  text-align: center;
}

.prompt-section h2 {
  color: rgb(219, 0, 123); /* Magenta Telekom */
  font-size: 1.5rem;
  margin-bottom: 10px;
}

.prompt-section input {
  width: 60%;
  padding: 10px;
  font-size: 1rem;
  border: 2px solid rgb(219, 0, 123);
  border-radius: 5px;
}

/* Hlavný obsah */
.content {
  display: flex;
  gap: 20px; /* Medzera medzi panelmi */
  height: 50%; /* 50% výšky obrazovky */
  width: 80%; /* Zmenšenie šírky na 80% */
  margin: 40px auto 0; /* Zarovnanie do stredu */
  justify-content: center; /* Zarovnanie horizontálne */
  align-items: stretch; /* Rovnaká výška pre oba panely */
}

/* Panely */
.left-panel,
.right-panel {
  flex: 1; /* Rovnaká flexibilná veľkosť */
  padding: 20px;
  background-color: #fff;
  border-radius: 15px;
  border: 2px solid rgb(219, 0, 123); /* Magentový okraj */
  overflow-y: auto;
  display: flex;
  flex-direction: column; /* Umožní správne rozloženie vnútorného obsahu */
  max-width: 45%; /* Oba panely spolu zaberajú maximálne 90% šírky */
}

.left-panel h2,
.right-panel h2 {
  color: rgb(219, 0, 123); /* Magenta Telekom */
}

/* Responzivita pre menšie obrazovky */
@media (max-width: 768px) {
  .content {
    flex-direction: column;
    width: 90%; /* Plná šírka na menších obrazovkách */
    margin: 20px 0 0;
  }

  .left-panel,
  .right-panel {
    width: 100%; /* Panely sa rozšíria na celú šírku */
    height: auto; /* Výška sa prispôsobí obsahu */
    border-radius: 0;
    border-left: none;
    border-right: none;
  }

  .left-panel {
    border-top-right-radius: 15px;
    border-top-left-radius: 15px;
    border-bottom-right-radius: 0;
    border-bottom-left-radius: 0;
  }

  .right-panel {
    border-top-right-radius: 0;
    border-top-left-radius: 0;
    border-bottom-right-radius: 15px;
    border-bottom-left-radius: 15px;
  }
}
</style>
