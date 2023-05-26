<template>
  <div style="height: 100vh">
    <el-container style="height: 100%;">
      <el-header style="padding: 0;">
        <Header />
      </el-header>
      <el-container>
        <el-container class="main-container">
          <el-main>
            <div style="margin-top: 150px;"/>
            <el-card style="margin: auto; width: 600px;">
              <el-row>
                <el-col :span="10">
                  <div style="text-align: center">
                    <el-image style="margin-top: 40px; width: 60px;" :src="logo" />
                  </div>
                  <div style="margin-top: 20px;"></div>
                  <div class="welcome">Welcome</div>
                  <div class="welcome">to</div>
                  <div class="welcome">WitFuzz</div>
                </el-col>
                <el-col :span="14">
                  <div style="margin-top: 40px;"></div>
                  <div style="text-align: center;font-weight: bold;font-size: 40px; ">
                    Sign In
                  </div>
                  <el-form ref="userRef" label-position="top" :model="user" :rules="rules" status-icon>
                    <el-form-item label="E-mail" prop="email" class="info">
                      <el-input v-model="user.email" :prefix-icon="Postcard" style="font-size: 15px" />
                    </el-form-item>
                    <el-form-item label="Password" prop="password" class="info">
                      <el-input v-model="user.password" clearable type="password" showpassword :prefix-icon="Grid"
                        style="font-size: 15px" />
                    </el-form-item>
                  </el-form>
                  <div style="margin-top: 30px" />
                  <div style="text-align: center;">
                    <el-button type="primary" @click="validate(userRef)" style="width: 15%">Login</el-button>
                  </div>
                  <router-link to="/retrieve">
                    <div style="margin-right: 20px; text-align: center; margin-top: 10px;">
                      Forget Password
                    </div>
                  </router-link>
                  <div style="margin-top: 20px" />
                  <el-alert v-if="success" title="Successfully login!" type="success" center show-icon />
                  <el-alert v-if="fail" title="Invaild information!" type="error" center show-icon />
                </el-col>
              </el-row>
            </el-card>
          </el-main>
          <el-footer style="background-color: #f3f3f3;font-size: 12px;line-height: 40px;height: 40px">
            <Footer />
          </el-footer>
        </el-container>
      </el-container>
    </el-container>
    </div>
</template>

<script lang="ts" setup>
import Header from "../Header.vue";
import Footer from "../Footer.vue";
import { Postcard, Grid } from "@element-plus/icons-vue";

import { ref, reactive } from 'vue';
import { FormInstance, FormRules } from 'element-plus';

import UserAPI from "../../api/UserAPI";

import logo from "../../assets/logo.png"

const userRef = ref<FormInstance>()

const validatePass = (rule: any, value: any, callback: any) => {
    if (value === '') {
        callback(new Error('Please input the password'))
    } else {
        if (user.password !== '') {
            if (!userRef.value) return
            userRef.value.validateField('user.password', () => null)
        }
        callback()
    }
}

const user = reactive({
    email: '',
    password: '',
})

const rules = reactive<FormRules>({
    email: [
        {
            type: 'email',
            required: true,
            message: 'Please input vaild e-mail address',
            trigger: 'blur',
        },
    ],
    password: [{ required: true, validator: validatePass, trigger: 'blur' }],
});

let valid_form = ref(false)
let success = ref(false)
let fail = ref(false)

const validate = async (userRef) => {
    await submitForm(userRef)
    if (valid_form.value) {
        UserAPI.login(user.email, user.password).then(res => {
            console.log(res)
            if (res.data.data.result) {
                console.log('valid')
                success.value = true

                localStorage.setItem('token', res.data.data.token)
                localStorage.setItem('user_id', res.data.data.user_id)

                setTimeout(toHomePage, 2000)
            }
            else {
                console.log('invalid')
                fail.value = true
            }
        })
    }

}

const submitForm = async (formEl: FormInstance | undefined) => {
    if (!formEl) return
    await formEl.validate((valid, fields) => {
        if (valid) {
            console.log('submit!')
            valid_form.value = true
        } else {
            console.log('error submit!', fields)
        }
    })
}

const toHomePage = () => {
    window.location.href = "/home";
}

</script>

<script lang="ts">
export default {
}
</script>

<style scoped>
.welcome {
    text-align: center;
    font-weight: bold;
    font-size: 30px;
    margin-top: 10px;
}

.info {
    font-size: 15px;
    margin-left: 5%;
    margin-top: 10px;
    margin-bottom: 10px;
    width: 90%;
}
</style>
