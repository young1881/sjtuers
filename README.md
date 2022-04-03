# 交大学生个性化首页开发

### 项目目的
- 目前的国内首页情况堪忧：
    - 常见的默认主页广告横行且不实用，例如hao123，2345，360等；
    - 默认的搜索引擎可以实现功能过少（仅能用于检索），并且UI个性化不足；
    - 交大学生在访问交大常见网址时，往往需要通过记忆网址或加入收藏夹的形式，且查询不同交大相关资料时往往需要在不同网站寻找，这极大地浪费了无数交大学子的时间。
- 与现有相似首页相比：
    - 目前已有人开发简洁、实用的首页，但是个性化不足仍未解决，例如[简约导航](https://www.jianavi.com/)；
    - 当下友校已搭建出了该校学生个性化使用的首页——[ZJUers轻首页](https://zjuers.com/)，其具有域名简单、界面简约、功能齐全的特点，但其个性化仅为学校个性化，我们希望能够搭建一个用户单位个性化的首页。

### 项目功能【草案】

基于以上需求，我们将以django为基础框架，构建一个具有以下功能的交大学生个性化首页：

- 交大网址索引，如教务处、教学信息服务网、canvas、邮箱、同去网、第二课堂等；
- 用户模块，支持Jaccount登录，并可以同步用户个性化设置的网址；
- 交大工具箱，包括课程表、同步canvas作业、食堂实时信息、校车实时信息等功能；
- 资讯小组件，包括天气、热搜、疫情信息等；
- 搜索引擎，可以在百度/必应/谷歌/搜狗中切换；
- 每日诗词，每日在角落更新一句诗词；
- 倒计时，计算到重要日期的时间；
- 壁纸，用户可以在壁纸库中选择也可以上传自己的壁纸；
- 云笔记，用于备忘录等情况，支持markdown, html语法。

### 第一轮迭代记录

**3月9日**：上传0.0版本。

**3月22日**：0.1版本，网站基本界面结构搭建完毕。修复热搜板块问题，优化搜索框，新增疫情板块，参数细节调整。

**3月30日**：搜索框增加切换搜索引擎功能，目前支持百度、谷歌、必应、搜狗、知乎、有道、B站、CSDN、Github等9种搜索引擎；更改搜索请求方式；搜索页面打开为新标签页；增加支持键盘回车搜索；优化部分样式和参数。

**4月2日**：新增教务处通知、B站热搜内容，超链接请求改为打开新标签页，修复news与tools板块级联的bug，外链化javaScript内容，优化部分参数。

**4月3日**：修复爬取数据时出现的bug，改用xpath方式爬取html数据，修改疫情数据来源，新增数据更新时间，调整疫情数据布局，获取图书馆数据。