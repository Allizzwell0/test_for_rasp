# 项目名称

此部分主要为raspberry读取高度计以及深度计数据测试代码，注意长时间未启动树莓派后，其远程ip可能更改，需要进行再次确认与设置

## 目录

- [参考](#参考)
- [使用](#使用)
- [debug记录](#debug)
## 参考
关于深度计部分，主要参考：
https://github.com/searobotix/ms5837-python
https://searobotix.com/b30/download/b30-sensor-tutorial-stm32/
https://pidoc.cn/gpiozero/recipes
https://github.com/searobotix/ping-python
## 使用
深度计数据传输使用I2C协议，查询手册有两组I2C接口，注意接线：
![引脚图](./picture/pinout.png)
![接线对应图](./picture/wire.png)
之后数据读取部分参考readdata即可

高度计的测试文件为ping-python，其中bluerobotics_ping无法直接安装，目前采用办法为强行安装该包：

`sudo pip install bluerobotics-ping --upgrade --break-system-packages
`

除此之外实测高度计confidence很低，猜测和使用环境有关

## debug

### 1. 模块导入问题 (2025-1-13）
- 问题描述: ms5837 模块无法正常导入
- 解决方案: 
  1. 添加模块路径到 PYTHONPATH
  2. 使用 sys.path.append() 添加本地模块路径
  ```python
  import sys
  sys.path.append('./ms5837-python')

### 2. 串口权限问题 （2025-1-14）
- 问题描述：brping模块无法导入
- 解决方案：
  1. 参考前文强行安装bluerobotics_ping模块，在具体执行时文件没有读取对应串口的权限，会判定问题为包未安装
  2. 解决方法为给予文件执行权限 

### 3. 高度计置信度低（2025-1-14）
- 问题描述： 高度计采集数据计算有误，置信度极低（0-20%），猜测并非水下环境测试导致（未解决）