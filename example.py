# mqtt 远程通信控制 led 例子
from machine import reset, Timer, Pin
import network
from umqtt.simple import MQTTClient
import time


# IoT 类
class IoTDevice:
    def __init__(self):
        self.client = None
        self.wifiName = '****-2.4G'
        self.wifiPass = '************'
        # 初始化 MQTT  参数
        self.clientID = '************************'
        self.serverIP = 'bemfa.com'
        self.serverPort = 9501
        self.topicName = b'****'

    # WIFI 连接
    def client_wifi(self):
        wlan = network.WLAN(network.STA_IF)
        if not wlan.isconnected():
            wlan.active(True)
            wlan.connect(self.wifiName, self.wifiPass)
        while not wlan.isconnected():
            pass

    # MQTT 连接
    def client_mqtt(self):
        client = MQTTClient(self.clientID, self.serverIP, self.serverPort)
        client.connect()
        client.set_callback(self.sub_cb)
        client.subscribe(self.topicName)
        return client

    # MQTT 心跳
    def heart_beat(self, t):
        try:
            self.client.publish(topic=f'{self.topicName}/set', msg="MQTT server", qos=0)
        except:
            self.machine_reset()

    # MQTT 设备重置
    def machine_reset(self):
        time.sleep(10)
        reset()

    #  回调函数
    def sub_cb(self, topic, msg):
        if topic == self.topicName:
            print(msg.decode())
            if msg.decode() == 'on':
                self.led.value(1)

            elif msg.decode() == 'off':
                self.led.value(0)


def main():
    device = IoTDevice()
    device.client_wifi()

    try:
        device.client = device.client_mqtt()
    except OSError as e:
        device.machine_reset()

    # 设置定时心跳
    tim = Timer(-1)
    tim.init(period=10000, mode=Timer.PERIODIC, callback=device.heart_beat)

    while True:
        try:
            device.client.check_msg()
            time.sleep_ms(100)
        except OSError as e:
            device.machine_reset()


if __name__ == '__main__':
    main()
