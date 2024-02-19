# ESP32_bemfa_MQTT
micropython ESP32基于巴法云MQTT通信
# 使用

---

```
micropython ESP32基于巴法云MQTT通信，可用于第三方接入：

1.配置 IoTDevice 类初始化参数
2.插入执行函数入回调函数
```
# Example

---

```python
# mqtt通信控制led灯
...
class IoTDevice:
    def __init__(self):
        self.client = None
        self.wifiName = 'wifi name'
        self.wifiPass = 'wifi password'
        # 初始化 MQTT  参数
        self.clientID = 'bemfa client id'
        self.serverIP = 'bemfa.com'
        self.serverPort = 9501
        self.topicName = b'topic name'

        led = Pin(2, Pin.OUT)  # 插入初始化参数
    ...
    #  回调函数
    def sub_cb(self, topic, msg):
        if topic == self.topicName:
            print(msg.decode())
            if msg.decode() == 'on':
                led.value(1)  # 插入执行函数
            elif msg.decode() == 'off':
                led.value(0)  # 插入执行函数
...
```
