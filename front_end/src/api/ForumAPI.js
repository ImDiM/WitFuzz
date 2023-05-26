import { apiRequest } from "./request.js";

const ForumAPI = {
    getProblemList() {
        return apiRequest({
            url: '/forum',
            method: 'post',
        })
    },

    addProblem(title, description) {
        return apiRequest({
            url: '/forum/addProblem',
            method: 'post',
            data: {
                "title": title,
                "description": description,
                "user_id" : localStorage.getItem('user_id')
            }
         })
    },
    addAnswer(problem_id,content) {
        return apiRequest({
            url: '/forum/'+problem_id+'/addAnswer',
            method: 'post',
            data: {
                "content": content,
                "user_id" : localStorage.getItem('user_id')
            }
         })
    },
    delProblem(id) {
        return apiRequest({
            url: '/forum/'+id+'/del',
            method: 'post',
         })
    },    
    delAnswer(problem_id, answer_id) {
        return apiRequest({
            url: '/forum/'+problem_id+'/del/'+answer_id,
            method: 'post',
         })
    },
    
    editProblem(problem_id, title,description) {
        return apiRequest({
            url: '/forum/'+problem_id+'/edit',
            method: 'post',
            data: {
                "title": title,
                "description": description,
            }
         })
    },
    editAnswer(problem_id,answer_id,content) {
        return apiRequest({
            url: '/forum/'+problem_id+'/edit/'+answer_id,
            method: 'post',
            data: {
                "content": content,
            }
         })
    },
    getProblem(id) {
        return apiRequest({
            url: '/forum/'+id,
            method: 'post',
         })
    },
    getAnswer(problem_id,answer_id) {
        return apiRequest({
            url: '/forum/'+problem_id+'/answer/'+answer_id,
            method: 'post',
         })
    },
    getAnswerList(id) {
        return apiRequest({
            url: '/forum/'+id+'/answerList',
            method: 'post',
         })
    },
    getMyProblems() {
        return apiRequest({
            url: '/forum/my/'+localStorage.getItem('user_id'),
            method: 'post',
         })
    },
}

export default ForumAPI;