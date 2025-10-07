![[Pasted image 20250829233919.png]]
![[Pasted image 20250829235448.png]]

### 二次封装
![[Pasted image 20250829234336.png]]
![[Pasted image 20250829234241.png]]

示例代码：
```javascript
import axios from "axios";
import { ElMessage } from "element-plus";
import "element-plus/es/components/message/style/css";
import { useUserStore } from "@/stores/user";
import router from "@/router";

//axios的基础封装
const httpInstance = axios.create({
    baseURL: "http://pcapi-xiaotuxian-front-devtest.itheima.net",
    timeout: 50000,
});

httpInstance.interceptors.request.use(
    (config) => {
        const userStore = useUserStore();
        const token = userStore.userInfo.token;
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (e) => Promise.reject(e)
);

// axios响应式拦截器
httpInstance.interceptors.response.use(
    (res) => res.data,
    (e) => {
        ElMessage({
            type: "warning",
            message: e.response?.data?.message,
        });

        //401token失效处理
        const userStore = useUserStore();

        if (e.response.status === 401) {
            userStore.clearUserInfo();
            router.push("/login");
        }

        return Promise.reject(e);
    }
);

export default httpInstance;

```

### API解耦
![[Pasted image 20250829235531.png]]
示例代码：
```javascript
import request from "@/utils/http";

export const getCheckInfoAPI = () => {
    return request({
        url: "/member/order/pre",
    });
};

export const createOrderAPI = (data) => {
    return request({
        url: "/member/order",
        method: "POST",
        data,
    });
};

```