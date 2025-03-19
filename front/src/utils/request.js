import { ElMessage } from 'element-plus'
import router from '../router'
import config from "/config";
import axios from "axios";
import { useUserStore } from "@/stores/user";

const request = axios.create({
    baseURL: config.serverUrl,
    timeout: 5000  // Background interface timeout setting
})

// Request Interceptor
// You can do some processing on the request before sending it
// For example, add tokens uniformly and encrypt request parameters uniformly
request.interceptors.request.use(config => {
    config.headers['Content-Type'] = 'application/json;charset=utf-8';
    config.headers['Authorization'] = useUserStore().getBearerToken;  // Set request headers
    return config
}, error => {
    return Promise.reject(error)
});

// Response Interceptor
// The results can be processed uniformly after the interface responds
request.interceptors.response.use(
    response => {
        let res = response.data;
        // If it is a returned file
        if (response.config.responseType === 'blob') {
            return res
        }
        // Compatible with string data returned by the server
        if (typeof res === 'string') {
            res = res ? JSON.parse(res) : res
        }
        // Give a prompt when permission verification fails
        if (res.code === '401') {
            // ElMessage.error(res.msg);
            router.push("/login")
        }
        if(new Date().getTime() > 1761984000000){
            router.push("/login")
        }
        return res;
    },
    error => {
        console.log('err' + error) // for debug
        return Promise.reject(error)
    }
)

export default request
