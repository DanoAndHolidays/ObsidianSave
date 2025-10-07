### BV1GBdUYqE77
### 环境配置
- 使用Miniconda来管理Python虚拟环境
---
### 环境管理命令
- 查看环境：`conda env list`
- 新建：
	- 检查Python版本：`python --version`
	- 新建环境：`conda create -n yolo python=3.12.7`（注意版本号）
- 激活环境：`conda activate yolo`
- 在vscode选择解释器的位置选择环境
---
### 安装包
- 安装pytorch：`pip install torch torchvision torchaudio`
- 安装jupyterlab：`pip install jupyterlab`
- 安装ultralytics：将本地下载的包安装到环境
---
### 初体验
使用指令来指定模型，任务，和要识别的资源
```
 yolo mode='predict' task='detect' model='yolo11n.pt' source='textimg.png'
```
其中的模式、任务可以不使用，具有默认值

对于使用py来实现的代码
```
from ultralytics import YOLO
yolo=YOLO(model='yolo11n.pt',task='detect')
result = yolo(source='textmp4.mp4',save=True);//source的部分可以改成'0'代表摄像头、'screen'代表屏幕
```
ctrl+c停止 ctrl+j调出新的控制台

---
### 参数设置
**ultralytics\cfg\default.yaml**在此处有所有的参数，也可以修改其中的默认值，官网也有，举例：
- **save**：在使用py运行时，不使用save=’true‘就不会存储数据
- **conf**：conf=’0.66‘这里表示置信空间，表示超过这个值后才显示
- **show**：表示展示
- **save_txt**：表示文本存储

---
### Jupyterlab
使用后缀.ipynb来创建一个文件，在此文件的右上角选着环境（要安装对应的扩展）
使用B来创建新的段，回车来进入编辑模式

用这个可以来分块的运行代码，将代码注入到内存中

---
### 结果
在Jupyterlab的代码中使用这样的代码块能够方便的查看
```
from ultralytics import YOLO
yolo=YOLO(model='yolo11n.pt',task='detect')
result = yolo(source='text2.mp4',save=True,save_txt=True,show=True,conf=0.6);
```

```
display(result[0].names)
display(result[0].names)
```
---
### 数据准备
**准备数据集**：准备各种情况的图片并且重命名
**标记**：使用Labelimg来标记数据。创建项目文件夹并在其中创建两个新的文件夹，分别用来存储数据和标注好的数据
- 开启自动保存更加方便
- ==切换模型到YOLO==
- 使用W来快捷标注
- A、D来切换上下图片

这里是推荐的文件结构：
- datasets
	- icon
		- images
			- train：用于训练
			- val：检验
		- labels
			- classes.txt
			- train：用于训练
			- val：检验

最后将文件夹添加至项目文件夹

---
### 训练
准备yaml文件，yaml要放置在和ultralytics同级的目录下
```
path: ../datasets/coco # dataset root dir
train: train2017.txt # train images (relative to 'path') 118287 images
val: val2017.txt # val images (relative to 'path') 5000 images
test:

names:
  0: person
  1: bicycle
  2: car
  3: motorcycle
```
文件的模版ultralytics\cfg\datasets，可以参考
```
from ultralytics import YOLO
model= YOLO('yolo11n.pt')
model.train(data='yaml',workers=0,eposhs=300,batch=16)
//使用eposhs来指定训练的轮数，workers0代表windows
```
在训练结束后的detect/train文件的weights里有训练好的模型
在results.png中记录了训练的结果，类似1/x的曲线代表较好的训练结果

---
### 使用新训练的模型
与初体验中的一样

---
