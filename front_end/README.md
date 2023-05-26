# Vue 3 + Vite

- [Vue.js (vuejs.org)](https://cn.vuejs.org/guide/quick-start.html)
- [Vite (vitejs.dev)](https://cn.vitejs.dev/)
- [Element Plus (gitee.io)](https://element-plus.gitee.io/zh-CN/)
- [Vue Router (vuejs.org)](https://v3.router.vuejs.org/zh/)
- [Axios (axios-http.cn)](https://www.axios-http.cn/docs/intro)


## install
```bash
npm install
```

## config
```bash
cp .env.development .env.development.local
```

> edit it to set your own config

## run
```bash
npm run dev
```

## Build

### Docker

- Nginx

```bash
docker build -t vite_demo .
```


- Linux
> use host network
```bash
docker run --name vite_demo --network=host -d --rm vite_demo
```

- others
> docker-desktop doesn't support host network
```bash
docker run --name vite_demo -p 5173:5173 -d --rm vite_demo
```

