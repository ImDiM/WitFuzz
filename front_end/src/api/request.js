import axios from "axios";

const apiUrl = import.meta.env.VITE_API_URL


export const apiRequest = axios.create({
  baseURL: apiUrl,
  timeout: 100000,
})

apiRequest.interceptors.response.use(res=>authMiddleware(res))

function authMiddleware(res) {
  if (res.data.code === 401) {
    ElNotification({
      title: 'Error',
      message: 'Please login first.',
      type: 'error',
    })
    setTimeout(() => {
      window.location.href = '/login'
    }, 500)
    // do sth.
  } else {
    // allow cross origin
    res.headers["Access-Control-Allow-Origin"] =  "*"
    return res
  }
}
