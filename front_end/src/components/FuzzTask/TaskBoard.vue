<template>
    <div style="margin-left: 2%; margin-right: 2%; ">
        <RecordList listType="board"/>
    </div>
</template>

<script setup>

import RecordList from "./RecordList.vue";
</script>

<script>
export default {
    name: "Taskboard",
    components: {
        RecordList
    }
}
</script>

<style scoped>

</style>
