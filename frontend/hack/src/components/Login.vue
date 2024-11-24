<template>
    <div class="login-container">
      <h2>Login</h2>
      <form @submit.prevent="loginUser">
        <div>
          <label for="username">Username</label>
          <input type="text" v-model="username" id="username" required />
        </div>
  
        <div>
          <label for="password">Password</label>
          <input type="password" v-model="password" id="password" required />
        </div>
  
        <button type="submit">Login</button>
      </form>
  
      <!-- Create Account Button -->
      <div class="create-account">
        <p>Don't have an account?</p>
        <button @click="redirectToRegister">Create Account</button>
      </div>
  
      <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  export default {
  name: "UserLogin", // Updated to a multi-word name
  data() {
    return {
      username: "",
      password: "",
      errorMessage: "",
    };
  },
  methods: {
    async loginUser() {
      try {
        const response = await axios.post("http://localhost:8000/token/", {
          username: this.username,
          password: this.password,
        });

        if (response.data.access && response.data.refresh) {
          localStorage.setItem("access_token", response.data.access);
          localStorage.setItem("refresh_token", response.data.refresh);
          this.$router.push({ name: "Home" });
        }
      } catch (error) {
        console.error("Error logging in:", error);
        this.errorMessage = "Invalid username or password!";
      }
    },
    redirectToRegister() {
      this.$router.push({ name: "Register" });
    },
  },
};

  </script>
  
  <style scoped>
  /* Styling the login form */
  .login-container {
    max-width: 400px;
    margin: 50px auto;
    padding: 20px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    background-color: #f9f9f9;
    border-radius: 10px;
    font-family: Arial, sans-serif;
    text-align: center;
  }
  
  h2 {
    font-size: 24px;
    margin-bottom: 20px;
  }
  
  form {
    display: flex;
    flex-direction: column;
    gap: 15px;
  }
  
  label {
    font-size: 14px;
    font-weight: bold;
    text-align: left;
  }
  
  input {
    width: 100%;
    padding: 10px;
    margin: 5px 0;
    border: 1px solid #ccc;
    border-radius: 5px;
    font-size: 14px;
    box-sizing: border-box;
  }
  
  button {
    padding: 10px;
    background-color: #4caf50;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    font-weight: bold;
    transition: background-color 0.3s ease;
  }
  
  button:hover {
    background-color: #45a049;
  }
  
  .create-account {
    margin-top: 20px;
  }
  
  .create-account p {
    margin: 0;
    font-size: 14px;
  }
  
  .create-account button {
    padding: 10px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 14px;
    font-weight: bold;
    transition: background-color 0.3s ease;
  }
  
  .create-account button:hover {
    background-color: #0056b3;
  }
  
  .error {
    color: red;
    font-size: 14px;
    margin-top: 10px;
  }
  </style>
  