<template>
    <div style="height: 100vh">
        <el-container style="height: 100%;">
            <el-header style="padding: 0;">
                <Header/>
            </el-header>
            <el-container>
                <el-aside width="200px">
                    <Sider/>
                </el-aside>
                <el-container class="main-container">
                    <el-main>
                        <router-view/>
                    </el-main>
                    <el-footer style="background-color: #f3f3f3;font-size: 12px;line-height: 40px;height: 40px">
                        <Footer/>
                    </el-footer>
                </el-container>
            </el-container>
        </el-container>
    </div>
</template>

<script setup>
import Sider from "./Sider.vue";
import Header from "./Header.vue";
import Footer from "./Footer.vue";
</script>


<script>
export default {
  name: "MainPage"
}
</script>

<style scoped>
.el-header {
    position: relative;
    width: 100%;
    height: 60px;
}

.el-aside {
    display: block;
    position: absolute;
    left: 0;
    top: 60px;
    bottom: 0;
}

.main-container {
    position: absolute;
    left: 200px;
    right: 0;
    top: 60px;
    bottom: 0;
    overflow-y: auto;
}
</style>
