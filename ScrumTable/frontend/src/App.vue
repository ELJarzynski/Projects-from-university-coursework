<template>
  <div id="app">
    <nav class="navbar is-dark">
      <div class="navbar-brand">
        <router-link to="/" class="navbar-item" ><strong>Dziarski scrum</strong></router-link>
      </div>

       <div class="navbar-end">
          <div class="navbar-item">
            <div class="buttons">
              <template v-if="$store.state.isAuthenticated">
                <span v-if="user">{{ user.first_name }} {{ user.last_name }}</span>
                <router-link to="/user-main" class="button-app is-light">Panel użytkownika</router-link>
                <button @click="logout" class="button-app is-light">Wyloguj</button>
              </template>

              <template v-else>
                <router-link to="/log-in" class="button-app is-light login-button"><i class="fas fa-sign-in-alt" style="color: black;"></i>Zaloguj</router-link>
              <router-link to="/sign-up" class="button-app is-light signup-button"><i class="fas fa-user-plus" style="color: black;"></i> Zarejestruj</router-link>
              </template>
          </div>
          </div>
        </div> 
    </nav>

    <section class="section">
      <router-view/>
    </section>

    <footer class="footer">
      <p class="has-text-centered">Visimind</p>
    </footer>
  </div>
</template>


<script>
import axios from 'axios'

export default {
  data() {
    return {
      showMobileMenu: false,
      cart: {
        items: []
      },
      refreshPage() {
        window.location.reload();
    },
      user: null // Dodaj pole user do danych komponentu
    }
  },
  beforeCreate() {
    this.$store.commit('initializeStore')

    const token = this.$store.state.token

    if (token) {
        axios.defaults.headers.common['Authorization'] = "Token " + token
    } else {
        axios.defaults.headers.common['Authorization'] = ""
    }
  },
  mounted() {
    this.cart = this.$store.state.cart
    this.fetchUserData(); // Wywołaj metodę fetchUserData po zamontowaniu komponentu
  },
  methods: {
    logout() {
      localStorage.removeItem('token');
      this.$router.push('/');
      setTimeout(() => {
        window.location.reload(); // Odśwież /log-in
      }, 2);
    },
    async fetchUserData() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/user/profile/');
        this.user = response.data;
      } catch (error) {
        console.error('Błąd podczas pobierania danych użytkownika:', error);
      }
    }
  },
  
  computed: {
      cartTotalLength() {
          let totalLength = 0

          for (let i = 0; i < this.cart.items.length; i++) {
              totalLength += this.cart.items[i].quantity
          }

          return totalLength
      }
  }
}
</script>


<style lang="scss">
@import '../node_modules/bulma';

.lds-dual-ring {
  display: inline-block;
  width: 80px;
  height: 80px;
}
.lds-dual-ring:after {
  content: " ";
  display: block;
  width: 64px;
  height: 64px;
  margin: 8px;
  border-radius: 50%;
  border: 6px solid #ccc;
  border-color: #ccc transparent #ccc transparent;
  animation: lds-dual-ring 1.2s linear infinite;
}
@keyframes lds-dual-ring {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.is-loading-bar {
  height: 0;
  overflow: hidden;

  -webkit-transition: all 0.3s;
  transition: all 0.3s;

  &.is-loading {
    height: 80px;
  }
}

.button-app {
  margin-left: 10px; /* Odstęp między przyciskami */
  padding: 10px 20px;
  font-size: 1em;
  text-decoration: none;
  color: black;
  background-color: white;
  border: 1px solid white; /* Dodanie białej ramki */
  border-radius: 5px;
}

.button-app i {
  margin-right: 5px;
}

.login-button,
.signup-button {
  font-family: inherit; /* Ustawienie dziedziczenia czcionki */
}
</style>