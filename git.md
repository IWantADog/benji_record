# git

工作目录、索引、提交。三种状态互相转换。

常用固定变量：HEAD、ORIG_HEAD、MERGE_HEAD、FETCH_HEAD

常用信息获取命令

- git log
- git show-branch --more=5

git commit -amend: 改变当前分支最近一次提交的简单简单办法

git add:暂存更改。

git commit: 提交暂存的文件

git diff的四种用法：

    - git diff: 比较工作目录与索引
    - git diff commit: 比较工作目录与指定提交
    - git diff --cached commit: 比较索引与指定提交
    - git diff commit1 commit2: 比较指定的两个提交

git reset的常见用法：

- git reset --soft commit: 将HEAD移动到指定提交,不改变索引和工作目录
- git reset --mixed commit: 将HEAD移动到指定提交，改变索引为指定提交的索引，工作目录不变
    （git reset的默认处理方式）
- git reset --hard commit: 将HEAD、索引、工作目录修改为指定索引的提交，覆盖提交的文件。

--soft用来修改指定提交的备注信息。

--mixed常见有两种用法

- 取消暂存的文件 git reset HEAD filename
- 取消最近的一次有错误的提交 git reset HEAD^

--hard覆盖错误的提交，相当与回滚。

git show

git checkout: 切换分支或恢复工作目录