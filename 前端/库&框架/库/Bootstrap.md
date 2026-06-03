# Bootstrap 框架核心组件与类名指南
---

##### 面板组件 (Panels)
[修正类名]：Bootstrap 3 的面板组件类名
```html
<div class="panel panel-default">
    <div class="panel-heading">面板标题</div>
    <div class="panel-body">面板内容</div>
    <div class="panel-footer">面板页脚</div>
</div>

<div class="panel panel-success">
    <div class="panel-heading">成功面板</div>
    <div class="panel-body">操作成功内容</div>
</div>

<p class="text-muted">次要文本颜色</p>
```

[补充说明]：Bootstrap 4+ 已用 card 组件替代 panel
```html
<!-- Bootstrap 4+ 等效代码 -->
<div class="card">
    <div class="card-header">卡片标题</div>
    <div class="card-body">卡片内容</div>
    <div class="card-footer">卡片页脚</div>
</div>
```

##### 表格样式 (Tables)
[修正类名]：
```html
<table class="table table-striped table-hover table-bordered">
    <thead>
        <tr class="table-success">
            <th>表头</th>
        </tr>
    </thead>
    <tbody>
        <tr class="table-info">
            <td>数据行</td>
        </tr>
    </tbody>
</table>
```

##### 其他常用组件
[修正类名]：
```html
<!-- 分页 -->
<nav>
    <ul class="pagination">
        <li class="page-item active"><a class="page-link" href="#">1</a></li>
        <li class="page-item"><a class="page-link" href="#">2</a></li>
    </ul>
</nav>

<!-- 面包屑 -->
<nav>
    <ol class="breadcrumb">
        <li class="breadcrumb-item"><a href="#">首页</a></li>
        <li class="breadcrumb-item active">当前页</li>
    </ol>
</nav>

<!-- 徽章 -->
<span class="badge badge-primary">主标签</span>
<span class="badge badge-danger">危险标签</span>

<!-- 警告框 -->
<div class="alert alert-danger">危险警告信息</div>

<!-- 列表组 -->
<ul class="list-group">
    <li class="list-group-item">列表项1</li>
    <li class="list-group-item active">活动列表项</li>
</ul>
```

##### 网格系统 (Grid System)
[修正说明]：Bootstrap 使用响应式网格系统
```html
<div class="container">
    <div class="row">
        <div class="col-md-4 col-sm-6">中等屏幕4列，小屏幕6列</div>
        <div class="col-md-4 col-sm-6">中等屏幕4列，小屏幕6列</div>
        <div class="col-md-4 col-sm-12">中等屏幕4列，小屏幕12列</div>
    </div>
</div>
```

##### 表单样式 (Forms)
[修正类名]：
```html
<form class="form-inline"> <!-- 行内表单 -->
    <div class="form-group has-success"> <!-- 表单组 -->
        <label class="control-label">邮箱</label>
        <input type="email" class="form-control" placeholder="输入邮箱">
    </div>
    
    <div class="form-group has-warning">
        <label class="control-label">密码</label>
        <input type="password" class="form-control" placeholder="输入密码">
    </div>
    
    <div class="form-group has-error">
        <label class="control-label">验证</label>
        <div class="input-group"> <!-- 输入组 -->
            <span class="input-group-addon">@</span>
            <input type="text" class="form-control" placeholder="用户名">
        </div>
    </div>
</form>
```

##### 按钮样式 (Buttons)
[修正类名]：
```html
<!-- 基础按钮 -->
<button class="btn btn-default">默认按钮</button>
<button class="btn btn-primary">主要按钮</button>
<button class="btn btn-danger">危险按钮</button>
<button class="btn btn-warning">警告按钮</button>
<button class="btn btn-info">信息按钮</button>
<button class="btn btn-link">链接按钮</button>

<!-- 按钮尺寸 -->
<button class="btn btn-primary btn-lg">大按钮</button>
<button class="btn btn-primary btn-sm">小按钮</button>
<button class="btn btn-primary btn-xs">超小按钮</button>

<!-- 按钮状态 -->
<button class="btn btn-primary active">激活状态</button>
<button class="btn btn-primary disabled">禁用状态</button>

<!-- 按钮组 -->
<div class="btn-group btn-group-lg">
    <button class="btn btn-default">左</button>
    <button class="btn btn-default">中</button>
    <button class="btn btn-default">右</button>
</div>
```

##### 导航组件 (Navigation)
[修正类名]：
```html
<!-- 标签式导航 -->
<ul class="nav nav-tabs">
    <li class="active"><a href="#">首页</a></li>
    <li><a href="#">简介</a></li>
    <li><a href="#">联系</a></li>
</ul>

<!-- 胶囊式导航 -->
<ul class="nav nav-pills nav-stacked"> <!-- 堆叠排列 -->
    <li class="active"><a href="#">首页</a></li>
    <li><a href="#">简介</a></li>
    <li><a href="#">联系</a></li>
</ul>

<!-- 导航栏 -->
<nav class="navbar navbar-default">
    <div class="navbar-header">
        <a class="navbar-brand" href="#">品牌标识</a>
    </div>
    <ul class="nav navbar-nav">
        <li class="active"><a href="#">首页</a></li>
        <li><a href="#">页面</a></li>
    </ul>
    <ul class="nav navbar-nav navbar-right">
        <li><a href="#">右侧链接</a></li>
    </ul>
</nav>
```

##### 设计理念说明
[补充说明]：Bootstrap 遵循以下设计原则：
1. **移动优先**：从小屏幕开始设计，逐步增强到大屏幕
2. **响应式设计**：基于12列的网格系统
3. **组件化**：提供预构建的UI组件
4. **实用性**：专注于解决常见的设计问题