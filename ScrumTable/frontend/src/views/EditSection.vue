<template>
    <div class="page-edit-section">
      <div class="columns">
        <div class="column is-4 is-offset-4">
          <h1 class="title">Edytuj Sekcję</h1>
  
          <form @submit.prevent="updateSection">
            <div class="field">
              <label for="editedSectionName">Nazwa Sekcji:</label>
              <div class="control">
                <input type="text" id="editedSectionName" class="input" v-model="editedSectionName" required>          
              </div>
            </div>
  
            <div class="field">
              <div class="control">
                <button class="button is-dark submit-button" type="submit" >Zapisz Zmiany</button>
                <button class="button is-dark dark-button" @click="goBack">Powrót</button>
              </div>
            </div>
          </form>
        </div>
      </div>
      <div v-if="showNotification" class="notification-container">
          <div class="notification is-success">
            <button class="delete" @click="hideNotification"></button>
            <div class="notification-content">
              <p class="notification-message">
                Edycja udana!
                <br>
                Czy chcesz wrócić do widoku tabeli?
                <br>
              </p>
              <div class="notification-buttons">
                <button class="button is-success is-large" @click="goToTable" style="background-color: lightgreen;">Tak</button>
                <button class="button is-danger is-large" @click="hideNotification">Nie</button>
              </div>
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
      editedSectionName: '',
      sectionId: null,
      boardId: null,
      boardName: '',
      showNotification: false
      };
    },

    mounted(){
        console.log("Params:", this.$route.params);
        this.sectionId = this.$route.params.section_id;
        this.boardId = this.$route.params.board_id;
        
    },

    methods: {
        goBack() {
          // Przekierowanie użytkownika na poprzednią stronę
          this.$router.go(-1);
        },

        async updateSection() {
          try {
            const token = localStorage.getItem('token');
            
            const response0 = await axios.get(`http://127.0.0.1:8000/board/${this.boardId}/`);
            this.boardName = response0.data.name;

            const response1 = await axios.get(`http://127.0.0.1:8000/board/${this.$route.params.board_id}/`);
            this.board_id = response1.data.id;

            const response2 = await axios.put(
              `http://127.0.0.1:8000/section/${this.board_id}/update_section/${this.sectionId}/`,
              { name: this.editedSectionName, board: null},
              { headers: { Authorization: `Token ${token}` } }
            );

            console.log('Section updated:', response2.data);
            //this.$router.go(-1); // Przekierowanie użytkownika po zapisaniu zmian
            this.showNotification=true;
          } catch (error) {
            console.error('Error updating section:', error);
            console.log("Board id: ",this.board_id, this.sectionId, this.boardName);
          }
        },

        hideNotification() {
        this.showNotification = false;
        },

        goToTable() {
        this.$router.go(-1); // Przekieruj do /user-main
        setTimeout(() => {
          window.location.reload(); // Odśwież /user-main
        }, 2);
      }
    }
  }
  </script>
  
  <style scoped>
  .page-edit-section {
    margin-top: 50px; 
  }
  
  .title {
    text-align: center; 
  }
  
  .submit-button {
   background-color: #95da8f;
   color:black;
  }

  .submit-button:hover {
   background-color: #669762;
  }

  .dark-button {
    background-color: #f55656 !important;
    margin-left: 320px;
    padding-left: 35px;
    padding-right: 35px;
  }
  
  .dark-button:hover {
    background-color: #923232 !important;
  }

  .notification-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.notification {
  max-width: 400px;
  padding: 20px;
}

.notification-content {
  text-align: center;
}

.notification-message {
  margin-bottom: 20px;
  font-size: 20px;
}

.notification-buttons {
  display: flex;
  justify-content: center;
}

.notification-buttons .button {
  margin: 0 10px;
}
  </style>
  