# project-management-system

a web for pms

## 功能介绍

-   项目管理
-   用户注册 支持一个邮箱多个用户！！！
-   用户密码找回
-   数据备份
    -   db
    -   media
    -   keys
-   文档生成
-   导入导出
-   周刊

优化:

- 改为使用 docker compose 和  cicd 优化开发和部署.  
- 备份数据库的脚本需要改为celery定时任务执行.  


容器化应用
设置基本CI/CD流程
迁移到生产级Web服务器


房屋  地址、价格、面积、图片、描述等
物品 订单 账单

 Vue 3 + Element Plus + Supabase 的组合

用户方案: one2one

TODO:
日志记录:


我计划把admin当管理系统来使用, 需要对django默认用户扩展, 采用 one2one 来扩展属性后, 需要控制权限, 具体权限需求如下:

1. 所有用户可以登录admin
2. 所有用户默认, 
   - 其他模块: 查看公开内容的权限, 自己创建内容的所有权限
3. 真正管理员 控制所有的权限


