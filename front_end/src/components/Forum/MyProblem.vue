<template>
  <div class="forum-homepage">
    <h1 class="title">My Problems</h1>
    <ul class="questions-list">
      <li v-for="question in questions" :key="question.id" class="question-item">
        <div class = "question-div">
        <span class="question-title">{{ question.title }}</span>
        </div>
        <router-link :to="{ path: '/forum/'+question.id }">
          <button class="view-question-btn" @click="viewQuestion(question.id)">
            Detail
          </button>
        </router-link>
        <router-link :to="{ path: '/forum/MyProblem' }">
          <button class="delete-question-btn" @click="deleteQuestion(question.id)">
            Delete
          </button>
        </router-link>
      </li>
    </ul>
  </div>
</template>
  

<script>
import ForumAPI from "../..//api/ForumAPI";
export default {
  name: "MyProblem",
  data() {
    return {
      questions: [ ]
    };
  },
  methods: {
    viewQuestion(questionId) {
      // 在这里添加导航到问题详细页面的逻辑
    },

    deleteQuestion(questionId) {
      ForumAPI.delProblem(questionId).then(res => {
        console.log(res)
        if (res.data.code == 202) {
          alert(res.data.msg)
          return
        }
      })
      alert("删除成功！");
      location.reload();
    }
  },
  async created() {
    try {
      ForumAPI.getMyProblems().then(res => {
        console.log(res)
        if (res.data.code == 202) {
          alert(res.data.msg)
          return
        }
        this.questions = res.data.data
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

.questions-list {
  list-style-type: none;
  padding: 0;
}

.question-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f8f9fa;
  border: 1px solid #dee2e6;
  padding: 1rem;
  border-radius: 5px;
  margin-bottom: 1rem;
}

.question-title {
  font-size: 1.1rem;
  color: #495057;
  max-width: 500px;
}

.view-question-btn {
  float: right;
}


.view-question-btn,
.delete-question-btn {
  background-color: #007bff;
  color: #fff;
  font-size: 1rem;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

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


.view-question-btn:hover {
  background-color: #0056b3;
}
.question-div{
  width: 600px;
}
</style>
