<template>
  <div class="user-panel">
    <div class="button-container">
      <!-- Przyciski -->
      <router-link to="/tables" class="button">Moje tablice</router-link>
      <router-link to="/add-board" class="button">Stwórz nową tablicę</router-link>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      userData: null
    };
  },
  mounted() {
    this.fetchUserData();
  },
  methods: {
    async fetchUserData() {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://127.0.0.1:8000/user/profile/', this.fetchUserData)
      
      this.userData = response.data;
    } catch (error) {
      console.error('Błąd podczas pobierania danych użytkownika:', error);
    }
},

  }
};
</script>



<style scoped src="../../style/UserPanel.css"></style>