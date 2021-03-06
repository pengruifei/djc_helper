# DNF蚊子腿小助手
本脚本可用于自动化道聚城和心悦活动的一些流程，从而不必再每日手动点开app去进行（签到-领取签到奖励-完成每日任务-领取任务奖励-领取金银箱子-兑换调整箱和疲劳药）的琐碎流程，解放双手和心智。

# 声明
再强调一遍，这个工具首先是我自己用，然后才是分享出来给大家一起用的~<br>
核心需求是我自己会用能用，文档、教程都是为了方便各位使用而特地添加的，能起到一丝参考作用已经是很不错了。<br>
维护这个工具的时间有限，各位请将程序稳定性/功能可用性/异常崩溃等【偏程序】类的问题来作为反馈问题的主要类目，而不是配置方便性、文档准确性、视频精练度、界面美观度等【非程序类】问题。我是一个程序员，不是策划，也不是文案，更不是ui，能把程序功能做好已经很不错了。而且单就指引性信息而言，目前的文字文档、视频教程、配置文件注释、代码注释、运行时日志等已经提供了使用本工具所需要的几乎所有须知信息了。<br>
今天在论坛跟一个揪着文档不能完美描述程序运行逻辑这一点不放的人大吵了一顿，而且最后看他给出的截图，所谓的因为我没有给出多账号时账号名称不能重复这一点而浪费了半小时也完全不能成立，根据截图，明确提示了【第2个账号 默认账号 的名称与第1个账号的名称重复了，请调整为其他名称】，因为使用了默认的log.error方法，最终的色彩为暗红色，可能不太显眼，但是这并不能抵消实际已经给出了解决问题所需的完整信息这一点。<br>
今后如果再有这种事的话，我觉得可能还是我自己一个人用比较好，免得生是非=……=<br>
最后再提一小点，这真的只是单纯的分享出来给大家用，没有高人一等，也不比你低劣几分。我选择分享出来，也自然可以选择只接受特定内容的建议，你如果觉得好用，尽管去用。<br>
如果觉得哪里不好，如果是程序性逻辑问题，可以向我提issue或反馈，自然会尽力解决。如果是非程序类的问题，如配置方便性等，请自行fork一份代码去做调整，然后使用自己修改后的版本。当然如果愿意与其他人分享，也可以提一个pull request，如果真的有所改善，将会选择性合并进主干。当然，也可以选择不用哈。但是不接受就非程序类的问题来向我提意见/需求等，真的真的没有时间（别跟我说【我管你有没有时间】这种话，如果这样彼此没用沟通的必要了）。

# 唯一发布地址
源代码将持续更新于[本仓库](https://github.com/fzls/djc_helper) ，每个版本将通过下面的蓝奏云链接进行发布，请勿于其他地方下载使用，如各种群文件、软件站等，避免使用到被篡改后的版本，以免出问题-。-

# 网盘链接（更新于2020/10/21)
链接: https://fzls.lanzous.com/b01bor45i 提取码: fzls
链接: https://fzls.lanzous.com/s/djc-helper 提取码: fzls

# 视频教程
https://space.bilibili.com/1851177

# 交流群
553925117

# 『重要』与个人隐私有关的skey相关说明
1. skey是腾讯系应用的通用鉴权票据，个中风险，请Google搜索《腾讯skey》后自行评估
2. skey有过期时间，目前根据测试来看应该是一天。目前已实现手动登录、扫码登录（默认）、自动登录。
    1. 手动登录需要自行在网页中登录并获取skey填写到配置表。
    2. 扫码登录则会在每次过期时打开网页让你签到，无需手动填写。
    3. 自动登录则设置过一次账号密码后续无需再操作。
3. 本脚本仅使用skey进行必要操作，用以实现自动化查询、签到、领奖和兑换等逻辑，不会上传到与此无关的网站，请自行阅读源码进行审阅
4. 如果感觉有风险，请及时停止使用本软件，避免后续问题

# 提示：
目前仅保证CHANGELOG.MD和使用教程文档中是最新内容介绍，后续新功能可能会忘记添加到这里，大家可以自行查看对应文档。

# 使用方法
请查看【使用教程/使用文档.docx】

# 开机自动运行
请查看【使用教程/使用文档.docx】

# 功能完成情况
- [X] 自动化登录qq获取skey
- [x] 签到
- [x] 领取每日签到奖励
- [x] 领取累积签到奖励
- [x] 自动完成《礼包达人》任务
- [x] 自动完成《绝不错亿》任务
- [x] 领取任务奖励和金银宝箱
- [x] 兑换调整箱和疲劳药
- [x] 查询聚豆余额
- [x] 查询聚豆流水
- [x] 获取dnf角色信息
- [x] 获取指尖江湖（手游）礼包、角色信息
- [X] 增加支持设置更多手游来用于完成《礼包达人》任务
- [X] 黑钻每月礼包
- [X] 信用积分礼包和游戏信用礼包
- [ ] 心悦G分每日签到、每周礼包和免费抽奖、理财周卡和月卡
