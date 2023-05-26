<template>
    <div>
        <h1>Fuzz Task</h1>
        <el-row v-loading="taskListLoading" :gutter="10">
            <el-col v-for="task in taskList" :key="task.id" :xs="24" :sm="24" :md="12" :lg="8" :xl="8">
                <router-link style="text-decoration: none" :to="`/fuzztask/${task.id}`">
                    <el-card style="margin-top: 20px; margin-left: 5px; margin-right: 5px">
                        <template #header>
                            <div>
                                <b style="font-size: 22px">{{ task.name }}</b>
                                <span style="float: right; padding: 3px 0;color: gray" >{{task.type}}</span>
                            </div>
                        </template>
                        <template #default>
                            <span><el-image :src="logoList[task.index]"/></span>
                            <p class="task-content">
                                {{ task.description }}
                            </p>
                        </template>
                    </el-card>
                </router-link>
            </el-col>
        </el-row>
    </div>
</template>

<script setup>
import TaskAPI from "../../api/TaskAPI.js";
import {onMounted, ref} from 'vue'
import bug1 from '../../assets/bug1.png'
import AFL_Dumb from '../../assets/task/AFL_Dumb.jpg'
import AFL_Easy from '../../assets/task/AFL_Easy.jpg'
import AFL_Standard from '../../assets/task/AFL_Standard.jpg'
import AFL_Quick from  '../../assets/task/AFL_Quick.jpg'

const logoList = [AFL_Easy, AFL_Quick, AFL_Dumb, AFL_Standard]

let taskList = ref([])
let taskListLoading = ref(true)
let user = ref(null);

onMounted(() => {
    TaskAPI.getTaskList().then((res) => {
        taskList.value = res.data.data.task_list;
        taskListLoading.value = false;
    }).catch((err) => {
        console.log(err)
    })
})

</script>

<script>
export default {
    name: "FuzzTask"
}
</script>

<style>
.task-content{
    font-size: 15px;
    overflow: hidden;
    letter-spacing: 0.6px;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
}
</style>
