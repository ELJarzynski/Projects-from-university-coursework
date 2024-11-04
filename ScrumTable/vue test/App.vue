<template>
  <div>
    <h2>Rejestracja</h2>
    <form @submit.prevent="register">
      <label for="email">Email:</label>
      <input type="email" id="email" v-model="registerForm.email" required>
      <label for="first_name">Imie:</label>
      <input type="text" id="first_name" v-model="registerForm.first_name" required>
      <label for="last_name">Nazwisko:</label>
      <input type="text" id="last_name" v-model="registerForm.last_name" required>
      <label for="password">Hasło:</label>
      <input type="password" id="password" v-model="registerForm.password" required>
      <button type="submit">Zarejestruj</button>
    </form>
    <h2>Logowanie</h2>
    <form @submit.prevent="login">
      <label for="loginEmail">Email:</label>
      <input type="email" id="loginEmail" v-model="loginForm.email" required>
      <label for="loginPassword">Hasło:</label>
      <input type="password" id="loginPassword" v-model="loginForm.password" required>
      <button type="submit">Zaloguj</button>
    </form>
    <h2>Utwórz nową tablicę</h2>
    <form @submit.prevent="createBoard">
      <label for="boardName">Nazwa tablicy:</label>
      <input type="text" id="boardName" v-model="boardcreateForm.boardName" required>
      <label for="boardDescription">Opis:</label>
      <textarea id="boardDescription" v-model="boardcreateForm.description"></textarea>
      <label for="dueDate">Data końcowa:</label>
      <input type="date" id="dueDate" v-model="boardcreateForm.due_date" required>
      <button type="submit">Utwórz</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      registerForm: {
        email: '',
        first_name: '',
        last_name: '',
        password: ''
      },
      loginForm: {
        email: '',
        password: ''
      },
      boardcreateForm: {
        name: '',
        description: '',
        due_date: ''
      }
    };
  },
  methods: {
    async register() {
      try {
        const response = await axios.post('http://127.0.0.1:8000/user/create/', this.registerForm);
        console.log(response.data); // Optional: Handle successful registration response
      } catch (error) {
        console.error('Registration error:', error.response.data);
      }
    },
    async login() {
      try {
        const response = await axios.post('http://127.0.0.1:8000/user/token/', this.loginForm);
        //console.log(response.data); // Optional: Handle successful login response
        // Assuming you will handle authentication token and redirect user after successful login
        const token = response.data.token;
        localStorage.setItem('token', token); // Zapisz token w localStorage
        console.log('Login successful');
      } catch (error) {
        console.error('Login error:', error.response.data);
      }
    },
    async createBoard() {
      try {
        console.log(localStorage.getItem('token'))
        const response = await axios.post('http://127.0.0.1:8000/board/create_board/', {
          name: this.boardcreateForm.boardName,
          description: this.boardcreateForm.description,
          due_date: this.boardcreateForm.due_date
        }, {
          headers: {
            Authorization:`Token ${localStorage.getItem('token')}`,
            "Content-Type": "application/json",
          }
        });
        console.log(response.data); // Optional: Handle successful board creation response
        // Redirect user or perform other actions after successful board creation
      } catch (error) {
        console.error('Board creation error:', error.response ? error.response.data : error.message);
      }
    }
  }
};
</script>
