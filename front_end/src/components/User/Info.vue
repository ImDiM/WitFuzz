<template>
    <div style="height: 100vh">
        <el-container style="height: 100%;">
            <el-header style="padding: 0;">
                <Header />
            </el-header>
            <el-container>
                <el-aside width="200px">
                    <Sider />
                </el-aside>
                <el-container class="main-container">
                    <el-main>
                        <div style="margin-top: 20px;"></div>
                        <div style="text-align: center;font-weight: bold;font-size: 40px; ">
                            My Profile
                        </div>
                        <el-form ref="userRef" label-position="top" :model="user" :rules="rules" status-icon>
                            <el-form-item label="Name" prop="name" class="info">
                                <el-input v-model="user.name" :prefix-icon="User" maxlength="30" show-word-limit
                                          style="font-size: 15px;" />
                            </el-form-item>
                            <el-form-item label="Birthday" prop="birthday" class="info">
                                <el-date-picker v-model="user.birthday" type="date" :prefix-icon="Calendar"
                                                style="font-size: 15px" />
                            </el-form-item>
                            <el-form-item label="Job" prop="job" class="info">
                                <el-input v-model="user.job" :prefix-icon="Suitcase" maxlength="30" show-word-limit
                                          style="font-size: 15px" />
                            </el-form-item>
                            <el-form-item label="Introduction" prop="intro" class="info">
                                <el-input v-model="user.intro" :rows="4" type="textarea" maxlength="250" show-word-limit
                                          style="font-size: 15px" />
                            </el-form-item>
                        </el-form>
                        <el-button type="primary" @click="modifyInfo(userRef)" style="width: 20%; margin-left: 40%;">Modify Information</el-button>
                        <div style="margin-top: 40px;"></div>
                        <el-form ref="passRef" label-position="top" :model="pass" :rules="rules" status-icon>
                            <el-form-item label="Password" prop="password" class="info">
                                <el-input v-model="pass.password" clearable type="password" showpassword :prefix-icon="Grid"
                                          style="font-size: 15px" />
                            </el-form-item>
                            <el-form-item label="Confirm password" prop="password_re" class="info">
                                <el-input v-model="pass.password_re" clearable type="password" showpassword
                                          :prefix-icon="Grid" style="font-size: 15px" />
                            </el-form-item>
                        </el-form>
                        <el-button type="primary" @click="modifyPass(userRef)" style="width: 20%; margin-left: 40%;">Modify Password</el-button>
                        <div style="margin-top: 20px" />
                        <el-alert v-if="success" title="Success!" type="success" center show-icon />
                        <el-alert v-if="fail" title="Failed!" type="error" center show-icon />
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
import Sider from "../Sider.vue";
import Footer from "../Footer.vue";
import { User, Postcard, Grid, Calendar, Suitcase } from "@element-plus/icons-vue";

import { ref, reactive, onMounted } from 'vue';
import { FormInstance, FormRules } from 'element-plus';

import UserAPI from "../../api/UserAPI";
import { timePanelSharedProps } from "element-plus/es/components/time-picker/src/props/shared";

let login = ref(false)
let user_info = ref({})
let valid_form = ref(false)
let success = ref(false)
let fail = ref(false)

let user = reactive({
    name: '',
    intro: '',
    birthday: '',
    job: '',
})

onMounted(() => {
    if (localStorage.getItem('token') != null) {

        UserAPI.getInfo(localStorage.getItem('token')).then(res => {
            if (res.data.code === 200) {
                login.value = true
                user_info.value = res.data.data.user
                user.name = user_info.value.name
                user.intro = user_info.value.intro
                user.birthday = user_info.value.birthday
                user.job = user_info.value.job
            }
        }).catch(err => {
            console.log(err)
        })
    }
})

const userRef = ref<FormInstance>()
const passRef = ref<FormInstance>()

const validatePass = (rule: any, value: any, callback: any) => {
    if (value === '') {
        callback(new Error('Please input the password'))
    } else {
        if (pass.password !== '') {
            if (!userRef.value) return
            userRef.value.validateField('user.password', () => null)
        }
        callback()
    }
}

const validatePass_re = (rule: any, value: any, callback: any) => {
    if (value === '') {
        callback(new Error('Please input the password again'))
    } else if (value !== pass.password) {
        callback(new Error("Two inputs don't match!"))
    } else {
        callback()
    }
}

const pass = reactive({
    password: '',
    password_re: '',
})

const rules = reactive<FormRules>({
    name: [
        { required: true, message: 'Please input name', trigger: 'blur' },
        { min: 3, max: 30, message: 'Length should be 3 to 30', trigger: 'blur' },
    ],
    password: [{ required: true, validator: validatePass, trigger: 'blur' }],
    password_re: [{ required: true, validator: validatePass_re, trigger: 'blur' }],
});

const reset = () => {
    success.value = false
    fail.value = false
}

const modifyInfo = async (userRef) => {
    await submitForm(userRef)
    if (valid_form.value) {
        UserAPI.modifyInfo(user.name, user.intro, user.job, user.birthday).then(res => {
            console.log(res)
            if (res.data.data.result) {
                console.log('valid')
                success.value = true
                setTimeout(reset, 2000)
            }
            else {
                console.log('invalid')
                fail.value = true
                setTimeout(reset, 2000)
            }
        })
    }

}

const modifyPass = async (passRef) => {
    await submitForm(passRef)
    if (valid_form.value) {
        UserAPI.modifyPassword(user_info.value.email, pass.password).then(res => {
            console.log(res)
            if (res.data.data.result) {
                console.log('valid')
                success.value = true
                setTimeout(reset, 2000)
            }
            else {
                console.log('invalid')
                fail.value = true
                setTimeout(reset, 2000)
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

</script>

<script lang="ts">
export default {
}
</script>

<style scoped></style>
