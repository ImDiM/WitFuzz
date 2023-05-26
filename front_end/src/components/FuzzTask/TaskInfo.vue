<template>
    <div v-loading="taskLoading" style="margin-left: 8%; margin-right: 8%; margin-bottom: 30px;">
        <h1 style="font-size: 40px;text-align: center">{{task.name}}</h1>
        <p style="text-align: center">{{task.description}}</p>
        <el-divider/>
        <mavon-editor v-model="task.content" defaultOpen="preview" :subfield="false" :editable="false" :toolbarsFlag="false" style="height: 100%;"/>
    </div>
</template>

<script setup>
import {ref} from "vue";
import {onMounted} from "vue";
import {useRoute, useRouter} from "vue-router";
import {mavonEditor} from "mavon-editor";
import 'mavon-editor/dist/css/index.css'
import TaskAPI from "../../api/TaskAPI.js";

const route = useRoute();
const router = useRouter()

const taskId = route.params.id

let task = ref({
    content: ''
})
let taskLoading = ref(true)

onMounted(() => {
    TaskAPI.getTask(taskId).then((res) => {
        task.value = res.data.data.task;
        taskLoading.value = false;
    }).catch((err) => {
        taskLoading.value = false;
        console.log(err)
    })
})
</script>

<script>
export default {
    name: "TaskInfo",
    components: {
        mavonEditor
    },
}
</script>

<style scoped>

</style>
