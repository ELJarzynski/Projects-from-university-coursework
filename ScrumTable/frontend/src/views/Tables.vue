<template>

  <div class="page-board">
    <div class="columns is-multiline">
      <div class="column is-12">
        <h1 class="title">Boards</h1>
      </div>
      <div class="column is-12 box">
        <table class="table is-fullwidth" v-if="boardTotalLength">
          <thead>
            <tr>
              <th>Name</th>
              <th>Description</th>
              <th>Create Date</th>
              <th>Due Date</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="board in boards" :key="board.id">
              <td>{{ board.name }}</td>
              <td>{{ board.description }}</td>
              <td>{{ board.create_date }}</td>
              <td>{{ board.due_date }}</td>
              <td>
                <button @click="deleteBoard(board.id)" class="button is-danger is-margin-right" style="margin-right: 10px;">Delete</button>
                <button @click="openEditBoardModal(board)" class="button is-info is-margin-right" style="margin-right: 10px;">Edit</button>
                <button @click="openBoard(board.id)" class="button is-primary is-margin-right" style="margin-right: 10px;">Open</button>
                <span @click="openUserModal(board.id)" style="cursor: pointer;" >
                  <i class="fas fa-users"></i> {{ getBoardUserCount(board.id) }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
        <p v-else>You don't have any boards...</p>
      </div>
    </div>

    <!-- Modal do usuwania tablicy -->
    <transition name="fadeIn">
      <div v-if="deleteBoardModalVisible" class="modal-delete">
        <div class="modal-content-delete">
          <h2 style="margin-bottom: 15px; font-weight: bold; font-size: 30px;">Delete Board</h2>
          <p>Are you sure you want to delete this board?</p>
          <div class="buttons">
            <button @click="confirmDeleteBoard" class="button is-danger is-margin-right">Yes</button>
            <button @click="cancelDeleteBoard" class="button is-primary">No</button>
          </div>
        </div>
      </div>
    </transition>

    <!-- Modal do edycji tablicy -->
    <transition name="fadeIn">
      <div v-if="editBoardModalVisible" class="modal-edit">
        <div class="modal-content-edit">
          <span class="close-edit" @click="closeEditBoardModal">&times;</span>
          <h2 style="margin-bottom: 15px; font-weight: bold; font-size: 30px;">Edit Board</h2>
          <form @submit.prevent="updateBoard">
            <div class="form-group" style="margin-bottom: 15px; font-weight: bold; font-size: 15px;">
              <label for="editBoardName" style="margin-right: 15px;" >Board Name:</label>
              <input type="text" id="editBoardName" v-model="editedBoardName" class="form-control">
            </div>
            <div class="form-group" style="margin-bottom: 15px; font-weight: bold; font-size: 15px;">
              <label for="editBoardDescription" style="margin-right: 15px;">Description:</label>
              <textarea type="description" id="editBoardDescription" v-model="editedBoardDescription" class="form-control textarea-description"></textarea>
            </div>
            <div class="form-group" style="margin-bottom: 15px; font-weight: bold; font-size: 15px;">
              <label for="editBoardDueDate" style="margin-right: 15px;">Due Date:</label>
              <input type="date" id="editBoardDueDate" v-model="editedBoardDueDate" class="form-control">
            </div>
            <button type="submit" class="button is-primary">Update Board</button>
          </form>
        </div>
      </div>
    </transition>

     <!-- Modal for User List -->
    <div class="modal" :class="{ 'is-active': userModalActive }">
      <div class="modal-background" @click="closeUserModal"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">User List</p>
          <button class="delete" aria-label="close" @click="closeUserModal"></button>
        </header>
        <section class="modal-card-body">
          <ul>
            <li v-for="user in currentUserList" :key="user.user_detail.id" style="color: white; margin-bottom: 10px;">
              ID: {{ user.user_detail.id }} | Email: {{ user.user_detail.email }}
              <button @click="openRemoveUserModal(currentBoardId, user)" class="button is-danger is-small">Remove</button>
            </li>
          </ul>
        </section>
        <footer class="modal-card-foot">
          <button class="button is-success" @click="openAddUserModal">Add User</button>
          <button class="button" @click="closeUserModal">Cancel</button>
        </footer>
      </div>
    </div>

    <!-- Modal for adding a new user -->
    <div class="modal" :class="{ 'is-active': addUserModalActive }">
      <div class="modal-background" @click="closeAddUserModal"></div>
        <div class="modal-content">
          <div class="box">
          <h2 class="subtitle">Add User to Board</h2>
          <div class="field">
            <label class="label">User Email</label>
            <div class="control">
              <input class="input" type="text" v-model="newUserEmail" placeholder="Enter user email">
            </div>
          </div>
          <div class="field">
            <button class="button is-success" @click="findAndAddUser">Add User</button>
            <button class="button" @click="closeAddUserModal">Cancel</button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Modal for confirming user removal -->
  <div class="modal" :class="{ 'is-active': confirmRemoveModalActive }">
    <div class="modal-background" @click="cancelRemoveUser"></div>
    <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">Confirmation</p>
        <button class="delete" aria-label="close" @click="cancelRemoveUser"></button>
      </header>
      <section class="modal-card-body">
        Are you sure you want to remove this user from the board?
      </section>
      <footer class="modal-card-foot">
        <button class="button is-danger" @click="removeUserFromBoard(currentBoardId, user)">Yes</button>
        <button class="button" @click="cancelRemoveUser">No</button>
      </footer>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      editedBoardName: '',
      editedBoardId: null,
      editBoardModalVisible: false,
      editedBoardDescription: '',
      editedBoardDueDate: '',
      boards: [],
      boardUserCounts: {},
      userModalActive: false,
      currentUserList: [],
      currentBoardId: null,
      userId: null,
      newUserId: '',
      addUserModalActive: false,
      newUserEmail: '',
      deleteBoardModalVisible: false,
      boardToDeleteId: null,
      confirmRemoveModalActive: false,
      removeUserId: null,
    };
  },

  mounted() {
    this.fetchBoards();
  },

  methods: {
    // -------------------- FETCHE --------------------
    async fetchBoards() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/board/list_board/');
        this.boards = response.data;

        // Po pobraniu listy tablic, dla każdej tablicy pobierz liczbę użytkowników
        for (const board of this.boards) {
          await this.fetchBoardUsers(board.id);
        }
      } catch (error) {
        console.error('Error fetching boards:', error);
      }
    },

    async fetchBoardUsers(boardId) {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/board/${boardId}/users/`);
        this.boardUserCounts[boardId] = response.data.length;
      } catch (error) {
        console.error('Error fetching board users:', error);
      }
    },

    async fetchBoardUsersList(boardId) {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/board/${boardId}/users/`);
        this.currentUserList = response.data;
        console.log('Current User List:', this.currentUserList); // Dodaj to logowanie
        // Przypisz pierwszego użytkownika z listy jako aktualnie wybranego użytkownika
        if (response.data.length > 0) {
          this.userId = response.data[0].user_id;
        }
      } catch (error) {
        console.error('Error fetching board users:', error);
      }
    },

    // -------------------- BOARDS --------------------
    // Update
    async updateBoard() {
      try {
        await axios.put(`http://127.0.0.1:8000/board/${this.editedBoardId}/edit_board/`, 
          { name: this.editedBoardName,
          description: this.editedBoardDescription,
          due_date: this.editedBoardDueDate }
        );
        console.log('Board updated successfully');
        this.closeEditBoardModal();
        this.fetchBoards();
      } catch (error) {
        console.error('Error updating board:', error);
      }
    },

    // Delete
    async deleteBoard(boardId) {
      try {
        this.deleteBoardModalVisible = true;
        this.boardToDeleteId = boardId;
      } catch (error) {
        console.error('Error deleting board:', error);
      } 
    },

    async confirmDeleteBoard() {
      try {
        await axios.delete(`http://127.0.0.1:8000/board/${this.boardToDeleteId}/delete_board/`);
        this.fetchBoards();
        this.closeDeleteBoardModal();
      } catch (error) {
        console.error('Error confirming deletion of board:', error);
      }
    },

    cancelDeleteBoard() {
      this.closeDeleteBoardModal();
    },

    closeDeleteBoardModal() {
      this.deleteBoardModalVisible = false;
      this.boardToDeleteId = null;
    },


    // Przekierowanie do widoku Sekcji
    openBoard(boardId) {
      this.$router.push(`/section-table/${boardId}/create_section`);
    },

    // Edit Board
    openEditBoardModal(board) {
      this.editBoardModalVisible = true;
      this.editedBoardId = board.id;
      this.editedBoardName = board.name;
      this.editedBoardDescription = board.description;
      this.editedBoardDueDate = board.due_date;
    },

    closeEditBoardModal() {
      this.editBoardModalVisible = false;
    },


    // ------------------------ USER ------------------------
    // Add User
    async findAndAddUser() {
  try {
    console.log('Searching for user with email:', this.newUserEmail); // Debugging log
    // Wyszukanie użytkownika na podstawie adresu e-mail
    const response = await axios.get(`http://127.0.0.1:8000/user/find/?email=${this.newUserEmail}`);
    console.log('Response data:', response.data); // Debugging log
    if (response.data.id) {
      const userId = response.data.id;

      // Dodanie użytkownika do zadania za pomocą ID
      await this.addUserToTask(userId);

      // Czyszczenie pola adresu e-mail po dodaniu użytkownika
      this.newUserEmail = '';
    } else {
      console.log('No user found with the provided email.');
    }
  } catch (error) {
    console.error('Error finding and adding user:', error);
  }
},


    async addUserToBoard(userId) {
      try {
        const boardId = this.currentBoardId;

        // Dodanie użytkownika do tablicy za pomocą ID
        await axios.post(`http://127.0.0.1:8000/board/${boardId}/add_user/`, { user: userId });

        // Pobranie zaktualizowanej listy użytkowników po dodaniu nowego
        await this.fetchBoardUsersList(boardId);

        // Odświeżenie listy tablic
        this.fetchBoards();

        // Zamknięcie modala po dodaniu użytkownika
        this.closeAddUserModal();
      } catch (error) {
        console.error('Error adding user to board:', error);
      }
    },

    // Delete
   async deleteUserFromBoard(boardId, user) {
      try {
        console.log("User:", user); // Dodajmy to logowanie
        //const userId = user.user_detail.id; // Pobierz user_id z obiektu user
        // Wykonanie zapytania HTTP do usunięcia użytkownika z tablicy
        await axios.delete(`http://127.0.0.1:8000/board/${boardId}/delete_user/${this.removeUserId}`);

        // Pobranie zaktualizowanej listy użytkowników po usunięciu
        await this.fetchBoardUsersList(boardId);
        window.location.reload();
      } catch (error) {
        console.error('Error deleting user from board:', error);
      }
    },

    async removeUserFromBoard(boardId, user) {
      console.log("User:", user); // Sprawdźmy, co jest w obiekcie user
      
      await this.deleteUserFromBoard(boardId, this.removeUserId);
    },

    // zliczanie ilosci ziutków przypisanych do tablicy
    getBoardUserCount(boardId) {
      return this.boardUserCounts[boardId] || 0;
    },

    // Wyswietlanie Userów
    openUserModal(boardId) {
      this.userModalActive = true;
      this.currentBoardId = boardId;
      this.fetchBoardUsersList(boardId); // Dodaj to wywołanie, aby pobrać użytkowników tablicy
    },

    closeUserModal() {
      this.userModalActive = false;
      this.currentBoardId = null;
      this.currentUserList = [];
    },

    // Dodawanie Userów
    openAddUserModal() {
      this.addUserModalActive = true;
    },

    closeAddUserModal() {
      this.addUserModalActive = false;
      this.newUserId = ''; 
    },

    //Usuwanie userów
    openRemoveUserModal(boardId, user){
      this.confirmRemoveModalActive = true;
      this.currentBoardId = boardId;
      this.removeUserId = user.user_detail.id;
    },

    cancelRemoveUser(){
      this.confirmRemoveModalActive = false;
    },
  },

  computed: {
    boardTotalLength() {
      return this.boards.length;
    }
  }
};
</script>

<style>
.modal-edit {
    display: flex;
    align-items: center;
    justify-content: center;
    position: fixed;
    z-index: 1000;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    overflow: auto;
  }
  
  .modal-content-edit {
    margin: auto;
    padding: 20px;
    width: 50%; /* zmieniamy szerokość modalu edycji */
    max-height: 80%; /* maksymalna wysokość modalu */
    overflow-y: auto; /* dodajemy pionowy scroll w przypadku długich treści */
    background-color: #d4d4d6; /* Zaktualizowany kolor tła */
    border-radius: 5px;
    border: 5px solid #007bff; /* Zaktualizowany kolor ramki */
    text-align: center;
    color: #000;
    opacity: 0.9;
  }
  
  .close-edit {
    color: #aaaaaa;
    float: right;
    font-size: 28px;
    font-weight: bold;
  }
  
  .close-edit:hover,
  .close-edit:focus {
    color: #000;
    text-decoration: none;
    cursor: pointer;
  }
  /* User */
  .modal {
    display: none;
    position: fixed;
    z-index: 1000;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    overflow: auto;
    
  }
  .modal-card-body {
    color: white;
  }

.modal-delete {
  display: flex;
  align-items: center;
  justify-content: center;
  position: fixed;
  z-index: 1000;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); /* Półprzezroczyste tło */
  overflow: auto;
}

.modal-content-delete {
  margin: auto;
  padding: 20px;
  width: 50%; /* Szerokość modalu */
  max-height: 80%; /* Maksymalna wysokość modalu */
  overflow-y: auto; /* Pionowy scroll w przypadku długich treści */
  background-color: #f38b8b; /* Tło modalu */
  border-radius: 5px;
  border: 5px solid #491010; /* Kolor ramki */
  text-align: center;
  color: #000;
  opacity: 0.9;
}

.buttons {
  display: flex;
  justify-content: center; /* Wyśrodkowanie guzików wzdłuż osi poziomej */
}

.buttons .button {
  margin: 0 5px; /* Dodatkowy odstęp między guzikami */
  margin-top: 15px;
}


@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px); /* Przesunięcie o -20px w górę */
  }
  to {
    opacity: 0.9;
    transform: translateY(0); /* Bez przesunięcia */
  }
}
  </style>
