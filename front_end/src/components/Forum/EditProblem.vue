<!-- src/components/AddProblem.vue -->
<template>
  <div class="add-problem">
    <h1 class="title">Edit Your Problem</h1>
    <form @submit.prevent="Commit" class="problem-form">
      <div class="form-group">
        <label for="problemTitle" class="form-label">Title</label>
        <input type="text" id="problemTitle" v-model="problemTitle" class="form-control"  required />
      </div>
      <div class="form-group">
        <label for="problemDescription" class="form-label">Description</label>
        <textarea id="problemDescription" v-model="problemDescription" class="form-control" rows="5" 
          required></textarea>
      </div>
      <button type="submit" class="submit-btn" @click="submitData()">Submit</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';
import ForumAPI from "../..//api/ForumAPI";
export default {
  data() {
    return {
      problemTitle: "",
      problemDescription: ""
    };
  },
  async created() {
    try {
      ForumAPI.getProblem(localStorage.getItem('problem_id')).then(res => {
        console.log(res)
        if (res.data.code == 202) {
          alert(res.data.msg)
          return
        }
        this.problemTitle = res.data.data.title
        this.problemDescription = res.data.data.description
      })

    } catch (error) {
      console.error("Error When get detail：", error);
      alert("Error When get detail.Please try later.");
    }
  },
  methods: {
    async submitData() {
      if (!this.problemTitle) {
        alert("Title can't be empty!");
        return;
      }
      if (!this.problemDescription) {
        alert("Description can't be empty!");
        return;
      }
      ForumAPI.editProblem(localStorage.getItem('problem_id'),this.problemTitle,this.problemDescription).then(res => {
        console.log(res)
        if (res.data.code == 202) {
          alert(res.data.msg)
          return
        }
      })
      alert("Submitted");
      window.location = "/forum/"+localStorage.getItem('problem_id');
    }
  }
};
</script>

<style scoped>
.add-problem {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  /* text-align: center; */
  max-width: 600px;
  margin: 40px auto;
  background-color: #f8f9fa;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
}

.title {
  text-align: center;
  font-size: 2rem;
  color: #2c3e50;
  margin-bottom: 2rem;
}

.problem-form {
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