<template>
  <div class="forum-homepage">
    <h1 class="title">WitFuzz Forum</h1>
    <ul class="problems-list">
      <li v-for="problem in problems" :key="problem.id" class="problem-item">
        <span>Problem{{ problem.id }}</span>
        <span class="problem-title">{{ problem.title }}</span>
        <router-link :to="`/forum/${ problem.id }`">
          <button class="view-problem-btn">
            Detail
          </button>
        </router-link>
      </li>
    </ul>
    <div v-if="!login" style="float: right">
      <router-link to="/login">
      <button class="login-btn">
          Join us
        </button>
        </router-link>
    </div>
    <div v-else style="float: right;" >
    <router-link :to="{ path: '/forum/addProblem' }">
      <button class="add-problem-btn">
        New Problem
      </button>
    </router-link>
    <router-link :to="{ path: '/forum/myProblem' }">
      <button class="view-my-problem-btn">
        View My Problems
      </button>
    </router-link>
    </div>
  </div>
</template>
  
<script setup>
import { onMounted, ref } from "vue";
import UserAPI from "../..//api/UserAPI";
let login = ref(false)
onMounted(() => {
  // TODO 存在 token
  if (localStorage.getItem('token') != null) {
    // for test only
    setTimeout(() => {
      login.value = true
    }, 10)
  }
  else {
    login.value = false

  }
})
</script>

<script>

import axios from "axios";
import ForumAPI from "../..//api/ForumAPI";
export default {
  name: "Forum",
  data() {
    return {
      problems: [],

    };
  },
  async created() {
    try {
      ForumAPI.getProblemList().then(res => {
          console.log(res)
          this.problems = res.data.data
        })
    } catch (error) {
      console.error("Error When get list：", error);
      alert("Error When get list.Please try later.");
    }
  }
  
  
}

</script>

<style scoped>
.forum-homepage {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  text-align: center;
  max-width: 800px;
  margin: 40px auto;
}

.title {
  font-size: 2rem;
  color: #2c3e50;
  margin-bottom: 1rem;
}

.problems-list {
  list-style-type: none;
  padding: 0;
}

.problem-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f8f9fa;
  border: 1px solid #dee2e6;
  padding: 1rem;
  border-radius: 5px;
  margin-bottom: 1rem;
}

.problem-title {
  font-size: 1.1rem;
  color: #495057;
}

.view-problem-btn {
  background-color: #007bff;
  color: #fff;
  font-size: 1rem;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
.login-btn,
.add-problem-btn,
.view-my-problem-btn {
  background-color: #007bff;
  color: #fff;
  font-size: 1rem;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-right: 50px;
}


.view-problem-btn:hover {
  background-color: #0056b3;
}
</style>
