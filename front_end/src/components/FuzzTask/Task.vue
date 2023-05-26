<template>
    <el-page-header @back="onBack">
        <template #content>
            <div>FuzzTask</div>
        </template>
    </el-page-header>

    <el-card style="margin-top: 20px">
        <el-menu :default-active="index" mode="horizontal">
            <router-link :to="`/fuzztask/${route.params.id}`" style="text-decoration: none">
                <el-menu-item index="0">Task</el-menu-item>
            </router-link>
            <router-link :to="`/fuzztask/${route.params.id}/submit`" style="text-decoration: none">
                <el-menu-item index="1">Submit</el-menu-item>
            </router-link>
            <router-link :to="`/fuzztask/${route.params.id}/board`" style="text-decoration: none">
                <el-menu-item index="2">Board</el-menu-item>
            </router-link>
            <router-link :to="`/fuzztask/${route.params.id}/record`" style="text-decoration: none">
                <el-menu-item index="3">Record</el-menu-item>
            </router-link>
        </el-menu>
        <router-view/>
    </el-card>
</template>

<script setup>
import {useRoute, useRouter} from "vue-router";
import {onMounted, ref} from "vue";

const route = useRoute();
const router = useRouter()

let index = ref('0')

onMounted(() => {
  if (route.path.includes('submit')) {
    index.value = '1'
  } else if (route.path.includes('board')) {
    index.value = '2'
  } else if (route.path.includes('record')) {
    index.value = '3'
  } else {
    index.value = '0'
  }
})

const onBack = () => {
  router.push('/fuzztask')
}

</script>

<script>
export default {
  name: "Task"
}
</script>

<style scoped>

</style>
