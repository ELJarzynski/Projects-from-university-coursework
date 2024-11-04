<template>
    <div class="create-board-container">
      <div class="form-group-container">
        <div class="form-panel">
          <h1>Create New Board</h1>
          <form @submit.prevent="createBoard" class="create-board-form">
            <div class="form-group">
              <label for="name">Name:</label>
              <input type="text" id="name" v-model="newBoard.name" class="form-control">
            </div>
            <div class="form-group">
              <label for="description">Description:</label>
              <textarea id="description" v-model="newBoard.description" class="form-control textarea-description"></textarea>
            </div>
            <div class="form-group">
              <label for="dueDate">Due Date:</label>
              <input type="date" id="dueDate" v-model="newBoard.due_date" class="form-control">
            </div>
            <button type="submit" class="btn btn-primary create-board-button">Create Board</button>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        newBoard: {
          name: '',
          description: '',
          due_date: ''
        }
      };
    },
    methods: {
      async createBoard() {
        try {
          const response = await axios.post('http://127.0.0.1:8000/board/create_board/', this.newBoard);
          console.log('Board created:', response.data);
          // Przekierowanie użytkownika do strony z listą tablic po utworzeniu tablicy
          this.$router.push('/tables');
        } catch (error) {
          console.error('Error creating board:', error);
        }
      }
    }
  };
  </script>
<style scoped src="../../style/CreateTable.css"></style>
