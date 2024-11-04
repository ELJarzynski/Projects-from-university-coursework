<template>
  <div class="page-log-in">
    <div class="columns">
      <div class="column is-4 is-offset-4">
        <h1 class="title">Zaloguj się</h1>

        <form @submit.prevent="login">
          <div class="field">
            <label for="loginEmail">Email:</label>
            <div class="control">
              <input type="email" id="loginEmail" class="input" v-model="loginForm.email" required>
            </div>
          </div>

          <div class="field">
            <label for="loginPassword">Hasło:</label>
            <div class="control">
              <input type="password" id="loginPassword" class="input" v-model="loginForm.password" required>
            </div>
          </div>

          <div class="field">
            <div class="control">
              <button class="button is-dark" type="submit">Zaloguj</button>
            </div>
          </div>

          Lub <router-link to="/sign-up">kliknij tutaj</router-link> żeby sę zarejestrować!
        </form>
      </div>
    </div>

    <div v-if="showSuccessNotification" class="notification-container">
      <div class="notification is-success">
        <button class="delete" @click="hideNotification"></button>
        <div class="notification-content">
          <p class="notification-message">
            Logowanie udane!
            <br>
            Czy chcesz przejść do panelu użytkownika?
            <br>
          </p>
          <div class="notification-buttons">
            <button class="button is-success is-large" @click="goToUserPanel" style="background-color: lightgreen;">Tak</button>
            <button class="button is-danger is-large" @click="hideNotification">Nie</button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showErrorNotification" class="notification-container">
      <div class="notification is-danger">
        <button class="delete" @click="hideNotification"></button>
        <div class="notification-content">
          <p class="notification-message">
            Błąd logowania!
            <br>
            Sprawdź swoje dane i spróbuj ponownie.
            <br>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import axios from 'axios';

export default {
  data() {
    return {
      loginForm: {
        email: '',
        password: ''
      },
      showSuccessNotification: false,
      showErrorNotification: false
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('http://127.0.0.1:8000/user/token/', this.loginForm);
        
        const token = response.data.token;
        localStorage.setItem('token', token); // Zapisz token w localStorage
        console.log('Login successful');
        console.log(token);

        this.showSuccessNotification = true;
      } catch (error) {
        console.error('Login error:', error.response.data);
        this.showErrorNotification = true;
      }
    },
    hideNotification() {
      this.showSuccessNotification = false;
      this.showErrorNotification = false;
      this.$router.push('/log-in');
    },
    goToUserPanel() {
      this.$router.push('/user-main'); // Przekieruj do /user-main
      setTimeout(() => {
        window.location.reload(); // Odśwież /user-main
      }, 2);
    }
  }
};
</script>

<style scoped src="../../style/Login.css"></style>
