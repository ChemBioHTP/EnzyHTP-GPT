# `MutexaGPT`

#### 介绍

**以下是 Gitee 平台说明，您可以替换此简介**
Gitee 是 OSCHINA 推出的基于 Git 的代码托管平台（同时支持 SVN）。专为开发者提供稳定、高效、安全的云端软件开发协作平台
无论是个人、团队、或是企业，都能够用 Gitee 实现代码托管、项目管理、协作开发。企业项目请看 [https://gitee.com/enterprises](https://gitee.com/enterprises)

#### 技术栈

* 框架：Vue3
* 状态管理：Pinia
* UI 库：Ant Design Vue
* 构建工具：Vite
* 其他：Axios 等

#### 环境要求

* **开发环境**：
  * Node.js 版本：v18.x或更高
  * npm 版本： v8.x 或更高
  * IDE 推荐： VS Code
 
* **运行环境**：
  * 浏览器支持：如 Chrome 90+、Firefox 85+、Edge 90+
  * 服务器要求：如 Nginx 或其他静态文件托管服务

#### 项目结构

**目录说明**：

```
├── public/           # 静态资源
├── src/              # 源代码
│   ├── api/          # 接口请求模块
│   ├── assets/       # 图片、样式等资源
│   ├── config/       # 配置文件
│   ├── components/   # 公共组件
│   ├── views/        # 页面视图
│   ├── router/       # 路由配置
│   ├── stores/        # 状态管理
│   └── main.js       # 入口文件
├── dist/             # 构建输出目录
├── package.json      # 依赖和脚本配置
└── vite.config.js    # Vite 配置文件（或 webpack.config.js）
```

​**核心文件说明**​：

* **src/main.js**：项目启动入口
* **src/router/index.js**：路由定义
* **src/api/**：后端接口调用逻辑

#### 安装与运行

1. **依赖安装**：

```
npm install
```

2. **启动开发服务器**：

````
npm run dev
````

3. **访问地址：**http://localhost:5173**（根据 Vite 默认端口，或自行修改）**

#### ​构建生产环境

* 构建命令：
  ```
  npm run build
  ```
* 输出目录：**dist/**
* 部署：将 **dist/** 文件夹上传至服务器，使用 Nginx 或其他工具托管。

#### 参与贡献

1. Fork 本仓库
2. 新建 Feat_xxx 分支
3. 提交代码
4. 新建 Pull Request

#### 特技

1. 使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2. Gitee 官方博客 [blog.gitee.com](https://blog.gitee.com)
3. 你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解 Gitee 上的优秀开源项目
4. [GVP](https://gitee.com/gvp) 全称是 Gitee 最有价值开源项目，是综合评定出的优秀开源项目
5. Gitee 官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)
6. Gitee 封面人物是一档用来展示 Gitee 会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)

