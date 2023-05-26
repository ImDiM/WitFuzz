<template>
    <div v-loading="submitDescriptionLoading" style="margin-top: 60px; margin-left: 8%; margin-right: 8%; margin-bottom: 30px">
        <mavon-editor v-model="submitDescription" defaultOpen="preview" :subfield="false" :editable="false" :toolbarsFlag="false" style="height: 100%; margin-top: 20px;"/>

        <div style="margin-top: 50px;">
            <el-divider content-position="left">
                <span class="submit-title">Submit Config</span>
            </el-divider>
            <el-input :disabled="submitLoading" autosize type="textarea" v-model="submitConfig" @change="onChangeSubmitConfig"/>
            <el-divider content-position="left">
                <span class="submit-title">Submit Description</span>
            </el-divider>
            <el-input :disabled="submitLoading" autosize type="textarea" v-model="description" maxlength="1024" show-word-limit/>
            <el-divider content-position="left">
                <span class="submit-title">Is Public</span>
            </el-divider>
            <el-switch
                v-model="is_public"
                :disabled="submitLoading"
                active-text="Public"
                inactive-text="Private"
            />
            <el-divider content-position="left">
                <span class="submit-title">Upload File</span>
            </el-divider>
            <el-upload
                ref="uploadRef"
                :disabled="submitLoading"
                drag
                :auto-upload="false"
                :limit="1"
                :on-exceed="handleExceed"
                :http-request="handleSubmit"
                :file-list="fileList"
                :on-change="handleFileChange"
            >
                <el-icon class="el-icon--upload"><upload-filled /></el-icon>
                <div class="el-upload__text">
                    Drop file here or <em>click to upload</em>
                </div>
                <template #tip>
                    <div class="el-upload__tip">
                        file size less than 1MB will be uploaded
                    </div>
                </template>
            </el-upload>
            <el-button :loading="submitLoading" type="primary" size="large" style="margin-top: 20px" @click="submitFuzz">submit</el-button>
        </div>
    </div>
</template>

<script setup>
import {onMounted, ref} from 'vue'
import { UploadFilled } from '@element-plus/icons-vue'
import {mavonEditor} from "mavon-editor";
import 'mavon-editor/dist/css/index.css'
import TaskAPI from "../../api/TaskAPI.js";
import {useRoute} from "vue-router";

const route = useRoute();
const taskId = route.params.id
let task_name = ref('')
let submitDescription = ref('')
let submitDescriptionLoading = ref(true)
let submitLoading = ref(false)
let submitConfig = ref('')
let allowedFileTypes = ref([])
let description = ref('')
let config_str = ref()
let is_public = ref(true)
let fileList = ref([])

const uploadRef = ref()

onMounted(() => {
    TaskAPI.getTaskSubmitDescription(taskId).then(res => {
        submitDescription.value = res.data.data.submit_description
        task_name.value = res.data.data.task_name
        submitDescriptionLoading.value = false;
        submitConfig.value = res.data.data.default_config
        allowedFileTypes.value = res.data.data.allowed_file_types.split(',')
    }).catch(err => {
        submitDescriptionLoading.value = false;
        console.log(err)
    })
})

const handleExceed = (files) => {
    uploadRef.value.clearFiles()
    const file = files[0]
    uploadRef.value.handleStart(file)
}

const onChangeSubmitConfig = () => {}

const handleSubmit = (fileObject) => {
    const file = fileObject.file
    let i = file.name.indexOf('.');
    const fileName = file.name.substring(0, i);
    let fileType = ''
    if (i>0 && i<file.name.length){
        fileType = file.name.substring(i+1);
    }
    if (allowedFileTypes.value.indexOf(fileType) === -1) {
        ElNotification({
            title: 'Error',
            message: 'File type not allowed',
            type: 'error',
        })
        return
    }
    if (file.size > 1024*1024) {
        ElNotification({
            title: 'Error',
            message: 'File size should be less than 1MB',
            type: 'error',
        })
        return
    }

    submitLoading.value = true
    let data = new FormData();
    data.append('file', file);
    data.append('file_name', fileName);
    data.append('file_type', fileType);
    data.append('description', description.value);
    data.append('config_str', submitConfig.value);
    data.append('is_public', is_public.value);
    data.append('task_name', task_name.value);

    TaskAPI.submitFuzz(taskId, data).then(res => {
        submitLoading.value = false
        if (res.data.data.result) {
            ElNotification({
                title: 'Success',
                message: 'Submit Success',
                type: 'success',
            })
            onSubmitSuccess()
        } else {
            ElNotification({
                title: 'Error',
                message: 'Submit Error',
                type: 'error',
            })
        }
    }).catch(err => {
        submitLoading.value = false
    })
}

const onSubmitSuccess = () => {
    // submitConfig.value = '{}'
    // description.value = ''
    //uploadRef.value.clearFiles()
    //fileList.value = []
}


const handleFileChange = (UploadFile) => {
    fileList.value = [UploadFile]
}

const checkData = () => {
    if (submitConfig.value === '') {
        submitConfig.value = '{}'
    }
    try {
        config_str.value = JSON.parse(submitConfig.value)
    } catch (JSONParseError) {
        ElNotification({
            title: 'Error',
            message: 'Submit Config is not a valid JSON',
            type: 'error',
        })
        return false
    }
    if (fileList.value.length === 0) {
        ElNotification({
            title: 'Error',
            message: 'Please upload a file',
            type: 'error',
        })
    }
    return true
}

const submitFuzz = () => {
    if (checkData()) {
        uploadRef.value.submit()
    }
}

</script>

<script>
export default {
    name: "SubmitTask"
}
</script>

<style>
.submit-title {
    font-size: 14px;
    font-weight: bold;
}
</style>
