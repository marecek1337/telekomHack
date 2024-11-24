<template>
  <div class="register-container">
    <h2>Register</h2>
    <form @submit.prevent="registerUser">
      <div>
        <label for="username">Username</label>
        <input type="text" v-model="username" id="username" required />
      </div>

      <div>
        <label for="password">Password</label>
        <input type="password" v-model="password" id="password" required />
      </div>

      <div>
        <label for="email">Email</label>
        <input type="email" v-model="email" id="email" />
      </div>

      <button type="submit">Register</button>
    </form>

    <div v-if="successMessage" class="success">{{ successMessage }}</div>
    <div v-if="errorMessage" class="error">{{ errorMessage }}</div>

    <p class="login-redirect">
      Already have an account? 
      <button @click="redirectToLogin">Log in</button>
    </p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "UserRegister",
  data() {
    return {
      username: "",
      password: "",
      email: "",
      successMessage: "",
      errorMessage: "",
    };
  },
  methods: {
    async registerUser() {
      try {
        const response = await axios.post("http://localhost:8000/register/", {
          username: this.username,
          password: this.password,
          email: this.email,
        });

        // Show success message
        this.successMessage = "User registered successfully! Redirecting to login...";
        this.errorMessage = "";

        // Clear the form fields
        this.username = "";
        this.password = "";
        this.email = "";

        console.log("User registered:", response.data);

        // Redirect to the login page after 2 seconds
        setTimeout(() => {
          this.$router.push({ name: "Login" });
        }, 2000);
      } catch (error) {
        console.error("Error registering user:", error);
        this.successMessage = "";
        this.errorMessage = error.response?.data?.error || "Registration failed! Please try again.";
      }
    },
    redirectToLogin() {
      this.$router.push({ name: "Login" }); // Redirect to the Login page
    },
  },
};
</script>

<style scoped>
/* Styling for the registration form */
.register-container {
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
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #0056b3;
}

.success {
  color: green;
  font-size: 14px;
  margin-top: 10px;
}

.error {
  color: red;
  font-size: 14px;
  margin-top: 10px;
}

.login-redirect {
  margin-top: 15px;
}

.login-redirect button {
  background: none;
  border: none;
  color: #007bff;
  text-decoration: underline;
  cursor: pointer;
  font-size: 14px;
}

.login-redirect button:hover {
  color: #0056b3;
}
</style>
