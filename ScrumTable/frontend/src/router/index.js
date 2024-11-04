import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SignUp from '../views/SignUp.vue'
import LogIn from '../views/LogIn.vue'
import UserPanel from '../views/UserPanel.vue'
import Tables from '../views/Tables.vue'
import CreateTable from '../views/CreateTable.vue'
import AddNewBoard from '../views/AddNewBoard.vue'
import SectionTable from '../views/SectionTable.vue'
import EditSection from '../views/EditSection.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/sign-up',
    name: 'SignUp',
    component: SignUp
  },
  {
    path: '/log-in',
    name: 'LogIn',
    component: LogIn
  },
  {
    path: '/user-main',
    name: 'UserPanel',
    component: UserPanel
  },
  {
    path: '/tables',
    name: 'Tables',
    component: Tables
  },
  {
    path: '/create-table',
    name: 'CreateTable',
    component: CreateTable
  },
  {
    path: '/add-board',
    name: 'AddNewBoard',
    component: AddNewBoard
  },
  {
    path: '/section-table/:board_id/create_section',
    name: 'SectionTable',
    component: SectionTable
  },
  {
    path: '/section/:board_id/edit-section/:section_id',
    name: 'EditSection',
    component: EditSection
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router