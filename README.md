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