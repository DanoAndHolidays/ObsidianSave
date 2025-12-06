# MVVM与MVC
## 1 MVC

![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/56662504fb1b43de86e6b663697945da~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp#?w=743&h=382&s=66496&e=png&b=fdfafa)

### MVC组成
**MVC思想** ：Controller负责将Model的数据用View显示出来。

|MVC|解释|
|---|---|
|① Model（模型）|是应用程序中**用于处理应用程序数据逻辑**的部分。  <br>通常模型对象负责**在数据库中存取数据**。处理数据的crud|
|② View（视图）|是应用程序中处理**数据显示**的部分。通常视图是依据模型数据创建的。视图层，前端|
|③ Controller（控制器）|是应用程序中处理**用户交互**的部分。  <br>**控制器负责从视图读取数据，控制用户输入，并将数据发送给模型。**  <br>一般包括业务处理模块和router路由模块|

### MVC优点
- **耦合度低**（运用MVC的应用程序的三个部件是相互独立的，改变其中一个不会影响其他两个）；
- 重用性高（多个视图可以使用同一个模型）
- 生命周期成本低
- 部署快（业务分工明确）
- **可维护性高**
### MVC缺点：
- 不适合小型项目开发
- **视图与控制器联系过于紧密**，妨碍了它们的独立重用
## 2 MVVM——视图模型双向绑定（谈谈你对MVVM开发模式的理解）

![image.png](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/86732b9278e74d6c857d72ea77995d2d~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp#?w=796&h=411&s=20174&e=png&b=fefdfd)
### MVVM 组成：
MVVM由Model，View，ViewModel三部分构成。

|M V VM|解释|
|---|---|
|Model|代表数据模型（Vue的data），**数据和业务逻辑**都在Model层中定义；|
|View|代表UI视图，负责**数据的展示**（Vue的el）；|
|ViewModel|是一个对象，负责**监听 Model 中数据的改变**并且**控制View视图的更新**，处理用户交互操作；|

- **Model** 和 **View** 并无直接关联，而是通过 **ViewModel** 来进行交互的（即双向数据绑定），
- **Model** 和 **ViewModel**之间有着**双向数据绑定的联系**。  
    View的变化可以引起Model的变化，Model的变化也可以引起View变化（类似于浅拷贝）。`ViewModel`是`View`和`Model`层的桥梁，数据会绑定到`viewModel`层并自动将数据渲染到页面中，视图变化的时候会通知`viewModel`层更新数据。
### MVVM 优点：
- 低耦合：
    - 视图（View）可以独立于Model变化和修改，**一个Model可以绑定到不同的View上**，
    - 当View变化的时候Model可以不变化，当Model变化的时候View也可以不变；
- 可重用性：你可以把一些视图逻辑放在一个Model里面，让很多View重用这段视图逻辑。
- 独立开发：**双向数据绑定的模式，实现了View和Model的自动同步，因此开发者只需要专注对数据的维护操作即可，而不需要一直操作 dom。**  
    可以实现双向绑定的标签：Input，textarea，select标签等（可以输入或改变标签内容的标签）

![MVVM2.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/4e8980cd36bb4c78856500307dd289f9~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp#?w=720&h=483&s=38876&e=jpg&b=fbf9fc)

- MVVM 和 MVC都是一种设计思想。
- MVVM 与 MVC 最大的**区别**就是：它实现了**View和Model的自动同步**
    - 当Model属性改变时，不用手动操作Dom元素去改变View的显示。
    - 而改变属性后，该属性对应View的显示会自动改变