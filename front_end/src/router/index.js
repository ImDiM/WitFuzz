import { createRouter, createWebHistory } from 'vue-router'


const Register = () => import('../components/User/Register.vue')
const Login = () => import('../components/User/Login.vue')
const Retrieve = () => import('../components/User/Retrieve.vue')
const MainPage = () => import('../components/MainPage.vue')
const Home = () => import('../components/Home/Home.vue')
const FuzzTask = () => import('../components/FuzzTask/FuzzTask.vue')
const Forum = () => import('../components/Forum/Forum.vue')

const Task = () => import('../components/FuzzTask/Task.vue')

const TaskInfo = () => import('../components/FuzzTask/TaskInfo.vue')
const TaskSubmit = () => import('../components/FuzzTask/TaskSubmit.vue')
const Taskboard = () => import('../components/FuzzTask/TaskBoard.vue')
const TaskRecord = () => import('../components/FuzzTask/TaskRecord.vue')

const Problem = () => import('../components/Forum/Problem.vue')
const AddProblem = () => import('../components/Forum/AddProblem.vue')
const MyProblem = () => import('../components/Forum/MyProblem.vue')
const AddAnswer = () => import('../components/Forum/AddAnswer.vue')
const EditProblem = () => import('../components/Forum/EditProblem.vue')
const EditAnswer = () => import('../components/Forum/EditAnswer.vue')

const UserInfo = () => import('../components/User/Info.vue')





const routes = [
  {
    path: '/',
    name: 'MainPage',
    component: MainPage,
    children: [
      {
        path: '',
        redirect: 'home'
      },
      {
        path: 'home',
        name: 'Home',
        component: Home
      },
      {
        path: 'fuzztask',
        children: [
          {
            path: '',
            name: 'FuzzTask',
            component: FuzzTask
          },
          {
            path: ':id',
            name: 'Task',
            component: Task,
            children: [
              {
                path: '',
                name: 'TaskInfo',
                component: TaskInfo
              },
              {
                path: 'submit',
                name: 'TaskSubmit',
                component: TaskSubmit
              },
              {
                path: 'board',
                name: 'Taskboard',
                component: Taskboard
              },
              {
                path: 'record',
                name: 'TaskRecord',
                component: TaskRecord
              }
            ]
          }
        ]
      },
      {
        path: 'forum',
        name: 'Forum',
        component: Forum,
      },
      {
        path: 'forum/addProblem',
        name: 'AddProblem',
        component: AddProblem
      },
      {
        path: 'forum/:problemId',
        name: 'Problem',
        component: Problem
      },
      {
        path: 'forum/:problemId/addAnswer',
        name: 'addAnswer',
        component: AddAnswer
      },
      {
        path: 'forum/myProblem',
        name: 'MyProblem',
        component: MyProblem
      },
      {
        path: 'forum/editProblem',
        name: 'EditProblem',
        component: EditProblem
      },
      {
        path: 'forum/editAnswer',
        name: 'EditAnswer',
        component: EditAnswer
      },
    ]
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/retrieve',
    name: 'Retrieve',
    component: Retrieve
  },
  {
    path: '/user/info',
    name: 'UserInfo',
    component: UserInfo
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
