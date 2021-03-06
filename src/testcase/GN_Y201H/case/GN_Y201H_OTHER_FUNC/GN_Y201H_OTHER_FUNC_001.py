# coding=utf-8
from src.testcase.GN_Y201H.WidgetOperation import *


class GNY201HOtherFunc1(WidgetOperation):
    @case_run(False)
    def run(self):
        self.case_module = u"其他功能(#247)"  # 用例所属模块
        self.case_title = u'APP查看信息功能'  # 用例名称
        self.zentao_id = "2088"  # 禅道ID

    # 用例动作
    def case(self):
        self.choose_home_device(conf["MAC"]["HW"][0])

        self.set_power("power_off")

        self.widget_click(self.page["control_device_page"]["device_setting"],
                          self.page["device_setting_page"]["title"])

        self.widget_click(self.page["device_setting_page"]["device_info"],
                          self.page["device_info_page"]["title"])

        mac = self.ac.get_attribute(self.wait_widget(self.page["device_info_page"]["mac"]), "name")

        serial_number = self.ac.get_attribute(self.wait_widget(self.page["device_info_page"]["serial_number"]), "name")

        device_model = self.ac.get_attribute(self.wait_widget(self.page["device_info_page"]["device_model"]), "name")

        if "".join(mac.split(":")) != serial_number:
            raise TimeoutException("Mac is error, current: Mac: %s; serial_number: %s" % (mac, serial_number))
        if device_model != "GN-Y201H":
            raise TimeoutException("device_model is error, current: device_model: %s" % device_model)
