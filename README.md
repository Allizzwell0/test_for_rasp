# 项目名称

此部分主要为raspberry读取高度计以及深度计数据测试代码

## 目录

- [参考](#参考)
- [使用](#使用)
## 参考
关于深度计部分，主要参考：
https://github.com/searobotix/ms5837-python
https://searobotix.com/b30/download/b30-sensor-tutorial-stm32/
https://pidoc.cn/gpiozero/recipes
## 使用
深度计数据传输使用I2C协议，查询手册只有一组I2C接口，注意接线：
![引脚图](./picture/pinout.png)
![接线对应图](./picture/wire.png)
之后数据读取部分参考readdata即可