<template>
  <div class="container">
    <div class="problem-container">
      <h1 class="problem-title">{{ problem.title }}</h1>
      <pre class="problem-description">{{ problem.description }}</pre>
      <div class="answer-info">
        <span class="answer-author">Raiser：{{ problem.user }}</span>
        <span class="answer-date">Answer NO.:{{ problem.answer_number }}</span>
        <div v-if="problem.user_id == user" class="del-btn">
          <router-link :to="`/forum/editProblem`">
            <button class = "edit"  type="submit" @click="addProblemToken()">Edit</button>
          </router-link>
          <router-link :to="`/forum`">
            <button class = "delete"  type="submit" @click="deleteProblem(problem.id)">Delete</button>
          </router-link>
        </div>
        <div v-else class="del-btn"></div>

      </div>
    </div>

    <div class="answers-container">
      <div class="answer" v-for="answer in answers" :key="answer.id">
        <pre class="answer-content">{{ answer.content }}</pre>
        <div class="answer-info">
          <span class="answer-author">Answer：{{ answer.user }}</span>
          <span class="answer-date">Edit Time:{{ answer.edit_time }}</span>
          <div v-if="answer.user_id == user" class="del-btn">
            <router-link :to="`/forum/editAnswer`">
              <button class = "edit" type="submit" @click="addAnswerToken(answer.id)">Edit</button>
            </router-link>
            <router-link :to="`/forum`">
              <button class = "delete" type="submit" @click="deleteAnswer(answer.id)">Delete</button>
              </router-link>
          </div>
          <div v-else class="del-btn">
          </div>
        </div>
      </div>
    </div>

    <div v-if="user > 0" class="add-btn">
      <router-link :to="`/forum/${problem.id}/addAnswer`">
        <button type="submit">Reply</button>
      </router-link>
    </div>
    <div v-else style="float: right" class="login-btn">
      <router-link :to="`/login`">
        <button type="submit">Join us</button>
      </router-link>
    </div>
  </div>
</template>



<script setup>
import { onMounted, ref } from "vue";
let user = ref(localStorage.getItem("user_id"))
</script>
<script>
import axios from 'axios';
import ForumAPI from "../..//api/ForumAPI";
export default {
  name: "Problem",
  data() {
    return {
      problem: {
        title: "",
        description: "",
        user: "",
        answer_number: "",
        id: ""
      },
      answers: []
    };
  },


  async created() {
    try {
      ForumAPI.getProblem(this.$route.params.problemId).then(res => {
        console.log(res)
        if (res.data.code == 202) {
          alert(res.data.msg)
          return
        }

        this.problem = res.data.data
        this.addProblemToken()
      })
      ForumAPI.getAnswerList(this.$route.params.problemId).then(res => {
        console.log(res)
        if (res.data.code == 202) {
          alert(res.data.msg)
          return
        }

        this.answers = res.data.data
      })
    } catch (error) {
      console.error("Error When get detail：", error);
      alert("Error When get detail.Please try later.");
    }
  },
  methods: {
    deleteProblem(problem_id) {
      ForumAPI.delProblem(problem_id).then(res => {
        console.log(res)
        if (res.data.code == 202) {
          alert(res.data.msg)
          return
        }
      })
      alert("deleted");
    },
    deleteAnswer(answer_id) {
      ForumAPI.delAnswer(this.problem.id, answer_id).then(res => {
        if (res.data.code == 202) {
          alert(res.data.msg)
          return
        }
        console.log(res)
      })
      alert("deleted");
      location.reload();
    },
    addAnswerToken(answer_id) {
      localStorage.setItem('answer_id', answer_id)
    },
    addProblemToken() {
      localStorage.setItem('problem_id', this.problem.id)
    }
  },
}
</script>
  
<style scoped>
.problem-container {
  background-color: #f9f9f9;
  border-radius: 5px;
  padding: 20px;
  margin-bottom: 20px;
}

.problem-title {
  font-size: 2rem;
  color: #2c3e50;
  margin-bottom: 1rem;
}

.problem-content {
  font-size: 1.2rem;
  color: #333;
  margin-bottom: 1rem;
}

.answers-container {
  margin-bottom: 40px;
}

.answer {
  background-color: #fff;
  border-radius: 5px;
  padding: 15px;
  margin-bottom: 10px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24);
}

.answer-info {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
  color: #999;
  margin-top: 10px;
}

.answer-author,
.answer-date {
  margin: 0;
}

button[type="submit"] {
  background-color: #0084ff;
  color: #ffffff;
  border: none;
  border-radius: 5px;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}

button[type="submit"]:hover {
  background-color: #0073e6;
}

.add-btn {
  text-align: center;
}

.answer-content {
  padding: 10px;
  font-family: "Courier New", monospace;
  font-size: 16px;
  line-height: 1.5;
  white-space: pre-wrap;
}

.problem-description {
  font-size: 20px;
  color: #2c3e50;
  margin-bottom: 1rem;
  font-family: Arial, Helvetica, sans-serif;
}
.edit,
.delete {
  background-color: #007bff;
  color: #fff;
  font-size: 1rem;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-right: 50px;
}
</style>