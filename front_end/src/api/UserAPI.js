import { apiRequest } from "./request.js";
import qs from 'qs';
import md5 from 'js-md5'


const UserAPI = {
  register(email, name, password, intro, birthday, job) {
    return apiRequest({
      url: '/user/register',
      method: 'post',
      data: {
        "email": email,
        "name": name,
        "password": md5(password),
        "intro": intro,
        "birthday": birthday,
        "job": job,
      }
    })
  },
  login(email, password) {
    return apiRequest({
      url: '/user/login',
      method: 'post',
      data: {
        "email": email,
        "password": md5(password),
      }
    })
  },
  getInfo(token) { // TODO 获取用户信息
    return apiRequest({
      url: '/user/getinfo',
      method: 'post',
      data: {
        "token": token,
      }
    })
  },
  sendVerifyCode(email) {
    return apiRequest({
      url: '/user/sendverifyCode',
      method: 'post',
      data: {
        "email": email,
      }
    })
  },
  modifyPasswordVerify(email, code) {
    return apiRequest({
      url: '/user/modifypasswordverify',
      method: 'post',
      data: {
        "email": email,
        "verifycode": code,
      }
    })
  },
  modifyPassword(email, password) {
    return apiRequest({
      url: '/user/modifypassword',
      method: 'post',
      data: {
        "email": email,
        "password": md5(password),
      }
    })
  },
  modifyInfo(name, intro, job, birthday) {
    return apiRequest({
      url: '/user/modifyinfo',
      method: 'post',
      data: {
        "token": localStorage.getItem('token'),
        "name": name,
        "intro": intro,
        "job": job,
        "birthday": birthday,
      }
    })
  }
}


export default UserAPI;
