<template>
  <div class="page-section-table">
      <div class="columns is-multiline">
        <div class="column is-12">
          <h1 class="title">Sekcje</h1>
        </div>
        <div class="info-container">
          <button @click="toggleInfoPanel" class="info-button">Informacje o tablicy</button>
          <div :class="['info-panel', { 'info-panel--visible': infoPanelVisible }]">

          <h2 class="subtitle">Informacje o tablicy</h2>
          <p><strong>Opis:</strong> {{ boardDescription }}</p>
          <p><strong>Data utworzenia:</strong> {{ boardCreateDate }}</p>
          <p><strong>Termin:</strong> {{ boardDueDate }}</p>
          <h2 class="subtitle" style="margin-top: 20px;">Użytkownicy przypisani do tablicy:</h2>
          <ul>
            <li v-for="user in boardUsers" :key="user.id">
              {{ user.user_detail.email }}
            </li>
          </ul>
        </div>
    </div>
      </div>
    </div>
    <div class="section-table-container">
     <!-- Nagłówek tabeli z nazwą tablicy -->
     <h1 class="board-title">Sekcja dla tablicy: {{ boardName }}</h1>
     <!-- Kontener sekcji i przycisku do dodawania nowej sekcji -->
     <h2 class="section-edit-info">Kliknij na nazwę sekcji by móc ją edytować!</h2>
     <div class="section-container">
      <div class="section-card" v-for="section in sections" :key="section.id">
        <div class="section-name" id="section-title" @click="editSection(section.id)" :data-section-id="section.id">
          <b>{{ section.name }}</b> 
        </div>
  
        <!-- Ramka z listą zadań -->
        <button @click="confirmDeleteSection(section)" class="button is-danger delete-section-btn">
          <i class="fas fa-times"></i>
        </button>
        
        <draggable  v-model="section.tasks" group="tasks" animation = "200" ghost-class="ghost-card" @start="onDragStart($event)" @end="onDragEnd($event)" >
          <template #item="{element}">
            <div class="task-list-frame">
              
                <div class="task-name-frame">
                  <div class="task-name" :data-task-id="element.id" @click="showTaskDetails(element)">
                    {{ element.name }}
                  </div>
                </div>
             
            </div>
          </template>
        </draggable>
  
        <!-- Przycisk do dodawania nowego zadania -->
        <button @click="openAddTaskModal(section)" class="add-task-button">Dodaj zadanie</button>
    </div>
  
       <!-- Przycisk do dodawania nowej sekcji -->
       <div class="add-section-btn-container">
         <button class="add-section-btn" @click="showModal = true"><i class="fas fa-plus" style="font-size: 50px;"></i></button>
       </div>
     </div>
  
      <!-- ------------------------------ MODALE  SEKCJA--------------------------------------------------------------------------------------- -->
      <!-- Modal do potwierdzenia usunięcia sekcji -->
    <div v-if="deleteConfirmationModalVisibleSection" class="modal" >
      <div class="modal-content" id="delete-section" style="max-width: 400px;">
        <h2 style="margin-bottom: 15px; font-weight: bold; font-size: 30px;">Usuń sekcję</h2>
        <p>Na pewno chcesz usunąć sekcję?</p>
        <div style="margin-top: 20px;">
          <button @click="deleteSection(confirmedDeleteSectionId)" class="button is-danger" style="margin-right: 15px;">Tak</button>
          <button @click="closeDeleteConfirmationModalSection" class="button is-info">Nie</button>
        </div>
      </div>
    </div>
  
     <!-- ----------- Modal do tworzenia nowej sekcji ----------- -->
     <div v-if="showModal" class="modal">
       <div class="modal-content">
         <span class="close" @click="showModal = false"><i class="fas fa-times"></i></span>
         <h2 class="section-name">Podaj nazwę sekcji</h2>
         <form @submit.prevent="createSection">
           <div class="form-group">
             <label for="sectionName" class="section-name">Nazwa sekcji: </label>
             <input type="text" id="sectionName" v-model="sectionName" class="form-control">
           </div>
           <button type="submit" class="btn btn-primary section-name">Utwórz sekcję</button>
         </form>
       </div>
     </div>
  
     <!-- ----------- Modal do edycji sekcji ----------- -->
     <div v-if="editSectionModalVisible" class="modal">
        <div class="modal-content">
          <span class="close" @click="closeEditModalSection"><i class="fas fa-times"></i></span>
          <h2 class="section-name" style="margin-bottom: 15px; font-weight: bold; font-size: 30px;">Edit Section</h2>
          <form @submit.prevent="updateSection">
  
  
            <div class="form-group">
              <label for="editSectionName" class="section-name" style="margin-bottom: 15px; margin-right:15px; font-weight: bold; font-size: 15px;">Nazwa sekcji:</label>
              <input type="text" id="editSectionName" v-model="editedSectionName" class="form-control">
            </div>
            <button type="submit" class="button is-primary" style="margin-top: 15px;">Edycja sekcji</button>
          </form>
        </div>
      </div>
  
      <!-- ------------------------------ MODALE  TASKI --------------------------------------------------------------------------------------- -->
     <!-- ----------- Modal do dodawania nowego zadania ----------- -->
     <div v-if="taskModalVisible" class="modal">
       <div class="modal-content">
         <span class="close" @click="closeAddTaskModal"><i class="fas fa-times"></i></span>
         <h2 class="section-name">Dodaj nowe zadanie</h2>
         <form @submit.prevent="createTask">
           <div class="form-group">
             <label for="taskName" class="section-name">Nazwa zadania:</label>
             <input type="text" id="taskName" v-model="taskName" class="form-control">
           </div>
           <div class="form-group">
             <label for="description" class="section-name">Opis:</label>
             <textarea id="description" v-model="description" class="form-control"></textarea>
           </div>
           <div class="form-group">
             <label for="dueDate" class="section-name">Termin:</label>
             <input type="date" id="dueDate" v-model="dueDate" class="form-control">
           </div>
  
           <button type="submit" class="btn btn-primary section-name">utwórz zadanie</button>
         </form>
       </div>
     </div>
     
      <!-- Twój kod dla modalu wyświetlającego szczegóły zadania -->
      <div v-if="selectedTask" class="modal">
          <div class="modal-content">
            <span class="close" @click="selectedTask = null"><i class="fas fa-times"></i></span>
            <h2 class="section-name">Informacje o zadaniu</h2>
            <div class="task-details">
              <!-- Nazwa zadania -->
              <div class="task-name" style="color: black; font-size: 25px;">{{ selectedTask.name }}</div>
              <div class="task-description" style="font-weight: bold;">Opis: {{ selectedTask.description }}</div>
              <div class="task-due-date" style="margin-bottom: 10px;"> 
                Termin: {{ selectedTask.due_date }}
                <br>
                <!-- Dodaj przycisk do otwierania modala do dodawania użytkownika -->
                <button @click="openAddUserModal" class="add-user-button">Dodaj użytkownika</button>
                <button @click="fetchTaskUsers(selectedTask.id)" class="show-users-button">Pokaż użytkowników</button>
              </div>
              <button @click="openEditModalTask(selectedTask)" class="edit-section-button">Edytuj</button>
              <button @click="deleteTask(selectedTask.id)" class="delete-task-button">Usuń</button>
            </div>
          </div>
        </div>
  
        <!-- Modal do dodawania użytkownika do zadania -->
    <div v-if="addUserModalVisible" class="modal">
      <div class="modal-content">
        <span class="close" @click="addUserModalVisible = false"><i class="fas fa-times"></i></span>
        <h2 class="section-name">Dodaj użytkownika do zadania</h2>
        <div class="form-group">
          <label for="userIdInput">Email użytkownika:</label>
          <input class="input" type="text" v-model="newUserEmail" placeholder="Wpisz email użytkownika">
        </div>
        <button @click="findAndAddUser" class="add-user-task-button">Dodaj</button>
      </div>
    </div>
  
        <!-- ----------- Modal do edycji taska ----------- -->
        <div v-if="editTaskModalVisible" class="modal">
       <div class="modal-content">
         <span class="close" @click="closeTaskEditModal"><i class="fas fa-times"></i></span>
         <h2 class="section-name">Edytuj</h2>
         <form @submit.prevent="editTask">
          <div class="form-group">
             <label for="taskName" class="section-name" style="font-size: 20px; margin-right: 15px; margin-top: 10px;">Nazwa:</label>
             <input type="text" id="taskName" v-model="taskName" class="form-control">
           </div>
           <div class="form-group">
             <label for="description" class="section-name" style="font-size: 20px;  margin-right: 15px; margin-top: 10px;">Opis:</label>
             <textarea id="description" v-model="description" class="form-control"></textarea>
           </div>
           <div class="form-group">
             <label for="dueDate" class="section-name" style="font-size: 20px;  margin-right: 15px; margin-top: 10px;">Termin:</label>
             <input type="date" id="dueDate" v-model="dueDate" class="form-control">
           </div>
           <button type="submit" class="btn btn-primary section-name">Edytuj</button>
         </form>
       </div>
     </div>
  
     <!-- ----------- Modal z użytkownikami przypisanymi do zadania ----------- -->
  <div v-if="taskUsers.length > 0" class="modal">
    <div class="modal-content">
      <span class="close" @click="taskUsers = []"><i class="fas fa-times"></i></span>
      <h2 class="section-name">Użytkownicy przypisani do zadania</h2>
      <ul>
        <li v-for="user in taskUsers" :key="user.id" style="margin-top: 10px;">
          {{ user.user_detail.email }}
          <button @click="deleteUserFromTask(user)" class="button is-danger is-small" >Remove</button>
        </li>
      </ul>
    </div>
  </div>
  
  <!-- Modal dla braku użytkowników -->
  <div v-if="taskUsersModalVisible" class="modal">
    <div class="modal-content">
      <span class="close" @click="closeTaskUsersModal"><i class="fas fa-times"></i></span>
      <h2 class="section-name">Brak użytkowników</h2>
      <p>Brak użytkowników przypisanych do tego zadania.</p>
    </div>
  </div>
  
     <!-- Modal do potwierdzenia usunięcia taska -->
    <div v-if="deleteConfirmationModalVisibleTask" class="modal" >
      <div class="modal-content" id="delete-task" style="max-width: 400px;">
        <h2 style="margin-bottom: 15px; font-weight: bold; font-size: 30px;">Usuń zadanie</h2>
        <p>Na pewno chcesz usunąć zadanie?</p>
        <div style="margin-top: 20px;">
          <button @click="deleteTask(confirmedDeleteSectionId)" class="button is-danger" style="margin-right: 15px;">Tak</button>
          <button @click="closeDeleteConfirmationModalTask" class="button is-info">Nie</button>
        </div>
      </div>
    </div>
   </div>

   <div v-if="addUserErrorModalVisibleCorrect" class="modal">
  <div class="modal-content">
    <span class="close" @click="addUserErrorModalVisibleCorrect = false"><i class="fas fa-times"></i></span>
    <h2 class="section-name">Sukces</h2>
    <p>Udało się dodać użytkownika.</p>
  </div>
</div>

    <div v-if="addUserErrorModalVisibleError" class="modal">
  <div class="modal-content">
    <span class="close" @click="addUserErrorModalVisibleError = false"><i class="fas fa-times"></i></span>
    <h2 class="section-name">Błąd</h2>
    <p>Nie udało się dodać użytkownika.</p>
  </div>
</div>
  </template>
  
  <script>
  import axios from 'axios';
  import draggable from "vuedraggable";
  
  export default {
   components: {
     draggable
   },
   data() {
     return {
       boardId: null,
       boardName: '',
       sections: [],
       tasks: [],
       sectionId: null,
       newSectionId: null,
       taskId: null,
       sectionName: '',
       taskName: '',
       description: '',
       dueDate: '',
       dragging: false,
       taskUsers: [],
       userId: null,
       addUserErrorModalVisibleCorrect: false,
       addUserErrorModalVisibleError: false,
       // Modal dla dodania sekcji
       showModal: false,
       selectedTask: null,
       // Modale dla sekcji
       editModalVisible: false,
       editedSectionId: null,
       editedSectionName: '',
       editSectionModalVisible: false,
       confirmedDeleteSectionId: null,
       deleteConfirmationModalVisibleSection: false,
       // Modale dla taskow
       taskModalVisible: false,
       editTaskModalVisible: false,
       taskUsersModalVisible:false,
       // Board Info
       infoPanelVisible: false,
       boardUsers: [],
       boardDescription: '',
       boardCreateDate: '',
       boardDueDate: '',
       //Drag n drop
       container: null,
       draggedtaskid: null,
       // add user to task
       selectedTask: null,
       boardUsers: [],
        selectedUser: null,
        addUserModalVisible: false,
        newUserEmail: '',
     };
   },
   mounted() {
     this.boardId = this.$route.params.board_id;
     this.sectionId = this.$route.params.section_id;
     this.fetchBoardName();
     this.fetchSections();
     this.fetchBoardData(); 
     console.log("Params:", this.$route.params);
   },
   methods: {
    editSection(sectionId) {
      this.$router.push(`/section/${this.$route.params.board_id}/edit-section/${sectionId}`);
    },
  
    async onDragStart(event){
      console.log("dragged task id " + event.item.querySelector('.task-name').dataset.taskId)
      this.draggedtaskid = event.item.querySelector('.task-name').dataset.taskId
    },
  
    async onDragEnd(event) {
    try {
      console.log("event log: " + event); // Wyświetlenie obiektu event w konsoli
      console.log("event item: " + event.item); // Wyświetlenie obiektu item w konsoli
  
      
      const container = event.to;
      
      // Sprawdzenie, czy kontener jest zdefiniowany
      if (!container) {
        console.error('Container is undefined');
        return;
      }
  
      // Uzyskanie sekcji docelowej
      const targetSection = container.closest('.section-card');
      
      // Sprawdzenie, czy udało się znaleźć sekcję docelową
      if (!targetSection) {
        console.error('Target section not found');
        return;
      }
  
      // Uzyskanie ID sekcji docelowej
      const newSectionId = targetSection.querySelector('.section-name').dataset.sectionId;
  
      // Get ID of task
      const taskId = this.draggedtaskid
      console.log("task ID: " + taskId);
  
      const response = await axios.patch(`http://127.0.0.1:8000/task/update_task_section/${taskId}/section/${newSectionId}`);
      console.log(response.data);
      console.log("Dziala") // Logowanie odpowiedzi z serwera
    } catch (error) {
      console.error('Error updating task section:', error);
    }
  },
  
  
  
  
      // ------------ Displaying board info ----------------
      async fetchBoardData() {
        try {
          // Pobranie danych tablicy z backendu
          const boardResponse = await axios.get(`http://127.0.0.1:8000/board/${this.boardId}/`);
          // Ustawienie opisu tablicy
          this.boardDescription = boardResponse.data.description;
          this.boardCreateDate = boardResponse.data.create_date;
          this.boardDueDate = boardResponse.data.due_date;
          // Pobranie listy użytkowników przypisanych do tablicy
          const usersResponse = await axios.get(`http://127.0.0.1:8000/board/${this.boardId}/users/`);
          this.boardUsers = usersResponse.data;
        } catch (error) {
          console.error('Error fetching board data:', error);
        }
      },
  

  
    // ----------- Fetche -----------
     async fetchBoardName() {
       try {
         const response = await axios.get(`http://127.0.0.1:8000/board/${this.boardId}/`);
         this.boardName = response.data.name;
       } catch (error) {
         console.error('Error fetching board name:', error);
       }
     },
  
     async fetchSections() {
       try {
         const response = await axios.get(`http://127.0.0.1:8000/section/${this.boardId}/sections/`);
         this.sections = response.data;
         for (const section of this.sections) {
           if (!section.tasks) {
             section.tasks = []; // Inicjalizacja pustej tablicy tasków, jeśli nie istnieje
             await this.fetchTasksForSection(section);
           }
         }
       } catch (error) {
         console.error('Error fetching sections:', error);
       }
     },
  
     async fetchTasksForSection(section) {
       try {
         const response = await axios.get(`http://127.0.0.1:8000/task/${section.id}/task_list/`);
         section.tasks = response.data;
       } catch (error) {
         console.error(`Error fetching tasks for section:`, error);
       }
     },
     // ----------- Section -----------
     async createSection() {
       try {
         const token = localStorage.getItem('token');
         const response = await axios.post(
           `http://127.0.0.1:8000/section/${this.boardId}/create_section/`,
           { name: this.sectionName, board: this.boardId },
           { headers: { Authorization: `Token ${token}` } }
         );
         console.log('Section created:', response.data);
         this.showModal = false;
         this.fetchSections();
       } catch (error) {
         console.error('Error creating section:', error);
       }
     },
     async updateSection() {
      try {
          const token = localStorage.getItem('token');
          const response = await axios.put(
              `http://127.0.0.1:8000/section/${this.boardId}/update_section/${this.section.id}/`,
              { name: this.sectionName},
           { headers: { Authorization: `Token ${token}` } }
          );
          console.log('Section updated:', response.data);
          this.editModalVisible = false;
          this.fetchSections(); // Ponowne pobranie sekcji po aktualizacji
      } catch (error) {
          console.error('Error updating section:', error);
      }
    },
    async deleteSection(sectionId) {
      try {
        const token = localStorage.getItem('token');
        await axios.delete(`http://127.0.0.1:8000/section/delete_section/${sectionId}`, {
          headers: {
            Authorization: `Token ${token}`
          }
        });
        this.fetchSections(); // Odśwież listę sekcji po usunięciu
        this.deleteConfirmationModalVisibleSection = false;
      } catch (error) {
        console.error('Error deleting section:', error);
      }
    },
  
    // ----------- MODAL DLA SEKCJI -----------
    openEditModalSection(section) {
      this.editSectionModalVisible = true;
      this.editedSectionId = section.id;
      this.editedSectionName = section.name;
    },
  
   
    closeEditModalSection() {
      this.editSectionModalVisible = false;
    },
  
    confirmDeleteSection(section) {
        this.confirmedDeleteSectionId = section.id;
        this.deleteConfirmationModalVisibleSection = true;
    },
  
    closeDeleteConfirmationModalSection() {
      this.deleteConfirmationModalVisibleSection = false;
    },
  
    closeTaskUsersModal() {
    this.taskUsersModalVisible = false;
  },
  
  
    // ----------- TASKI -----------
      // Delete
  async deleteUserFromTask(user) {
      try {
        this.removeUserId = user.user_detail.id;
        console.log("User:", user); // Dodajmy to logowanie
        //const userId = user.user_detail.id; // Pobierz user_id z obiektu user
        // Wykonanie zapytania HTTP do usunięcia użytkownika z tablicy
        await axios.delete(`http://127.0.0.1:8000/task/${this.selectedTask.id}/user/${this.removeUserId}/delete/`);

        // Pobranie zaktualizowanej listy użytkowników po usunięciu
        //await this.fetchTasksUsers(this.selectedTask.id);
        window.location.reload();
      } catch (error) {
        console.error('Error deleting user from board:', error);
      }
    },
    
    async findAndAddUser() {
  try {
    console.log('Searching for user with email:', this.newUserEmail); // Debugging log
    // Wyszukanie użytkownika na podstawie adresu e-mail
    const response = await axios.get(`http://127.0.0.1:8000/user/find/?email=${this.newUserEmail}`);
    console.log('Response data:', response.data); // Debugging log
    if (response.data.user_id) { // Sprawdzamy czy istnieje użytkownik
      const userId = response.data.user_id;

      // Dodanie użytkownika do zadania za pomocą ID
      await this.addUserToTask(userId);

      // Czyszczenie pola adresu e-mail po dodaniu użytkownika
      this.newUserEmail = '';
      this.addUserModalVisible = false;
      this.selectedTask = false;
      this.addUserErrorModalVisibleCorrect = true;
    } else {
      console.log('No user found with the provided email.');
      this.addUserModalVisible = false;
      this.selectedTask = false;
      this.addUserErrorModalVisibleError = true;
    }
  } catch (error) {
    console.error('Error finding and adding user:', error);
    this.addUserModalVisible = false;
      this.selectedTask = false;
      this.addUserErrorModalVisibleError = true;
  }
},

async addUserToTask(userId) {
    try {
      const selectedTask = this.selectedTask;
      // Dodanie użytkownika do zadania za pomocą jego ID
      await axios.post(`http://127.0.0.1:8000/task/${this.boardId}/create_task_user/${this.selectedTask.id}`, { user: userId });
  
      // Zamknięcie modala po dodaniu użytkownika
      this.addUserModalVisible = false;
      this.selectedTask = false;
      this.showNotificationCorrect = true;
    } catch (error) {
      console.error('Błąd podczas dodawania użytkownika do zadania:', error);
      
    }
  },

  // Otwieranie modala do dodania użytkownika
  openAddUserModal() {
    this.addUserModalVisible = true;
  },

  closeAddUserModal() {
    this.addUserModalVisible = false;
    this.newUserEmail = '';
  },
  
  async fetchTaskUsers(taskId) {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/task/${taskId}/task_user_list/`);
      this.taskUsers = response.data;
      
      if (Array.isArray(this.taskUsers) && this.taskUsers.length === 0) {
        this.taskUsersModalVisible = true;
      }
    } catch (error) {
      console.error('Błąd podczas pobierania użytkowników zadania:', error);
    }
  },
    async createTask() {
        try {
          const token = localStorage.getItem('token');
          const currentDate = new Date();
          const response = await axios.post(
            'http://127.0.0.1:8000/task/create/',
            { name: this.taskName, description: this.description, section: this.selectedSectionId, create_date: currentDate, due_date: this.dueDate,  },
            { headers: { Authorization: `Token ${token}` } }
          );
          console.log('Task created:', response.data);
          this.taskModalVisible = false;
          this.fetchSections(); // Po utworzeniu zadania odśwież listę sekcji, aby wyświetlić nowe zadanie
        } catch (error) {
          console.error('Error creating task:', error.response);
        }
      },
  
     async editTask(selectedTask) {
      try {
        const token = localStorage.getItem('token');
        //const currentDate = new Date();
        const response = await axios.put(
          `http://127.0.0.1:8000/task/update_task/${this.selectedTask.id}`,  
          { 
            name: this.taskName, 
            description: this.description, 
            section: this.selectedSectionId,
            due_date: this.dueDate,
          },
          { headers: { Authorization: `Token ${token}` } }
        );
  
        console.log('Task updated:', response.data);
        window.location.reload();
        this.fetchTasksForSection();
        // Tutaj możesz dodać odpowiednią obsługę po udanej aktualizacji zadania, np. odświeżenie listy zadań
      } catch (error) {
        console.error('Error updating task:', error);
      }
    },
    async deleteTask(taskId) {
      try {
        await axios.delete(`http://127.0.0.1:8000/task/delete_task/${taskId}`,);
        this.fetchTasksForSection(); // Aktualizuj listę zadań po usunięciu
        window.location.reload();
      } catch (error){
        console.error('Error deleting task:', error);
      }
    },
      // ----------- MODALE TASKI -----------
    // Add Task
    // wyswietlenie
    openAddTaskModal(section) {
      this.taskModalVisible = true;
      this.sectionName = section.sectionName;
      this.selectedSectionId = section.id;
    },
    // zamkniecie
    closeAddTaskModal() {
      this.taskModalVisible = false;
    },
    // Delete Task
    showTaskDetails(task) {
      this.selectedTask = task;
    },
    // Edit Task
    openEditModalTask(task) {
    this.editTaskModalVisible = true;
    this.taskName = task.name;
    this.description = task.description; 
    this.sectionName = task.sectionName;  // Check if this property is correct
    this.dueDate = task.dueDate; // Check if this property is correct
  },
  
    closeTaskEditModal() {
      this.editTaskModalVisible = false; 
    },
    // Details Task
    closeTaskDetailsModal() {
      this.selectedTask = false;
    },

    hideNotificationCorrect(){
      this.showNotificationCorrect = false;
    },

    hideNotificationError(){
      this.showNotificationError = false;
    },
    toggleInfoPanel() {
      this.infoPanelVisible = !this.infoPanelVisible;
    },
    } 
  };
  </script>
  
  
  <style scoped src="../../style/SectionTable.css"></style>