#   树莓派电子钟

## 使用方法

```Bash
sudo pigpiod # 开启pigpio的守护进程
sudo python main.py &
```

## 项目介绍

使用了 *微雪电子* 的**2.9inch墨水屏**和**dht11温度湿度传感器**，通过**高德API**读取位置信息和天气信息。

每分钟更新室内温湿度和随机（？）表情，每小时更新室外温湿度和天气信息，每六小时全局刷新屏幕以防残影。

在**树莓派zero w**上开发完成

![image](https://user-images.githubusercontent.com/32357397/64483494-0164e580-d235-11e9-97bd-c8b8d968165f.png)

使用 *shapr3d* 设计并用树脂打印了外壳，但是目前仍有需要修改的地方，譬如屏幕开口没对准QAQ，还有就是温度传感器由于外壳封闭导致测得的温度过高。

使用LED灯带来提升夜间的使用体验。

后期考虑增加闹钟功能。

## 引用的库

[Adafruit Python DHT](https://github.com/adafruit/Adafruit_Python_DHT)

[微雪电子官方电子纸例程](https://github.com/waveshare/e-Paper)
