<template>
    <el-menu
            :default-active="index"
            style="height: 100%"
            @close="handleClose"
            @open="handleOpen"
    >
        <router-link to="/home">
            <el-menu-item index="0">
                <el-icon>
                    <HomeFilled/>
                </el-icon>
                <span>Home</span>
            </el-menu-item>
        </router-link>

        <router-link to="/fuzztask">
            <el-menu-item index="1">
                <el-icon>
                    <icon-menu/>
                </el-icon>
                <span>FuzzTask</span>
            </el-menu-item>
        </router-link>

        <router-link to="/forum">
            <el-menu-item index="2">
                <el-icon>
                    <HelpFilled/>
                </el-icon>
                <span>Forum</span>
            </el-menu-item>
        </router-link>
    </el-menu>
</template>

<script setup>
import {HelpFilled, HomeFilled, Menu as IconMenu} from '@element-plus/icons-vue'
import {useRoute, useRouter} from "vue-router";
import {onMounted, ref} from "vue";

const route = useRoute();
const router = useRouter()
let index = ref(0)

onMounted(() => {
  if (route.path.includes('fuzztask')) {
    index.value = 1
  } else if (route.path.includes('forum')) {
    index.value = 2
  } else {
    index.value = 0
  }
})

const handleOpen = (key, keyPath) => {
  console.log(key, keyPath);
};
const handleClose = (key, keyPath) => {
  console.log(key, keyPath);
};

</script>

<script>
export default {
  name: "Sider"
}
</script>

<style scoped>
a {
    text-decoration: None;
}

.router-link-active {
    text-decoration: None;
}
</style>
