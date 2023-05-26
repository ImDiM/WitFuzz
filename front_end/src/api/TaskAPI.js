import { apiRequest} from "./request.js";
import qs from 'qs';


const TaskAPI = {
  getTaskList(id) {
    return apiRequest({
      url: `/tasklist`,
      method: 'get',
    })
  },
  getTask(taskId) {
    return apiRequest({
      url: `/task/${taskId}`,
      method: 'get',
    })
  },
  getTaskSubmitDescription(taskId) {
    return apiRequest({
      url: `/task/${taskId}/submit_description`,
      method: 'get',
    })
  },
  submitFuzz(taskId, data) {
    return apiRequest({
      url: `/task/${taskId}/submit`,
      method: 'post',
      data: data,
      params: {
        token: localStorage.getItem('token')
      }
    })
  }
}


export default TaskAPI;
