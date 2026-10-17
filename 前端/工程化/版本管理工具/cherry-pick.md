# cherry-pick
*第一次用这个命令还是在字节实习的时候，我哭，想回去*

```sh
git cherry-pick <commit-hash>
```


|命令|作用|
|---|---|
|`git cherry-pick abc1234`|挑选一个提交|
|`git cherry-pick A B C`|挑选多个指定提交|
|`git cherry-pick A..B`|挑选 A 之后到 B 的提交，不包含 A|
|`git cherry-pick A^..B`|挑选从 A 到 B 的提交，包含 A|
|`git cherry-pick -n abc1234`|应用修改但不自动创建 Commit|
|`git cherry-pick -x abc1234`|在新提交信息中记录原始提交 Hash|

其中 `-n`（`--no-commit`）很有用