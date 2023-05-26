<template>
    <div style="margin-left: 2%; margin-right: 2%; ">
        <RecordList listType="record"/>
    </div>
</template>

<script setup>
import RecordList from "./RecordList.vue";

</script>

<script>
export default {
    name: "TaskRecord",
    components: {
        RecordList
    }
}
</script>

<style scoped>

</style>
