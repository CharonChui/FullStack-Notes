全栈开发知识库
===

> 一份覆盖 **移动端 · C/C++ · Go · 鸿蒙 · 前端 · 服务端** 的工程实践笔记合集，
> 按技术域分目录沉淀，共 **628 篇** 笔记，统一索引、持续更新。

内容总览
===

| 技术域 | 目录 | 篇数 | 覆盖范围 |
| :--- | :--- | ---: | :--- |
| Android 移动端 | [Android/](./Android/README.md) | 562 | 基础与进阶、源码解析、音视频、Jetpack、Kotlin、架构、端侧 AI |
| C / C++ | [CPP/](./CPP/README.md) | 26 | C 语言、C++、Qt、Linux 系统编程 |
| Go | [Golang/](./Golang/README.md) | 25 | 语言基础、并发、Web 开发、数据库、GUI |
| HarmonyOS | [HarmonyOS/](./HarmonyOS/README.md) | 15 | ArkTS、声明式 UI、UIAbility、网络与数据管理 |
| 前端 | [Fe/](./Fe/README.md) | — | 规划中 |
| 服务端 | [Server/](./Server/README.md) | — | 规划中 |
| **合计** | | **628** | |

---

一、Android（移动端）
---

目录：[Android/](./Android/README.md)　|　562 篇，19 个主题目录。

| 分类 | 目录 | 篇数 | 内容概要 |
| :--- | :--- | ---: | :--- |
| 基础部分 | [BasicKnowledge](./Android/BasicKnowledge) | 71 | 四大组件、UI 控件、存储、权限、JNI、面试题 |
| 进阶部分 | [AdavancedPart](./Android/AdavancedPart) | 30 | 性能优化、热修复、RecyclerView、Crash/ANR、OOM |
| 源码解析 | [SourceAnalysis](./Android/SourceAnalysis) | 19 | View 绘制、事件分发、Activity 启动、网络框架 |
| 音视频开发 | [VideoDevelopment](./Android/VideoDevelopment) | 85 | FFmpeg、OpenGL、ExoPlayer、封装格式、编解码 |
| Jetpack | [Jetpack](./Android/Jetpack) | 30 | Lifecycle、ViewModel、Room、Compose、Material |
| Kotlin | [KotlinCourse](./Android/KotlinCourse) | 10 | 语法、协程、扩展、Kotlin 设计模式 |
| 依赖注入 | [Dagger2](./Android/Dagger2) | 9 | Dagger2 入门到原理分析 |
| 图片加载 | [ImageLoaderLibrary](./Android/ImageLoaderLibrary) | 4 | Glide、Coil、图片库横向对比 |
| RxJava | [RxJavaPart](./Android/RxJavaPart) | 7 | 操作符、调度、执行原理 |
| Java 与算法 | [JavaKnowledge](./Android/JavaKnowledge) | 37 | JVM、并发、集合、设计模式、加密、面试题 |
| 算法题解 | [Algorithm](./Android/Algorithm) | 129 | 数据结构、剑指 Offer、高频算法专题 |
| 操作系统 | [OperatingSystem](./Android/OperatingSystem) | 17 | 进程线程、内存管理、Android 内核与 Framework |
| 架构设计 | [Architect](./Android/Architect) | 2 | 架构演进与分层设计 |
| 构建工具 | [Gradle&Maven](./Android/Gradle&Maven) | 5 | Gradle 专题、Maven 发布、Composing builds |
| 开发工具 | [Tools&Library](./Android/Tools&Library) | 8 | 开发组合、性能工具、MAT、Markdown |
| 应用发布 | [AppPublish](./Android/AppPublish) | 3 | 打包、签名、Zipalign、Jenkins |
| Android Studio | [AndroidStudioCourse](./Android/AndroidStudioCourse) | 10 | IDE 使用技巧、构建提速、NDK 开发 |
| 跨平台 | [Flutter](./Android/Flutter) | 12 | Flutter 入门与实战 |
| 端侧 AI | [MobileAIModel](./Android/MobileAIModel) | 74 | 端侧模型、AI Agent 体系课、推理与部署 |

> Android 的完整分类索引（含 347 条文章直链）见 **[Android/README.md](./Android/README.md)**；其余笔记因数量较大，此处仅列主题目录。

---

二、C / C++（CPP）
---

目录：[CPP/](./CPP/README.md)　|　26 篇。

| 分类 | 目录 | 篇数 | 内容概要 |
| :--- | :--- | ---: | :--- |
| C 语言入门 | [C入门](./CPP/C%E5%85%A5%E9%97%A8) | 9 | 指针、结构体、共用体、文件读写、内存管理、链表 |
| C++ 入门 | [C++入门](./CPP/C%2B%2B%E5%85%A5%E9%97%A8) | 8 | 类、引用与值参数、动态内存、decltype、lambda、核心与提高编程 |
| Qt | [Qt](./CPP/Qt) | 6 | 组件、事件机制、绘制、IO 流、线程 |
| Linux 系统编程 | [linux](./CPP/linux) | 3 | 动态库、系统函数调用、进程间通信 |

**C 语言入门（9 篇）** · `CPP/C入门/`

- [1.C语言简介(一)](CPP/C入门/1.C语言简介%28一%29.md)
- [2.指针(二)](CPP/C入门/2.指针%28二%29.md)
- [3.结构体(三)](CPP/C入门/3.结构体%28三%29.md)
- [4.共用体(四)](CPP/C入门/4.共用体%28四%29.md)
- [5.文件读写(五)](CPP/C入门/5.文件读写%28五%29.md)
- [6.内存管理(六)](CPP/C入门/6.内存管理%28六%29.md)
- [7.预处理器(七)](CPP/C入门/7.预处理器%28七%29.md)
- [8.链表(八)](CPP/C入门/8.链表%28八%29.md)
- [9.编写大型程序(九)](CPP/C入门/9.编写大型程序%28九%29.md)

**C++ 入门（8 篇）** · `CPP/C++入门/`

- [1.C++基础](CPP/C++入门/1.C++基础.md)
- [2.类](CPP/C++入门/2.类.md)
- [3.引用参数和值参数](CPP/C++入门/3.引用参数和值参数.md)
- [4.动态内存](CPP/C++入门/4.动态内存.md)
- [5.decltype](CPP/C++入门/5.decltype.md)
- [6.C++核心编程](CPP/C++入门/6.C++核心编程.md)
- [7.C++提高编程](CPP/C++入门/7.C++提高编程.md)
- [8.lambda表达式](CPP/C++入门/8.lambda表达式.md)

**Qt（6 篇）** · `CPP/Qt/`

- [1.Qt简介](CPP/Qt/1.Qt简介.md)
- [2.Qt常用组件](CPP/Qt/2.Qt常用组件.md)
- [3.Qt事件机制](CPP/Qt/3.Qt事件机制.md)
- [4.Qt绘制](CPP/Qt/4.Qt绘制.md)
- [5.Qt IO流](CPP/Qt/5.Qt%20IO流.md)
- [6.Qt线程](CPP/Qt/6.Qt线程.md)

**Linux 系统编程（3 篇）** · `CPP/linux/`

- [1.动态库](CPP/linux/1.动态库.md)
- [2.系统函数调用](CPP/linux/2.系统函数调用.md)
- [3.进程间通信](CPP/linux/3.进程间通信.md)

---

三、Go（Golang）
---

目录：[Golang/](./Golang/README.md)　|　25 篇。

| 分类 | 目录 | 篇数 | 内容概要 |
| :--- | :--- | ---: | :--- |
| 语言基础 | [Golang/](./Golang) | 13 | 语法、切片映射、指针结构体接口、错误处理、并发、反射 |
| Web 开发 | [Golang进行Web开发](./Golang/Golang%E8%BF%9B%E8%A1%8CWeb%E5%BC%80%E5%8F%91) | 7 | 搭建服务器、表单、数据库、Session、日志部署 |
| 数据库 | [常见数据库简介](./Golang/%E5%B8%B8%E8%A7%81%E6%95%B0%E6%8D%AE%E5%BA%93%E7%AE%80%E4%BB%8B) | 3 | MySQL、SQLite、Redis |
| Beego 框架 | [Beego框架](./Golang/Beego%E6%A1%86%E6%9E%B6) | 1 | Beego 简介 |
| GUI 开发 | [GUI开发](./Golang/GUI%E5%BC%80%E5%8F%91) | 1 | GTK 简介 |

**语言基础（13 篇）** · `Golang/` 根目录

- [1.Golang简介(一)](Golang/1.Golang简介%28一%29.md)
- [2.Golang变量及函数(二)](Golang/2.Golang变量及函数%28二%29.md)
- [3.Golang控制语句(三)](Golang/3.Golang控制语句%28三%29.md)
- [4.Golang数组、切片及映射(四)](Golang/4.Golang数组、切片及映射%28四%29.md)
- [5.Golang字符串(五)](Golang/5.Golang字符串%28五%29.md)
- [6.Golang指针、结构体及接口(六)](Golang/6.Golang指针、结构体及接口%28六%29.md)
- [7.Golang错误处理(七)](Golang/7.Golang错误处理%28七%29.md)
- [8.Golang并发编程之Goroutine及Channel(八)](Golang/8.Golang并发编程之Goroutine及Channel%28八%29.md)
- [9.Golang常用功能简介(九)](Golang/9.Golang常用功能简介%28九%29.md)
- [10.Golang方法(十)](Golang/10.Golang方法%28十%29.md)
- [11.Golang反射(十一)](Golang/11.Golang反射%28十一%29.md)
- [12.Golang开发之IDE选择(十二)](Golang/12.Golang开发之IDE选择%28十二%29.md)
- [13.Golang new和make的区别(十三)](Golang/13.Golang%20new和make的区别%28十三%29.md)

**Golang 进行 Web 开发（7 篇）** · `Golang/Golang进行Web开发/`

- [1.搭建一个Web服务器(一)](Golang/Golang进行Web开发/1.搭建一个Web服务器%28一%29.md)
- [2.Go搭建Web服务器的执行过程(二)](Golang/Golang进行Web开发/2.Go搭建Web服务器的执行过程%28二%29.md)
- [3.表单处理(三)](Golang/Golang进行Web开发/3.表单处理%28三%29.md)
- [4.数据库操作(四)](Golang/Golang进行Web开发/4.数据库操作%28四%29.md)
- [5.Session和数据存储(五)](Golang/Golang进行Web开发/5.Session和数据存储%28五%29.md)
- [6.日志和部署(六)](Golang/Golang进行Web开发/6.日志和部署%28六%29.md)
- [7.Linux环境go部署安装](Golang/Golang进行Web开发/7.Linux环境go部署安装.md)

**常见数据库简介（3 篇）** · `Golang/常见数据库简介/`

- [1.MySQL简介(一)](Golang/常见数据库简介/1.MySQL简介%28一%29.md)
- [2.SQLite简介(二)](Golang/常见数据库简介/2.SQLite简介%28二%29.md)
- [3.Redis简介(三)](Golang/常见数据库简介/3.Redis简介%28三%29.md)

**Beego 框架（1 篇）** · `Golang/Beego框架/`

- [1.Beego框架简介(一)](Golang/Beego框架/1.Beego框架简介%28一%29.md)

**GUI 开发（1 篇）** · `Golang/GUI开发/`

- [1.GTK简介(一)](Golang/GUI开发/1.GTK简介%28一%29.md)

---

四、HarmonyOS
---

目录：[HarmonyOS/](./HarmonyOS/README.md)　|　15 篇，基于 HarmonyOS 4.0（NEXT 开放后更新）。

- [1.HarmonyOS简介](HarmonyOS/1.HarmonyOS简介.md)
- [2.ArkTS基础语法](HarmonyOS/2.ArkTS基础语法.md)
- [3.HarmonyOS开发术语](HarmonyOS/3.HarmonyOS开发术语.md)
- [4.HarmonyOS应用开发初探](HarmonyOS/4.HarmonyOS应用开发初探.md)
- [5.ArkTS声明式UI入门](HarmonyOS/5.ArkTS声明式UI入门.md)
- [6.常用组件](HarmonyOS/6.常用组件.md)
- [7.应用组件UIAbility](HarmonyOS/7.应用组件UIAbility.md)
- [8.通知](HarmonyOS/8.通知.md)
- [9.动画](HarmonyOS/9.动画.md)
- [10.网络请求](HarmonyOS/10.网络请求.md)
- [11.数据管理](HarmonyOS/11.数据管理.md)
- [12.使用第三方库](HarmonyOS/12.使用第三方库.md)
- [13.应用状态管理Storage](HarmonyOS/13.应用状态管理Storage.md)
- [14.公共事件概述](HarmonyOS/14.公共事件概述.md)
- [15.Promise、Async、Await、then](HarmonyOS/15.Promise、Async、Await、then.md)

---

五、前端（Fe）
---

目录：[Fe/](./Fe/README.md)　|　暂未收录笔记，规划目录：

- `Fe/Base/` —— HTML / CSS / JavaScript 基础与浏览器原理
- `Fe/TypeScript/` —— 类型系统、泛型、工程化配置
- `Fe/Framework/` —— Vue / React / 跨端框架
- `Fe/Engineering/` —— 构建工具、包管理、性能优化、调试

---

六、服务端（Server）
---

目录：[Server/](./Server/README.md)　|　暂未收录笔记，规划目录：

- `Server/Java/` —— Java 服务端、Spring 生态
- `Server/Go/` —— Go 服务端（可与 `Golang/` 联动）
- `Server/Database/` —— MySQL、Redis、索引与事务
- `Server/Middleware/` —— 消息队列、网关、缓存
- `Server/DevOps/` —— Docker、CI/CD、日志监控

---

目录结构
---

```text
FullStack-Notes/
├── README.md                # 本文件：全库总索引
├── Android/                 # 移动端 562 篇
│   ├── README.md            # Android 完整分类索引
│   ├── BasicKnowledge/      71    基础部分
│   ├── AdavancedPart/       30    进阶部分
│   ├── SourceAnalysis/      19    源码解析
│   ├── VideoDevelopment/    85    音视频开发
│   ├── Jetpack/             30    Jetpack
│   ├── KotlinCourse/        10    Kotlin
│   ├── Dagger2/              9    依赖注入
│   ├── ImageLoaderLibrary/   4    图片加载
│   ├── RxJavaPart/           7    RxJava
│   ├── JavaKnowledge/       37    Java 与算法
│   ├── Algorithm/          129    算法题解
│   ├── OperatingSystem/     17    操作系统
│   ├── Architect/            2    架构设计
│   ├── Gradle&Maven/         5    构建工具
│   ├── Tools&Library/        8    开发工具
│   ├── AppPublish/           3    应用发布
│   ├── AndroidStudioCourse/ 10    Android Studio
│   ├── Flutter/             12    跨平台
│   └── MobileAIModel/       74    端侧 AI
├── CPP/                     # C/C++ 26 篇
│   ├── README.md
│   ├── C入门/                9
│   ├── C++入门/              8
│   ├── Qt/                   6
│   └── linux/                3
├── Golang/                  # Go 25 篇
│   ├── README.md
│   ├── *.md                 13    语言基础
│   ├── Golang进行Web开发/     7
│   ├── 常见数据库简介/        3
│   ├── Beego框架/            1
│   └── GUI开发/              1
├── HarmonyOS/               # 鸿蒙 15 篇
│   └── README.md
├── Fe/                      # 前端（规划中）
│   └── README.md
└── Server/                  # 服务端（规划中）
    └── README.md
```

维护约定
---

1. **先归域，再归主题**：新增笔记先判断归属 `Android` / `CPP` / `Golang` / `HarmonyOS` / `Fe` / `Server`，再落到对应主题子目录。
2. **各域自治**：域入口为该目录下的 `README.md`，记录该域完整分类索引；根 README 只做域级导航。
3. **命名一致**：主题目录用英文名（`BasicKnowledge`、`Qt`、`linux`），笔记文件名用中文题目，系列文章加 `1.`、`2.` 前缀。
4. **链接规范**：域内互链使用相对路径；文件名含 `(`、`)`、空格时需编码为 `%28`、`%29`、`%20`。

License
===

    Copyright (C) 2013 Charon Chui <charon.chui@gmail.com>

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
