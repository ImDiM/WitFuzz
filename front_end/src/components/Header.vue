<template>
    <div style="height: 100%; width: 100%; background-color: aliceblue;">
        <div style="float: left;line-height: 60px;cursor: pointer" @click="toHomePage">
            <el-row style="height: 60px">
                <el-col :span="9">
                    <el-image :src="logo" style="width: 34px;height: 34px;margin-left: 20px;margin-top: 13px"/>
                </el-col>
                <el-col :span="15">
          <span style="font-size: 30px;font-weight: bold">
            WitFuzz
          </span>
                </el-col>
            </el-row>
        </div>

        <div v-if="!login" style="float: right;line-height: 60px">
            <router-link to="/login">
        <span style="margin-right: 20px">
          Login
        </span>
            </router-link>
            <router-link to="/register">
        <span style="margin-right: 40px">
          Register
        </span>
            </router-link>
        </div>
        <div v-else style="float: right;">
            <el-dropdown style="margin-right: 40px;cursor: pointer" trigger="click">
        <span class="el-dropdown-link">
          <span style="margin-right: 10px; font-size: 18px">
            <el-icon><Avatar/></el-icon>
          </span>
          <span style="line-height: 60px; font-size: 16px">
            {{ user.name }}
          </span>
        </span>
                <template #dropdown>
                    <el-dropdown-menu>
                        <el-dropdown-item @click="gotoUserInfo">
                            <el-icon>
                                <UserFilled/>
                            </el-icon>
                            UserInfo
                        </el-dropdown-item>
                        <el-dropdown-item divided @click="logout">
                            <el-icon>
                                <SwitchButton/>
                            </el-icon>
                            Logout
                        </el-dropdown-item>
                    </el-dropdown-menu>
                </template>
            </el-dropdown>
        </div>
    </div>
</template>

<script setup>
import logo from "../assets/logo.png";
import {onMounted, ref} from "vue";
import {Avatar, SwitchButton, UserFilled} from "@element-plus/icons-vue";
import UserAPI from "../api/UserAPI.js";

let login = ref(false)
let user = ref({})

const toHomePage = () => {
  window.location.href = "/home";
}

const gotoUserInfo = () => {
  //跳转用户信息页面
  window.location.href = "/user/info";
}

const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user_id')
  localStorage.removeItem('problem_id')
  localStorage.removeItem('answer_id')
  login.value = false
  toHomePage()
}

onMounted(() => {
  if (localStorage.getItem('token') != null) {

    UserAPI.getInfo(localStorage.getItem('token')).then(res => {
      if (res.data.code === 200) {
        login.value = true
        user.value = res.data.data.user
      }
    }).catch(err => {
      console.log(err)
    })
  }
})
</script>

<script>
export default {
  name: "Header"
}
</script>

<style scoped>
a {
    text-decoration: none;
}
</style>
