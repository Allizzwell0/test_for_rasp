#!/usr/bin/python
#从ms5837-python中导入ms5837模块
#!/usr/bin/python
import sys
import os

# 添加模块路径
current_dir = os.path.dirname(os.path.abspath(__file__))
ms5837_path = os.path.join(current_dir, 'ms5837-python')
sys.path.append(ms5837_path)
# print(ms5837_path)

import ms5837
import time
from brping import Ping1D
import argparse
from builtins import input
import serial.tools.list_ports

'''
# 深度计
# 此处查询手册获得当前对应具体bus参数
sensor = ms5837.MS5837_30BA(bus=1) # Default I2C bus is 1 (Raspberry Pi 3)
#sensor = ms5837.MS5837_30BA(0) # Specify I2C bus
#sensor = ms5837.MS5837_02BA()
#sensor = ms5837.MS5837_02BA(0)
#sensor = ms5837.MS5837(model=ms5837.MS5837_MODEL_30BA, bus=0) # Specify model and bus

# We must initialize the sensor before reading it
if not sensor.init():
    print("Sensor could not be initialized")
    exit(1)

# We have to read values from sensor to update pressure and temperature
if not sensor.read():
    print("Sensor read failed!")
    exit(1)

# 压力读取
print(("Pressure: %.2f atm  %.2f Torr  %.2f psi") % (
sensor.pressure(ms5837.UNITS_atm),
sensor.pressure(ms5837.UNITS_Torr),
sensor.pressure(ms5837.UNITS_psi)))
# 温度读取
print(("Temperature: %.2f C  %.2f F  %.2f K") % (
sensor.temperature(ms5837.UNITS_Centigrade),
sensor.temperature(ms5837.UNITS_Farenheit),
sensor.temperature(ms5837.UNITS_Kelvin)))

# 根据不同密度计算深度
freshwaterDepth = sensor.depth() # default is freshwater
sensor.setFluidDensity(ms5837.DENSITY_SALTWATER)
saltwaterDepth = sensor.depth() # No nead to read() again
sensor.setFluidDensity(1000) # kg/m^3
print(("Depth: %.3f m (freshwater)  %.3f m (saltwater)") % (freshwaterDepth, saltwaterDepth))

# fluidDensity doesn't matter for altitude() (always MSL air density)
print(("MSL Relative Altitude: %.2f m") % sensor.altitude()) # relative to Mean Sea Level pressure in air

time.sleep(5)

# Spew readings
# while True:
#         time.sleep(1)
#         if sensor.read():
#                 print(("P: %0.1f mbar  %0.3f psi\tT: %0.2f C  %0.2f F") % (
#                 sensor.pressure(), # Default is mbar (no arguments)
#                 sensor.pressure(ms5837.UNITS_psi), # Request psi
#                 sensor.temperature(), # Default is degrees C (no arguments)
#                 sensor.temperature(ms5837.UNITS_Farenheit))) # Request Farenheit
#         else:
#                 print("Sensor read failed!")
#                 exit(1)
'''

# 高度计
def list_serial_ports():
    """列出所有可用的串口设备"""
    ports = serial.tools.list_ports.comports()
    available_ports = []
    for port, desc, hwid in sorted(ports):
        print(f"{len(available_ports)+1}: {port} - {desc}")
        available_ports.append(port)
    return available_ports

def select_serial_port():
    """让用户选择串口设备"""
    available_ports = list_serial_ports()
    if not available_ports:
        print("未找到可用的串口设备")
        return None
    
    while True:
        try:
            choice = int(input("请选择串口设备编号 (输入0退出): "))
            if choice == 0:
                return None
            if 1 <= choice <= len(available_ports):
                return available_ports[choice-1]
            print("无效的选择，请重试")
        except ValueError:
            print("请输入有效的数字")

def init_ping_sensor(port):
    """初始化Ping传感器"""
    ping = Ping1D()
    if port is not None:
        ping.connect_serial(port, 115200)
        print("连接到Ping设备: %s" % port)
        return ping
    if not ping.initialize():
        print("无法初始化Ping传感器")
        return None

def main():
    # 选择串口设备
    selected_port = select_serial_port()
    # print(selected_port)
    if selected_port is None:
        print("未选择设备，程序退出")
        exit(1)
    
    print(f"选择的串口设备: {selected_port}")
    
    # 初始化Ping传感器
    ping = init_ping_sensor(selected_port)
    if ping is None:
        print("传感器初始化失败，程序退出")
        exit(1)
    
    print("------------------------------------")
    print("Starting Ping..")
    print("Press CTRL+C to exit")
    print("------------------------------------")
    
    input("Press Enter to continue...")
    
    # 主循环读取数据
    try:
        while True:
            data = ping.get_distance()
            if data:
                print("Distance: %s\tConfidence: %s%%" % (
                    data["distance"], data["confidence"]))
            else:
                print("Failed to get distance data")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n程序已退出")

if __name__ == "__main__":
    main()
