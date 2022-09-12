import axios from 'axios'
export var baseurl = 'http://127.0.0.1:8000/api/'
export function get(config){

    const instance=axios.create({
        method: 'get',
        baseURL: baseurl,
        timeout: 100000,
        headers: {'Content-Type': 'application/x-www-form-urlencoded',}
    })

    return instance(config)
}

export function post(config){

    const instance=axios.create({
        method: 'post',
        baseURL: baseurl,
        timeout: 100000,
        headers: {'Content-Type': 'application/x-www-form-urlencoded',}
    })

    return instance(config)
}
