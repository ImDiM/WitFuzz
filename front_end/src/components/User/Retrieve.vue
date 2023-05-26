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
                        <el-card style="margin: auto; width: 800px;">
                            <el-row>
                                <el-col :span="6">
                                    <div style="text-align: center">
                                        <el-image style="margin-top: 80px; width: 30%;" :src="logo" />
                                    </div>
                                    <div style="margin-top: 40px;"></div>
                                    <div class="welcome">Welcome</div>
                                    <div class="welcome">to</div>
                                    <div class="welcome">WitFuzz</div>
                                </el-col>
                                <el-col :span="18">
                                    <div style="margin-top: 40px;"></div>
                                    <div style="text-align: center;font-weight: bold;font-size: 30px; ">
                                        Retrieve Password
                                    </div>
                                    <div style="margin-top: 40px;"></div>
                                    <el-form ref="userRef" :inline="true" :model="user" :label-position="right"
                                             label-width="150px" :rules="rules" status-icon>
                                        <el-form-item label="E-mail" prop="email" style="font-size: 15px; width: 70%;">
                                            <el-input v-model="user.email" :prefix-icon="Postcard"
                                                      style="font-size: 15px" />
                                        </el-form-item>
                                        <el-form-item>
                                            <el-button type="primary" @click="sendCode(userRef)" class="button">Send Code</el-button>
                                        </el-form-item>
                                    </el-form>
                                    <div style="margin-top: 10px" />
                                    <el-form ref="codeRef" :inline="true" :model="code" :label-position="right"
                                             label-width="150px" :rules="rules" status-icon>
                                        <el-form-item label="Code" prop="code" style="font-size: 15px; width: 70%;">
                                            <el-input v-model="code.code" :prefix-icon="Grid" style="font-size: 15px" />
                                        </el-form-item>
                                        <el-form-item>
                                            <el-button type="primary" @click="verifyCode(codeRef)" class="button" :disabled="!valid_user && !verify_user">Verify</el-button>
                                        </el-form-item>
                                    </el-form>
                                    <div style="margin-top: 10px" />
                                    <el-form ref="passRef" :inline="true" :model="pass" :label-position="right"
                                             label-width="150px" :rules="rules" status-icon>
                                        <el-form-item label="Password" prop="password" style="font-size: 15px; width: 70%;">
                                            <el-input v-model="pass.password" clearable type="password" showpassword
                                                      :prefix-icon="Grid" style="font-size: 15px" />
                                        </el-form-item>
                                        <div style="margin-top: 10px" />
                                        <el-form-item label="Confirm password" prop="password_re"
                                                      style="font-size: 15px; width: 70%;">
                                            <el-input v-model="pass.password_re" clearable type="password" showpassword
                                                      :prefix-icon="Grid" style="font-size: 15px" />
                                        </el-form-item>
                                    </el-form>
                                    <div style="text-align: center;">
                                        <div style="margin-top: 10px" />
                                        <el-button type="primary" @click="modifyPassword(passRef)" :disabled="!valid_code && !verify_code">Modify
                                            Password</el-button>
                                    </div>
                                    <div style="margin-top: 20px" />
                                    <el-alert v-if="success" title="Success!" type="success" center show-icon />
                                    <el-alert v-if="fail" title="Failed!" :description=fail_message type="error" center show-icon />
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
import { right } from "@popperjs/core";

const userRef = ref<FormInstance>()

const user = reactive({
    email: '',
})

const codeRef = ref<FormInstance>()

const code = reactive({
    code: '',
})

const passRef = ref<FormInstance>()

const pass = reactive({
    password: '',
    password_re: '',
})


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

const rules = reactive<FormRules>({
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
let verify_user = ref(false)
let verify_code = ref(false)
let valid_pass = ref(false)
let success = ref(false)
let fail = ref(false)
let fail_message = ref('')

const sendCode = async (userRef) => {
    await submitForm(userRef, 'user')
    if (valid_user.value) {
        UserAPI.sendVerifyCode(user.email).then(res => {
            console.log(res)
            if (res.data.data.result) {
                console.log('valid')
                success.value = true
                valid_user.value = true
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
        UserAPI.modifyPasswordVerify(user.email, code.code).then(res => {
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

const modifyPassword = async (passRef) => {
    await submitForm(passRef, 'pass')
    if (valid_pass.value) {
        UserAPI.modifyPassword(user.email, pass.password).then(res => {
            console.log(res)
            if (res.data.data.result) {
                console.log('valid')
                success.value = true
                setTimeout(toLogin, 2000)
            }
            else {
                console.log('invalid')
                fail.value = true
                fail_message.value = 'Password cannot be the same with the prior!'
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
            else if (phase === 'pass') {
                valid_pass.value = true
            }
        } else {
            console.log('error submit!', fields)
        }
    })
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

.button {
    width: 80px;
}
</style>
