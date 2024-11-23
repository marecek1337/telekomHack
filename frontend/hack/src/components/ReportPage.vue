<!-- src/components/ReportPage.vue -->

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
  import axios from 'axios';
  import { Chart, registerables } from 'chart.js';
  
  Chart.register(...registerables);
  
  export default {
    name: 'ReportPage',
    data() {
      return {
        textContent: '',
        selectedOption: '',
      };
    },
    methods: {
      fetchData() {
        // Simulácia načítania textu z endpointu
        axios
          .get('https://baconipsum.com/api/?type=meat-and-filler')
          .then((response) => {
            this.textContent = response.data[0];
          })
          .catch((error) => {
            console.error('Chyba pri načítaní textu:', error);
            this.textContent = 'Nastala chyba pri načítaní údajov.';
          });
  
        // Simulácia načítania dát pre graf
        this.renderChart();
      },
      renderChart() {
        const ctx = document.getElementById('myChart').getContext('2d');
        new Chart(ctx, {
          type: 'bar',
          data: {
            labels: ['Január', 'Február', 'Marec', 'Apríl', 'Máj', 'Jún'],
            datasets: [
              {
                label: 'Ukážkové dáta',
                data: [12, 19, 3, 5, 2, 3],
                backgroundColor: 'rgba(219, 0, 123, 0.5)', // Magenta Telekom s 50% priehľadnosťou
                borderColor: 'rgba(219, 0, 123, 1)', // Magenta Telekom
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
        alert('Tlačidlo bolo kliknuté!');
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
    background: url('~@/assets/back.jpg') no-repeat center center fixed;
    background-size: cover;
    margin: 0;
    height: 100vh;
  }
  
  /* Horný panel */
  .top-bar {
    width: 100%;
    height: 60px;
    background-color: rgb(219, 0, 123); /* Magenta Telekom */
    display: flex;
    align-items: center;
    justify-content: flex-end; /* Prvky zarovnané vpravo */
  }
  
  /* Pravá strana horného panela */
  .top-bar-right {
    display: flex;
    align-items: center;
    margin-right: 20px;
  }
  
  .top-bar-right select,
  .top-bar-right button {
    margin-left: 10px;
    padding: 5px 10px;
    font-size: 14px;
  }
  
  /* Hlavný obsah */
  .content {
    display: flex;
    gap: 20px; /* Medzera medzi panelmi */
    height: calc(100vh - 80px); /* Výška okna mínus výška horného panela a margin */
    width: 90%; /* Zmenšenie celkovej šírky */
    margin: 20px auto 0; /* Pridanie horného marginu medzi horný panel a obsah */
  }
  
  /* Ľavý panel */
  .left-panel {
    flex: 1; /* Relatívna veľkosť */
    padding: 20px;
    background-color: #fff;
    border-radius: 15px; /* Oblé rohy na všetkých stranách */
    border: 2px solid rgb(219, 0, 123); /* Magentový okraj */
    overflow-y: auto;
  }
  
  /* Pravý panel */
  .right-panel {
    flex: 3; /* Relatívna veľkosť */
    padding: 20px;
    background-color: #fff;
    border-radius: 15px; /* Oblé rohy na všetkých stranách */
    border: 2px solid rgb(219, 0, 123); /* Magentový okraj */
    overflow-y: auto;
  }
  
  .left-panel h2,
  .right-panel h2 {
    color: rgb(219, 0, 123); /* Magenta Telekom */
  }
  
  .report-page {
    display: flex;
    flex-direction: column;
  }
  
  @media (max-width: 768px) {
    .content {
      flex-direction: column;
      width: 100%; /* Plná šírka na menších obrazovkách */
      margin: 20px 0 0; /* Upravený margin */
    }
  
    .left-panel,
    .right-panel {
      width: 100%;
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
  