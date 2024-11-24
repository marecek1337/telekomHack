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
        "├── T-Systems",
        "│   ├── hardware",
        "│   │   ├── memory.csv",
        "│   │   ├── peripherals.csv",
        "│   │   ├── processors.csv",
        "│   │   └── storage.csv",
        "│   ├── hr",
        "│   │   ├── benefits.csv",
        "│   │   ├── payroll.csv",
        "│   │   └── recruitment.csv",
        "│   ├── management",
        "│   │   ├── meetings.csv",
        "│   │   ├── policies.csv",
        "│   │   └── reports.csv",
        "│   ├── notebooks",
        "│   │   ├── dell.csv",
        "│   │   ├── hp.csv",
        "│   │   └── lenovo.csv",
        "│   ├── pcs",
        "│   │   ├── desktop",
        "│   │   │   ├── dell.csv",
        "│   │   │   └── hp.csv",
        "│   │   └── laptops",
        "│   │       ├── macbook.csv",
        "│   │       └── surface.csv",
        "│   ├── people",
        "│   │   ├── contractors",
        "│   │   │   ├── it.csv",
        "│   │   │   └── marketing.csv",
        "│   │   └── employees",
        "│   │       ├── engineering.csv",
        "│   │       ├── hr.csv",
        "│   │       └── sales.csv",
        "│   ├── projects",
        "│   │   ├── active.csv",
        "│   │   └── archived.csv",
        "│   └── software",
        "│       ├── applications.csv",
        "│       ├── licenses.csv",
        "│       └── operating_systems.csv",
        "├── people",
        "│   └── time_series_covid19_deaths_global.csv"
      ],
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
    this.log("Starting to display tree structure...");
    // Spúšťanie riadkov po jednom
    this.interval = setInterval(() => {
      if (this.currentLineIndex < this.lines.length - 1) {
        this.currentLineIndex++;
        this.log(`Displayed line: ${this.lines[this.currentLineIndex]}`);
      } else {
        clearInterval(this.interval);
      }
    }, 200); // Skrátenie intervalu na rýchlejšie zobrazovanie

    // Presmerovanie na /report po 5 sekundách
    setTimeout(() => {
      this.log("Redirecting to report...");
      this.$router.push("/report");
    }, 5000); // Skrátenie presmerovania
  },
  beforeUnmount() {
    clearInterval(this.interval);
  },
  methods: {
    log(message) {
      console.log(`[LOG] ${new Date().toISOString()}: ${message}`);
    },
  },
};
</script>
