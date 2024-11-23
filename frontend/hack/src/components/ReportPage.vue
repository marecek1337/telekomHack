<!-- src/components/ReportPage.vue -->

<template>
    <div class="report-page">
      <h1>Report Page</h1>
      <p>Received Data:</p>
      <pre>{{ formattedData }}</pre>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ReportPage',
    data() {
      return {
        data: null,
      };
    },
    computed: {
      formattedData() {
        return JSON.stringify(this.data, null, 2);
      },
    },
    created() {
      const queryData = this.$route.query.data;
      if (queryData) {
        this.data = JSON.parse(queryData);
      } else {
        this.data = { error: 'No data received.' };
      }
    },
  };
  </script>
  
  <style scoped>
  .report-page {
    text-align: center;
    margin-top: 50px;
  }
  
  pre {
    text-align: left;
    display: inline-block;
    background-color: #f5f5f5;
    padding: 1rem;
    border-radius: 4px;
  }
  </style>
  