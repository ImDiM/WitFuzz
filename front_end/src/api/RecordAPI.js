import { apiRequest} from "./request.js";
import qs from 'qs';


const RecordAPI = {
  getUserRecordList(taskId, pageNumber, pageSize, orderBy, orderType) {
    return apiRequest({
      url: `/recordlist`,
      method: 'get',
      params: {
        token: localStorage.getItem('token'),
        task_id: taskId,
        page_number: pageNumber,
        page_size: pageSize,
        order_by: orderBy,
        order_type: orderType,
      }
    })
  },
  getPublicRecordList(taskId, pageNumber, pageSize, orderBy, orderType) {
    return apiRequest({
      url: `/recordlist/public`,
      method: 'get',
      params: {
        task_id: taskId,
        page_number: pageNumber,
        page_size: pageSize,
        order_by: orderBy,
        order_type: orderType,
      }
    })
  },
  getRecord(recordId) {
    return apiRequest({
      url: `/record/${recordId}`,
      method: 'get',
      params: {
        token: localStorage.getItem('token')
      }
    })
  },
  setRecordAsPublic(recordId) {
    return apiRequest({
      url: `/record/${recordId}/public`,
      method: 'put',
      params: {
        token: localStorage.getItem('token')
      }
    })
  },
  setRecordAsPrivate(recordId) {
    return apiRequest({
      url: `/record/${recordId}/private`,
      method: 'put',
      params: {
        token: localStorage.getItem('token')
      }
    })
  },
  deleteRecord(recordId) {
    return apiRequest({
      url: `/record/${recordId}`,
      method: 'delete',
      params: {
        token: localStorage.getItem('token')
      }
    })
  },
  getFile(recordId, fileId) {
    return apiRequest({
      url: `/record/${recordId}/file`,
      method: 'get',
      responseType: 'blob',
      headers:{ 'Content-Type': 'application/json; application/octet-stream'},
      params: {
        token: localStorage.getItem('token'),
        file_id: fileId,
      }
    })
  }
}


export default RecordAPI;
