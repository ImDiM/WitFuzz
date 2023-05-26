<template>
    <div style="text-align: center;font-weight: bold;font-size: 40px; margin-top: 20px">
        WitFuzz
    </div>
    <div style="text-align: center;margin-top: 30px">
    <span style="margin-right: 40px">
      <el-image style="width: 100px;height: 100px" :src="bug2" alt="logo" />
    </span>
        <el-image style="width: 100px;height: 100px" :src="logo" alt="logo" />
        <span style="margin-left: 40px">
      <el-image style="width: 100px;height: 100px" :src="bug1" alt="logo" />
    </span>
    </div>
    <div style="margin-top: 40px;margin-left: 15%;margin-right: 15%;line-height: 24px;letter-spacing: 1px">
        <p v-for="paragraph in paragraphs">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{{ paragraph }}</p>
    </div>
</template>

<script setup>
import logo from "../../assets/logo.png";
import bug1 from "../../assets/bug1.png";
import bug2 from "../../assets/bug2.png";

const paragraphs = [
    'Security vulnerability is one of the root causes of cyber-security threats. To discover vulnerabilities and fix them in advance, researchers have proposed several techniques, among which fuzzing is the most widely used one.',
    'The core idea of ​​fuzz testing is to automatically or semi-automatically generate random data input into the program, and monitor program exceptions, such as crashes, assertion failures, etc., to find possible program errors, such as memory leaks. Nowadays, the requirements for the robustness of programs and models are getting higher and higher, and people need a tool that can check the security of their software conveniently and quickly. At this stage, there are few open source frameworks for fuzz testing based on deep learning, and they have not been maintained and upgraded for a long time. WitFuzz aims to upgrade and integrate these basic open source frameworks, display them to users with a graphical interface, and add community Discussion function.',
    'Not support multiprocess / multithread.'
]

</script>

<script>

export default {
    name: "Home"
}
</script>

<style scoped>

</style>
