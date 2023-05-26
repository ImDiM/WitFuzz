<template>
    <div>
        <div style="margin-top: 10px;text-align: center">
            <span style="font-size: 18px;font-weight: bold;">{{listType}}</span>
            <span>
                <el-tooltip content="refresh list">
                    <el-button style="float: right;margin-right: 20px" :disabled="recordListLoading" size="large" type="primary" :icon="RefreshLeft" circle @click="updateRecordList"/>
                </el-tooltip>
            </span>
        </div>

        <el-table
                @row-click="onRowClick"
                :data="tableData"
                style="width: 100%;margin-top: 30px;"
                v-loading="recordListLoading"
                :row-class-name="tableRowClassName"
                class="record-table"
        >
            <el-table-column prop="status" label="Status" width="100">
                <template #default="scope">
                    <el-tag v-if="scope.row.status === 'finished'" type="success">
                        {{scope.row.status}}
                    </el-tag>
                    <el-tag v-else-if="scope.row.status === 'failed'" type="danger">
                        {{scope.row.status}}
                    </el-tag>
                    <el-tag v-else-if="scope.row.status === 'running'" type="warning">
                        {{scope.row.status}}
                    </el-tag>
                    <el-tag v-else type="info">
                        {{scope.row.status}}
                    </el-tag>
                </template>
            </el-table-column>

            <el-table-column prop="submitted_at" label="SubmittedAt" width="114"/>
            <el-table-column prop="started_at" label="StartedAt" width="114"/>
            <el-table-column prop="finished_at" label="FinishedAt" width="114"/>
            <el-table-column prop="running_time" label="RunningTime" width="119"/>
            <el-table-column prop="config_str" label="Config" width="200"/>
            <el-table-column prop="description" label="Description" min-width="200"/>

            <el-table-column v-if="listType==='record'" fixed="right" label="Operations" width="110">
                <template #default="scope">
                    <el-tooltip content="Delete record">
                      <el-popconfirm title="Are you sure to delete this record?" @confirm="deleteRecord(scope.$index, scope.row.id)">
                          <template #reference>
                              <el-button :loading="deleteLoading[scope.$index]" :disabled="scope.row.status !== 'finished' && scope.row.status !== 'failed'" @click.stop="clickStop" type="danger" :icon="Delete" circle/>
                          </template>
                      </el-popconfirm>
                    </el-tooltip>
                    <el-tooltip v-if="scope.row.is_public" content="Set record as private">
                      <el-button :loading="setPublicPrivateLoading[scope.$index]" @click.stop="setAsPrivate(scope.$index, scope.row.id)" type="info" :icon="Hide" circle/>
                    </el-tooltip>
                    <el-tooltip v-else content="Set record as public">
                      <el-button :loading="setPublicPrivateLoading[scope.$index]" @click.stop="setAsPublic(scope.$index, scope.row.id)" type="primary" :icon="View" circle/>
                    </el-tooltip>
                </template>
            </el-table-column>
        </el-table>
        <div style="margin-top: 10px;margin-bottom: 10px;">
            <el-pagination layout="prev, pager, next" :page-size="pageSize" :total="totalNumber" @current-change="handleCurrentChange"/>
        </div>

        <el-drawer
                v-model="drawer"
                size="50%"
                direction="rtl"
                v-loading="drawerLoading"
        >
            <template #header>
        <span>
          <el-tag size="large" v-if="currentRecord.status === 'finished'" type="success">
            {{currentRecord.status}}
          </el-tag>
          <el-tag size="large" v-else-if="currentRecord.status === 'failed'" type="danger">
            {{currentRecord.status}}
          </el-tag>
          <el-tag size="large" v-else-if="currentRecord.status === 'running'" type="warning">
            {{currentRecord.status}}
          </el-tag>
          <el-tag size="large" v-else type="info">
            {{currentRecord.status}}
          </el-tag>
        </span>
            </template>
            <template #default>
                <el-divider>
          <span class="drawer-divider-title">
            Time Line
          </span>
                </el-divider>
                <el-card shadow="hover">
                    <el-timeline>
                        <el-timeline-item
                                v-for="(item, index) in currentTimeLine"
                                :key="index"
                                :timestamp="item.timestamp"
                                :type="item.type"
                        >
                            {{item.content}}
                        </el-timeline-item>
                    </el-timeline>
                </el-card>
                <el-divider>
          <span class="drawer-divider-title">
            Running Time
          </span>
                </el-divider>
                <el-card shadow="hover">
                    <p>{{currentRecord.running_time}}</p>
                </el-card>
                <el-divider>
          <span class="drawer-divider-title">
            Submit Description
          </span>
                </el-divider>
                <el-card shadow="hover">
                    <p>{{currentRecord.description}}</p>
                </el-card>
                <el-divider>
          <span class="drawer-divider-title">
            Config
          </span>
                </el-divider>
                <el-card shadow="hover">
                    <p>{{currentRecord.config_str}}</p>
                </el-card>
                <el-divider>
          <span class="drawer-divider-title">
            Download Result
          </span>
                </el-divider>
                <el-button :loading="downloadResultLoading" :disabled="currentRecord.status !=='finished'" @click="downloadResultFile">Download result.zip</el-button>
                <el-divider>
                    <span class="drawer-divider-title">
                        Submit File
                    </span>
                </el-divider>
                <el-button :loading="downloadSubmitFileLoading" @click="downloadSubmitFile">Download {{currentRecord.file_name}}</el-button>
                <el-divider>
                    <span class="drawer-divider-title">
                        Out
                    </span>
                </el-divider>
                <el-card shadow="hover" style="overflow: auto; max-height: 800px">
                    <pre>{{currentRecord.out}}</pre>
                </el-card>
                <el-divider>
                    <span class="drawer-divider-title">
                        Err
                    </span>
                </el-divider>
                <el-card shadow="hover" style="overflow: auto; max-height: 800px">
                    <pre>{{currentRecord.err}}</pre>
                </el-card>
                <el-divider/>
            </template>
        </el-drawer>
    </div>
</template>

<script setup>
import {onMounted, ref} from "vue";
import {useRoute} from "vue-router";
import RecordAPI from "../../api/RecordAPI.js";
import {Delete, View, Hide, RefreshLeft} from "@element-plus/icons-vue";

const props = defineProps({
  listType: {
    type: String,
    default: 'board'
  }
})

const route = useRoute();
const taskId = route.params.id;
const publicOnly = props.listType === 'board'

let tableData = ref([]);
let pageSize = ref(10);
let pageNumber = ref(1);
let orderBy = ref('submitted_at');
let orderType = ref('desc')
let totalNumber = ref(0);
let drawer = ref(false);
let drawerLoading = ref(false);
let recordListLoading = ref(false);

let currentRecord = ref({})
let currentTimeLine = ref([])

let setPublicPrivateLoading = ref([])
let deleteLoading = ref([])

let downloadResultLoading = ref(false)
let downloadSubmitFileLoading = ref(false)

const tableRowClassName = ({row, rowIndex}) => {
  return row.status;
}

const setAsPublic = (index, recordId) => {
  setPublicPrivateLoading.value[index] = true
  RecordAPI.setRecordAsPublic(recordId).then(res => {
    if (res.data.data.result) {
      updateRecordList()
    }
    setPublicPrivateLoading.value[index] = false
  }).catch(err => {
    setPublicPrivateLoading.value[index] = false
    console.log(err)
  })
}

const setAsPrivate = (index, recordId) => {
  setPublicPrivateLoading.value[index] = true
  RecordAPI.setRecordAsPrivate(recordId).then(res => {
    if (res.data.data.result) {
      updateRecordList()
    }
    setPublicPrivateLoading.value[index] = false
  }).catch(err => {
    setPublicPrivateLoading.value[index] = false
    console.log(err)
  })
}

const handleCurrentChange = (val) => {
  pageNumber.value = val;
  updateRecordList()
}

const updateRecordList = () => {
  recordListLoading.value = true;
  if (publicOnly) {
    RecordAPI.getPublicRecordList(taskId, pageNumber.value-1, pageSize.value, orderBy.value, orderType.value).then((res) => {
      if (res.data.code === 200) {
        let loadingList = [];
        for (let i = 0; i < res.data.data.record_list.length; i++) {
          loadingList.push(false)
        }
        setPublicPrivateLoading.value = loadingList;
        deleteLoading.value = loadingList;
        tableData.value = res.data.data.record_list
        totalNumber.value = res.data.data.total_count
      }
      recordListLoading.value = false;
    }).catch(() => {
      recordListLoading.value = false;
      tableData.value = []
    })
  } else {
    RecordAPI.getUserRecordList(taskId, pageNumber.value-1, pageSize.value, orderBy.value, orderType.value).then((res) => {
      if (res.data.code === 200) {
        tableData.value = res.data.data.record_list
        totalNumber.value = res.data.data.total_count
      }
      recordListLoading.value = false;
    }).catch(() => {
      recordListLoading.value = false;
      tableData.value = []
    })
  }
}

const deleteRecord = (index, recordId) => {
  deleteLoading.value[index] = true
  RecordAPI.deleteRecord(recordId).then(res => {
    if (res.data.code === 200 && res.data.data.result) {
      updateRecordList()
    }
    deleteLoading.value[index] = false
  }).catch(err => {
    console.log(err)
    deleteLoading.value[index] = false
  })
}

const onRowClick = (row) => {
  drawerLoading.value = true
  drawer.value=true
  RecordAPI.getRecord(row.id).then(res => {
    if (res.data.code === 200) {
      currentRecord.value = res.data.data.record

      let timeLine = [
        {
          content: 'Submitted',
          timestamp: '-',
        },
        {
          content: 'Started',
          timestamp: '-',
        },
        {
          content: 'Finished',
          timestamp: '-',
        }
      ]
      if (currentRecord.value.status === 'waiting') {
        timeLine[0].type = 'primary'
        timeLine[0].timestamp = currentRecord.value.submitted_at
      } else if (currentRecord.value.status === 'running') {
        timeLine[0].type = 'primary'
        timeLine[0].timestamp = currentRecord.value.submitted_at
        timeLine[1].type = 'primary'
        timeLine[1].timestamp = currentRecord.value.started_at
      } else {
        timeLine[0].type = 'primary'
        timeLine[0].timestamp = currentRecord.value.submitted_at
        timeLine[1].type = 'primary'
        timeLine[1].timestamp = currentRecord.value.started_at
        timeLine[2].type = 'primary'
        timeLine[2].timestamp = currentRecord.value.finished_at
      }
      currentTimeLine.value = timeLine
    }
    drawerLoading.value = false
  }).catch(err => {
    drawerLoading.value = false
    console.log(err)
  })
}

const downloadResultFile = () => {
  downloadResultLoading.value = true
  RecordAPI.getFile(currentRecord.value.id, currentRecord.value.result_file_id).then(res => {
    const url = window.URL.createObjectURL(new Blob([res.data], { type: 'application/zip' }));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'result.zip');
    document.body.appendChild(link);
    link.click();
    downloadResultLoading.value = false
  }).catch(err => {
    console.log(err)
    downloadResultLoading.value = false
  })
}

const downloadSubmitFile = () => {
  downloadSubmitFileLoading.value = true;
  RecordAPI.getFile(currentRecord.value.id, currentRecord.value.file_id).then(res => {
    const url = window.URL.createObjectURL(new Blob([res.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', currentRecord.value.file_name);
    document.body.appendChild(link);
    link.click();
    downloadSubmitFileLoading.value = false
  }).catch(err => {
    console.log(err)
    downloadSubmitFileLoading.value = false
  })
}

const clickStop = () => {}

onMounted(() => {
  updateRecordList()
})

</script>

<script>
export default {
  name: "RecordList",
}
</script>

<style>
.record-table .cell{
    height: 60px;
    line-height: 30px;
    text-overflow: ellipsis;
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
}
.drawer-divider-title{
    font-size: 14px;
    font-weight: bold;
}
.el-table .waiting {
    --el-table-tr-bg-color: var(--el-color-info-light-9);
}
.el-table .failed {
    --el-table-tr-bg-color: var(--el-color-danger-light-9);
}
.el-table .running {
    --el-table-tr-bg-color: var(--el-color-warning-light-9);
}
.el-table .finished {
    --el-table-tr-bg-color: var(--el-color-success-light-9);
}
</style>
