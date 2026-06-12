# ‌git flow
是一种 Git 分支管理工作流模型‌，通过定义 5 类核心分支（master、develop、feature、release、hotfix）来规范团队协作开发流程，适合需要定期发布版本的项目。‌‌


核心分支有哪些
‌master 分支‌：只存放正式发布的稳定代码，每次提交都代表一个可上线版本，不能直接在此分支开发。
‌develop 分支‌：日常开发的主线分支，所有新功能都先合并到这里，代表最新开发进度。
‌feature 分支‌：从 develop 分支创建，用于开发单个新功能，完成后合并回 develop，命名格式为feature/功能名。
‌release 分支‌：从 develop 分支创建，用于发布前的测试和小 bug 修复，不允许加新功能，完成后合并到 master 和 develop。
‌hotfix 分支‌：从 master 分支创建，用于紧急修复线上严重 bug，修复后同时合并回 master 和 develop。‌‌
