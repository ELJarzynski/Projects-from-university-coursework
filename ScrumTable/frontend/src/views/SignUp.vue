<template>
  <div class="page-sign-up">
    <div class="columns">
      <div class="column is-4 is-offset-4">
        <h1 class="title">Zarejestruj się</h1>

        <form @submit.prevent="register">
          <div class="field">
            <label for="email">E-mail</label>
            <div class="control">
              <input type="email" class="input" v-model="registerForm.email" required>
            </div>
          </div>

          <div class="field">
            <label for="first_name">Imię</label>
            <div class="control">
              <input type="text" class="input" v-model="registerForm.first_name" required>
            </div>
          </div>
                  
          <div class="field">
            <label for="last_name">Nazwisko</label>
            <div class="control">
              <input type="text" class="input" v-model="registerForm.last_name" required>
            </div>
          </div>

          <div class="field">
            <label for="password">Hasło</label>
            <div class="control">
              <input type="password" class="input" id="password" v-model="registerForm.password" required>
              <a @click="passwordType(passwordText)" type="button" class="mdi mdi-eye-outline"></a>
            </div>
          </div>

          <div class="field">
            <div class="control">
              <router-link to="/user-main" class="button is-dark" @click="register">Zarejestruj</router-link>
            </div>
          </div>

          <hr>

          Masz już konto?  <router-link to="/log-in">Kliknij tutaj</router-link> żeby się zalogować!
        </form>
      </div>
    </div>

    <div v-if="showNotification" class="notification-container">
      <div class="notification is-success">
        <button class="delete" @click="hideNotification"></button>
        Rejestracja udana! <i class="fas fa-check-circle"></i>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import router from '@/router';

export default {
  data() {
    return {
      registerForm: {
        email: '',
        first_name: '',
        last_name: '',
        password: ''
      },
      showNotification: false
    };
  },
  methods: {
    async register() {
      this.errors = [];

      if (!this.errors.length) {
        try {
          const response = await axios.post('http://127.0.0.1:8000/user/create/', this.registerForm);
          console.log(response.data);
          this.showNotification = true;
          await this.loginAfterRegistration(response.data.token);
          this.clearForm();
          window.location.reload();

        } catch (error) {
          console.error('Registration error:', error.response.data);
        }
      }
    },
    async loginAfterRegistration(token) {
      try {
        const loginResponse = await axios.post('http://127.0.0.1:8000/user/token/', {
          email: this.registerForm.email,
          password: this.registerForm.password
        });

        const authToken = loginResponse.data.token;
        localStorage.setItem('token', authToken);
        this.$router.push('/user-main');
      } catch (error) {
        console.error('Login error after registration:', error.response.data);
      }
    },
    clearForm() {
      this.registerForm.email = '';
      this.registerForm.first_name = '';
      this.registerForm.last_name = '';
      this.registerForm.password = '';
    },
    passwordType() {
    },
    hideNotification() {
      this.showNotification = false;
    },
  }
};
</script>
