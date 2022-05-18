# 交大学生个性化首页开发

## 开发人员
本网站由上海交通大学本-(2021-2022-2)-NIS2328-1-软件工程课程小组5开发。

## 项目介绍
SJTUers轻主页为非官方网站。本网站的目的在于为交大学生开发个性化主页，集成交大常用与生活常用为一体。

## 项目目的
- 目前的国内首页情况堪忧：
    - 常见的默认主页广告横行且不实用，例如hao123，2345，360等；
    - 默认的搜索引擎可以实现功能过少（仅能用于检索），并且UI个性化不足；
    - 交大学生在访问交大常见网址时，往往需要通过记忆网址或加入收藏夹的形式，且查询不同交大相关资料时往往需要在不同网站寻找，这极大地浪费了无数交大学子的时间。
- 与现有相似首页相比：
    - 目前已有人开发简洁、实用的首页，但是个性化不足仍未解决，例如[简约导航](https://www.jianavi.com/)；
    - 当下友校已搭建出了该校学生个性化使用的首页——[ZJUers轻首页](https://zjuers.com/)，其具有域名简单、界面简约、功能齐全的特点，但其个性化仅为学校个性化，我们希望能够搭建一个用户单位个性化的首页。

## 项目功能

基于以上需求，我们将以django为基础框架，构建一个具有以下功能的交大学生个性化首页：

- 交大网址索引，如教务处、教学信息服务网、canvas、邮箱等；
- 用户模块，支持Jaccount登录，并可以同步用户个性化设置的网址等数据；
- 工具小组件，包括疫情、食堂、校车实时信息可视化；
- 天气小组件，包括实时天气与3日天气预告，点击后可查看天气详情页面，可自定义当前城市；
- 资讯小组件，包括教务处通知公告、交大新闻、微博、知乎、bilibili热搜实时信息；
- 搜索引擎，可以在百度、必应、谷歌等常用搜索引擎中切换；
- 每日诗词，随着每次刷新在网页底部更新一句诗词；
- 时钟组件，实时显示公历、农历日期和当前时间；
- 简洁模式与倒计时，点击时钟组件可以自动切换简洁模式开关，简洁模式下展示倒计时，自动计算到重要日期的时间；
- 壁纸，用户可以在壁纸库中选择也可以上传自己的壁纸，并与用户同步；
- 天气详情页面，背景随时间天气展示相应交大摄影图片，提供5天预告与当前天气指数；
- 关于我们页面，网址介绍与隐私声明。

## 第一轮迭代记录

**3月9日**：上传0.0版本。

**3月22日**：0.1版本，网站基本界面结构搭建完毕。修复热搜板块问题，优化搜索框，新增疫情板块，参数细节调整。

**3月30日**：搜索框增加切换搜索引擎功能，目前支持百度、谷歌、必应、搜狗、知乎、有道、B站、CSDN、Github等9种搜索引擎；更改搜索请求方式；搜索页面打开为新标签页；增加支持键盘回车搜索；优化部分样式和参数。

**4月2日**：新增教务处通知、B站热搜内容，超链接请求改为打开新标签页，修复news与tools板块级联的bug，外链化javaScript内容，优化部分参数。

**4月3日**：修复爬取数据时出现的bug，改用xpath方式爬取html数据，修改疫情数据来源，新增数据更新时间，调整疫情数据布局，获取图书馆数据。

**4月12日**：爬取xml类型的天气数据，新建天气应用，初步搭建完毕天气界面。可视化独立demo全部完成。

**4月14日**：协程&异步编程实现数据爬取，大幅度减小用户访问index页面的返回时间。

**4月15日**：模板层配置jinja2，对模板中重复内容调取 `marco` 宏，重构模板代码，提高可读性。

**4月17日**：新建翻页式时钟实时显示时间，推出“简洁模式”（仅保留时钟、搜索框和诗词，诗词悬浮时可以出现作者），可通过点击时钟进行切换。新建右侧边栏。修复缩放页面时出现的bug。更新搜索框样式。

**4月18日**：更改微博与知乎数据获取源，解决热搜数据响应超时和服务器崩坏的bug，大幅提升网页打开速度。对新闻板块过长字符串的截取采用先转码为utf-8、截断后再转码的方式，使得含有不同数目的英文/数字字符的字符串长度判定更为合理，修复用户视角出现的bug。

**4月19日**：添加交大新闻爬取内容，为网页匹配favicon.ico。

## 第二轮迭代记录

**4月22日**：实现了基础的jac登录登出功能。

**4月24日**：使用token获取basic的信息（包括Jac账号，姓名等）。

**4月24日**：自定义网址内容实现，允许用户增加、删除、修改网址。

**4月28日**：创建了用户数据库，并且能够保存不同用户的网站偏好设置。

**5月1日**：自定义功能ui设计完成，倒计时界面增加年月日下拉选择；对于未登录用户弹窗提示无权限使用自定义功能。初步全部实现可视化功能。

**5月4日**：实现了新用户登录能够自动创建用户，并且保存网站偏好的功能；切换壁纸、上传壁纸功能完成。POST请求由form形式发出改为ajax发出。

**5月5日**：添加整合网站、添加倒计时的前端UI；修改壁纸、添加删除网站都与用户绑定，数据库表建立完毕。

**5月6日**：网站logo添加完毕，增添网站时的icon显示问题解决。

**5月7日**：倒计时模块前后端交互完成。修复并完善所有POST请求的前后端交互。配置CRSF中间件。倒计时字体修改，壁纸自定义ui设计。添加weather页面根据天气和时间自动匹配相应背景图片的功能。修复已知的Bug。美化可视化界面，包括修改图标大小，字体倾斜度等。

**5月9日**：添加关于我们页面，可通过侧边栏“关于”按钮跳转。

**5月10日**：修改了几个无法正常跳转的网页地址；邮箱重定向问题仍待解决。

**5月12日**：邮箱重定向问题已经自动解决，修改了网页logo，以及搜索框URL不正确的问题；增加了单元测试；改进了可视化刷新间隔太快问题。

**5月13日**：天气组件全部完成，包括前端样式和后端更改城市的操作，点击组件内元素跳转到天气详情，即weather页面。重构代码。

**5月17日**：用户测试与项目部署。

## 特别感谢
感谢马颖华老师对于开发工具、软件工程概念等方面的传授以及项目开发中及时的指导与反馈。

感谢杜佳俊助教为本项目Jaccount登录等技术层面提供的耐心指导。

感谢王山木、谈子铭、邰嘉卫等同学为本项目提供的交大摄影图片。