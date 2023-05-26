<template>
    <div style="height: 100vh">
        <el-container style="height: 100%;">
            <el-header style="padding: 0;">
                <Header />
            </el-header>
            <el-container>
                <el-container class="main-container">
                    <el-main>
                        <el-card style="margin-left: 5%; width: 90%;">
                            <el-row>
                                <el-col :span="10">
                                    <div style="margin-top: 120px;"></div>
                                    <div style="text-align: center">
                                        <el-image style="margin-top: 10%" :src="logo" />
                                    </div>
                                    <div style="margin-top: 40px;"></div>
                                    <div class="welcome">Welcome</div>
                                    <div class="welcome">to</div>
                                    <div class="welcome">WitFuzz</div>
                                </el-col>
                                <el-col :span="14">
                                    <div style="margin-top: 40px;"></div>
                                    <div style="text-align: center;font-weight: bold;font-size: 40px; ">
                                        Sign Up
                                    </div>
                                    <div style="margin-top: 10px" />
                                    <el-form ref="mailRef" :inline="true" :model="mail" :label-position="right"
                                        :rules="rules" status-icon>
                                        <el-form-item label="E-mail" prop="email"
                                            style="font-size: 15px; margin-left: 5%; margin-top: 10px; margin-bottom: 10px; width: 65%;">
                                            <el-input v-model="mail.email" :prefix-icon="Postcard"
                                                style="font-size: 15px" />
                                        </el-form-item>
                                        <el-button type="primary" @click="sendCode(mailRef)">Send
                                            Code</el-button>
                                    </el-form>
                                    <div style="margin-top: 10px" />
                                    <el-form ref="codeRef" :inline="true" :model="code" :label-position="right"
                                        :rules="rules" status-icon>
                                        <el-form-item label="Code" prop="code"
                                            style="font-size: 15px; margin-left: 5%; margin-top: 10px; margin-bottom: 10px; width: 65%;">
                                            <el-input v-model="code.code" :prefix-icon="Grid" style="font-size: 15px" />
                                        </el-form-item>
                                        <el-button type="primary" @click="verifyCode(codeRef)"
                                            :disabled="!valid_mail && !verify_mail">Verify</el-button>
                                    </el-form>
                                    <el-form ref="userRef" label-position="top" :model="user" :rules="rules" status-icon>
                                        <el-form-item label="Name" prop="name" class="info">
                                            <el-input v-model="user.name" :prefix-icon="User" maxlength="30" show-word-limit
                                                style="font-size: 15px;" />
                                        </el-form-item>
                                        <el-form-item label="Password" prop="password" class="info">
                                            <el-input v-model="user.password" clearable type="password" showpassword
                                                :prefix-icon="Grid" style="font-size: 15px" />
                                        </el-form-item>
                                        <el-form-item label="Confirm password" prop="password_re" class="info">
                                            <el-input v-model="user.password_re" clearable type="password" showpassword
                                                :prefix-icon="Grid" style="font-size: 15px" />
                                        </el-form-item>
                                        <el-form-item label="Birthday" prop="birthday" class="info">
                                            <el-date-picker v-model="user.birthday" type="date" :prefix-icon="Calendar"
                                                style="font-size: 15px" />
                                        </el-form-item>
                                        <el-form-item label="Job" prop="job" class="info">
                                            <el-input v-model="user.job" :prefix-icon="Suitcase" maxlength="30"
                                                show-word-limit style="font-size: 15px" />
                                        </el-form-item>
                                        <el-form-item label="Introduction" prop="intro" class="info">
                                            <el-input v-model="user.intro" :rows="4" type="textarea" maxlength="250"
                                                show-word-limit style="font-size: 15px" />
                                        </el-form-item>
                                    </el-form>
                                    <div style="margin-top: 20px" />
                                    <el-row>
                                        <span style="margin-left: 32.5%;"></span>
                                        <el-button type="primary" @click="validate(userRef)" style="width: 15%"
                                            :disabled="!valid_code && !verify_code">Submit</el-button>
                                        <span style="margin-left: 5%;"></span>
                                        <el-button @click="toHomePage" style="width: 15%">Cancel</el-button>
                                    </el-row>
                                    <div style="margin-top: 20px" />
                                    <el-alert v-if="success" title="Success!" type="success" center
                                        show-icon />
                                    <el-alert v-if="fail" title="Failed!" :description=fail_message type="error"
                                        center show-icon />
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
import { User, Postcard, Grid, Calendar, Suitcase } from "@element-plus/icons-vue";

import { ref, reactive } from 'vue';
import { FormInstance, FormRules } from 'element-plus';

import UserAPI from "../../api/UserAPI";

import logo from "../../assets/logo.png"
import { right } from "@popperjs/core";

const userRef = ref<FormInstance>()

const mailRef = ref<FormInstance>()

const mail = reactive({
    email: '',
})

const codeRef = ref<FormInstance>()

const code = reactive({
    code: '',
})

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
const validatePass_re = (rule: any, value: any, callback: any) => {
    if (value === '') {
        callback(new Error('Please input the password again'))
    } else if (value !== user.password) {
        callback(new Error("Two inputs don't match!"))
    } else {
        callback()
    }
}

const user = reactive({
    name: '',
    password: '',
    password_re: '',
    intro: 'Welcome to WitFuzz',
    birthday: '',
    job: ''
})

const rules = reactive<FormRules>({
    name: [
        { required: true, message: 'Please input name', trigger: 'blur' },
        { min: 3, max: 30, message: 'Length should be 3 to 30', trigger: 'blur' },
    ],
    email: [
        {
            type: 'email',
            required: true,
            message: 'Please input vaild e-mail address',
            trigger: 'blur',
        },
    ],
    code: [
        { required: true, message: 'Please input code', trigger: 'blur' },
        { min: 6, max: 6, message: 'Length should be 6', trigger: 'blur' },
    ],
    password: [{ required: true, validator: validatePass, trigger: 'blur' }],
    password_re: [{ required: true, validator: validatePass_re, trigger: 'blur' }],
});

let valid_user = ref(false)
let valid_code = ref(false)
let valid_mail = ref(false)
let verify_mail = ref(false)
let verify_code = ref(false)
let success = ref(false)
let fail = ref(false)
let fail_message = ref('')

const sendCode = async (mailRef) => {
    await submitForm(mailRef, 'mail')
    if (valid_mail.value) {
        UserAPI.sendVerifyCode(mail.email).then(res => {
            console.log(res)
            if (res.data.data.result) {
                console.log('valid')
                success.value = true
                verify_mail.value = true
            }
            else {
                console.log('invalid')
                fail.value = true
                fail_message.value = 'User not exist!'
            }
        })
    }
}

const verifyCode = async (codeRef) => {
    await submitForm(codeRef, 'code')
    if (valid_code.value) {
        UserAPI.modifyPasswordVerify(mail.email, code.code).then(res => {
            console.log(res)
            if (res.data.data.result) {
                console.log('valid')
                success.value = true
                verify_code.value = true
            }
            else {
                console.log('invalid')
                fail.value = true
                fail_message.value = 'Wrong verify code!'
            }
        })
    }
}

const validate = async (userRef) => {
    await submitForm(userRef, 'user')
    if (valid_user.value) {
        UserAPI.register(mail.email, user.name, user.password, user.intro, user.birthday, user.job).then(res => {
            console.log(res)
            if (res.data.data.result) {
                console.log('valid')
                success.value = true
                setTimeout(toLogin, 2000)
            }
            else {
                console.log('invalid')
                fail.value = true
                fail_message.value = 'Infomation might be used!'
            }
        })
    }

}

const submitForm = async (formEl, phase) => {
    if (!formEl) return
    await formEl.validate((valid, fields) => {
        if (valid) {
            console.log('submit!')
            if (phase === 'user') {
                valid_user.value = true
            }
            else if (phase === 'code') {
                valid_code.value = true
            }
            else if (phase === 'mail') {
                valid_mail.value = true
            }
        } else {
            console.log('error submit!', fields)
        }
    })
}

const toHomePage = () => {
    window.location.href = "/home";
}

const toLogin = () => {
    window.location.href = "/login";
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
