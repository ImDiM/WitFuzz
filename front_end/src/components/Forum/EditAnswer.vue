<!-- src/components/AddAnswer.vue -->
<template>
  <div @submit.prevent="Commit" class="add-answer">
    <h1 class="title">Edit Your Answer</h1>
    <form class="answer-form">
      <div class="form-group">
        <textarea id="answerContent" v-model="answerContent" class="form-control" rows="5" placeholder="请输入回答"
          required></textarea>
      </div>
      <button type="submit" class="submit-btn" @click="submitAnswer()">Submit</button>
    </form>
  </div>
</template>
  
<script>

import axios from "axios";
import ForumAPI from "../..//api/ForumAPI";
export default {
  data() {
    return {
      problemId: "",
      answerContent: "",
    };
  },
  async created() {
    try {
      ForumAPI.getAnswer(localStorage.getItem('problem_id'),localStorage.getItem('answer_id')).then(res => {
        console.log(res)
        if (res.data.code == 202) {
          alert(res.data.msg)
          return
        }
        this.problemId = res.data.data.problem_id
        this.answerContent = res.data.data.content
      })

    } catch (error) {
      console.error("Error When get detail：", error);
      alert("Error When get detail.Please try later.");
    }
  },
  methods: {
    async submitAnswer() {
      if (!this.answerContent) {
        alert("Contet can't be empty!");
        return;
      }
      ForumAPI.editAnswer(localStorage.getItem('problem_id'), localStorage.getItem('answer_id'), this.answerContent).then(res => {
        if (res.data.code == 202) {
          alert(res.data.msg)
          return
        }
        console.log(res)
      })
      console.log('---------');
      alert("Submitted");
      window.location = '/forum/'+ localStorage.getItem('problem_id');
    }
  }
};
</script>
  
<style scoped>
.add-answer {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  text-align: center;
  max-width: 600px;
  margin: 40px auto;
  background-color: #f8f9fa;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
}

.title {
  font-size: 2rem;
  color: #2c3e50;
  margin-bottom: 2rem;
}

.answer-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: inline-block;
  margin-bottom: 0.5rem;
}

.form-control {
  display: block;
  width: 100%;
  padding: 0.5rem;
  font-size: 1rem;
  line-height: 1.5;
  color: #495057;
  background-color: #fff;
  background-clip: padding-box;
  border: 1px solid #ced4da;
  border-radius: 0.25rem;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.form-control:focus {
  border-color: #80bdff;
  outline: 0;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.submit-btn {
  background-color: #007bff;
  color: #fff;
  font-size: 1rem;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  width: 100%;
  margin-top: 1rem;
}

.submit-btn:hover {
  background-color: #0056b3;
}
</style>