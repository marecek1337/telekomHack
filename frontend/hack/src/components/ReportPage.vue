<template>
    <div class="report-page">
      <!-- Horný panel -->
      <div class="top-bar">
        <!-- Dropdown a tlačidlo napravo -->
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
          <h2>Detaily reportu</h2>
          <p>{{ textContent }}</p>
        </div>
  
        <!-- Pravý panel -->
        <div class="right-panel">
          <h2>Graf</h2>
          <canvas id="myChart"></canvas>
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
        textContent: "",
        selectedOption: "",
      };
    },
    methods: {
      fetchData() {
        // Simulácia načítania textu z endpointu
        axios
          .get("https://baconipsum.com/api/?type=meat-and-filler")
          .then((response) => {
            this.textContent = response.data[0];
          })
          .catch((error) => {
            console.error("Chyba pri načítaní textu:", error);
            this.textContent = "Nastala chyba pri načítaní údajov.";
          });
  
        // Simulácia načítania dát pre graf
        this.renderChart();
      },
      renderChart() {
        const ctx = document.getElementById("myChart").getContext("2d");
        new Chart(ctx, {
          type: "bar",
          data: {
            labels: ["Január", "Február", "Marec", "Apríl", "Máj", "Jún"],
            datasets: [
              {
                label: "Ukážkové dáta",
                data: [12, 19, 3, 5, 2, 3],
                backgroundColor: "rgba(219, 0, 123, 0.5)", // Magenta Telekom s 50% priehľadnosťou
                borderColor: "rgba(219, 0, 123, 1)", // Magenta Telekom
                borderWidth: 1,
              },
            ],
          },
          options: {
            responsive: true,
          },
        });
      },
      handleButtonClick() {
        // Spracovanie kliknutia na tlačidlo
        alert("Tlačidlo bolo kliknuté!");
      },
    },
    mounted() {
      this.fetchData();
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
  