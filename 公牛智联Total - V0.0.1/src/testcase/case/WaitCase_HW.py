# coding=utf-8
from src.testcase.case.HWAPP.INPUT_CASE.HWAppInputCase import *

from src.testcase.page.ReadAPPElement import *
from src.utils.CollectLog import *
from src.utils.Debug import *
from src.utils.OutputReport import *
from src.utils.WriteXls import *


class ScriptInitError(Exception):
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return repr(self.value)


class WaitCaseHW(object):
    def __init__(self, device_list, device_name, m_queue):
        self.device_list = device_list  # 设备列表
        self.device_name = device_name  # 设备名称
        self.device_info = device_list[device_name]  # 设备信息集
        self.app = self.device_info["app"]  # 运行APP信息
        database["m_queue"] = m_queue  # 用于主进程和子进程通讯的消息队列

        self.report = None  # 初始化结果报告模块
        self.logger = None  # 初始化log日志模块
        self.xls = None  # 初始化执行结果Excel文件模块
        self.debug = None  # 初始化debug日志模块
        self.script_init_success = False  # 脚本初始化结果标志位
        database["case_location"] = 1  # 用例执行次数
        self.row = 12  # Excel报告写入初始位置

        self.sc = ShellCommand()  # 实例化ShellCommand
        database[device_name] = {}  # 初始化设备数据库

        try:
            self.create_debug()
            self.create_log()
            self.create_report()
            self.write_xls()
            self.select_page_element()
            self.check_appium()
            self.init_app()
            self.script_init_success = True
        except BaseException:
            self.debug.error(traceback.format_exc())
            raise
        if self.script_init_success is True:
            self.run()
        else:
            raise ScriptInitError("Script Init Error!!! "
                                  "contain [create_debug(), create_log(), "
                                  "create_report(), write_xls(), check_appium()]")

    # 从元素库筛选对应APP元素库
    def select_page_element(self):
        PageElement(self.device_list, self.device_info["platformName"], self.device_info["app"]).wrapper()
        self.page_element = self.device_list["page"]

    # 生成log日志
    def create_log(self):
        check_log(self.device_list, self.device_name)
        self.logger = self.device_info["logger"]

    # 生成log格式运行结果
    def create_report(self):
        check_report(self.device_list, self.device_name)
        self.report = self.device_info["report"]

    # 生成debug日志
    def create_debug(self):
        check_debug(self.device_list, self.device_name)
        self.debug = self.device_info["debug"]

    # 实例化Excel文件
    def write_xls(self):
        self.xls = WriteXls(self.device_list, self.device_name)

    # 初始化启动APP
    def init_app(self):
        self.device_info_list = {"device_info": self.device_info,
                                 "page_element": self.page_element,
                                 "logger": self.logger,
                                 "app": self.app,
                                 "sc": self.sc}

    # 检查Appium服务是否启动
    def check_appium(self):
        while True:
            try:
                self.sc.find_proc_and_pid_by_port(self.device_info["port"])[0]
            except IndexError:
                time.sleep(1)
            else:
                self.logger.info("Appium Sever Launch Success! %s" % time.strftime("%Y-%m-%d %X"))
                break

    # 开始执行用例
    def run(self):
        # 填写设备信息日志
        self.logger.info("*" * 30)
        self.logger.info(u"[APP_INF]deviceName：.....%s" % self.device_info["deviceName"])
        self.logger.info(u"[APP_INF]UDID：...........%s" % self.device_info["udid"])
        self.logger.info(u"[APP_INF]platformName：...%s" % self.device_info["platformName"])
        self.logger.info(u"[APP_INF]platformVersion：%s" % self.device_info["platformVersion"])

        # self.logger.info(u"[APP_INF]appPackage：.....%s" % self.device_info["desired_caps"]["appPackage"])
        # self.logger.info(u"[APP_INF]appActivity：....%s" % self.device_info["desired_caps"]["appActivity"])
        # self.logger.info(u"[APP_INF]waitActivity：...%s" % self.device_info["desired_caps"]["waitActivity"])
        # self.logger.info(u"[APP_INF]bundleId：.......%s" % self.device_info["desired_caps"]["bundleId"])
        # self.logger.info("******************************")
        for name, blank in [["appPackage", 5], ["appActivity", 4], ["waitActivity", 3], ["bundleId", 7]]:
            try:
                self.logger.info(u"[APP_INF]%s：%s%s" % (name, "." * blank, self.device_info["desired_caps"][name]))
            except KeyError:
                pass
        self.logger.info("*" * 30)

        # 执行用例
        while True:
            self.logger.info("run times [%s]" % database["program_loop_time"])
            self.write_report(HWAppControl1)  # 2106, 在线状态，频繁开关操作后，状态检查
            self.write_report(HWAppControl2)  # 2105, 在线状态，开关操作后，状态检查
            self.write_report(HWAppDelayTimer1)  # 2100, 延时定时设置后，改变设备状态后查看延时定时的执行状态
            self.write_report(HWAppDelayTimer2)  # 2099, 在线状态，1组单关的延时定时执行状态检查
            self.write_report(HWAppDelayTimer3)  # 2098, 在线状态，1组单开的延时定时执行状态检查
            # self.write_report(HWAppNormalTimer1)  # 2079, 在线状态，临界点1组开与1组关的定时执行状态检查
            # self.write_report(HWAppNormalTimer2)  # 2064, 在线状态，4组开与4组关按自定义方式执行的定时执行状态检查
            # self.write_report(HWAppNormalTimer3)  # 2063, 在线状态，4组开与4组关按周末方式执行的定时执行状态检查
            # self.write_report(HWAppNormalTimer4)  # 2062, 在线状态，4组开与4组关按工作日方式执行的定时执行状态检查
            self.write_report(HWAppNormalTimer5)  # 2061, 在线状态，4组开与4组关单次执行的定时执行状态检查
            # self.write_report(HWAppNormalTimer6)  # 2060, 在线状态，1组开与1组关按自定义方式执行的定时执行状态检查
            # self.write_report(HWAppNormalTimer7)  # 2059, 在线状态，1组开与1组关按周末执行的定时执行状态检查
            # self.write_report(HWAppNormalTimer8)  # 2058, 在线状态，1组开与1组关按工作日执行的定时执行状态检查
            # self.write_report(HWAppNormalTimer9)  # 2057, 在线状态，临界点1组开与1组关的定时执行状态检查
            self.write_report(HWAppNormalTimer10)  # 2056, 在线状态，1组开与1组关定时执行状态检查
            self.write_report(HWAppNormalTimer11)  # 2055, 在线状态，1组单关定时执行状态检查
            self.write_report(HWAppNormalTimer12)  # 2054, 在线状态，1组单开定时执行状态检查
            self.write_report(HWAppOtherFunc1)  # 2088, APP查看信息功能
            # self.write_report(HWAppSmartLink1)  # 2048, 设备首次配网操作检查
            self.write_report(HWAppTimerFunc1)  # 2023, 延时定时的定时数量检查
            self.write_report(HWAppTimerFunc2)  # 2022, 普通定时的定时数量检查
            self.write_report(HWAppTimerFunc3)  # 2020, 普通定时周期格式检查

            database["program_loop_time"] += 1

    # 输出报告
    def write_report(self, case_name):
        try:
            case = case_name(**self.device_info_list).run()

            end = time.strftime("%Y-%m-%d %X")
            d = (u'[ZENTAO_ID=%s, RESULT=%s CASE_TITLE="%s", RUN_TIMES=%s, CASE_ID=%s, START=%s, CLOSE=%s]' % (
                case[0], case[1], case[2], database["program_loop_time"], database["case_location"], case[3], end))
            self.report.info(d)

            zentao_id = case[0]
            xls_data = database[self.device_name]
            xls_data[zentao_id]["end_time"] = end
            if "row" in xls_data[zentao_id].keys():
                pass
            else:
                xls_data[zentao_id]["row"] = self.row
                self.row += 1
            self.debug.info("row: %s" % xls_data[zentao_id]["row"])
            self.xls.write_data(xls_data[zentao_id]["row"],
                                xls_data[zentao_id]["ZenTao"],
                                xls_data[zentao_id]["case_title"],
                                xls_data[zentao_id]["end_time"],
                                xls_data[zentao_id]["test_count"],
                                xls_data[zentao_id]["test_pass"],
                                xls_data[zentao_id]["test_fail"],
                                xls_data[zentao_id]["test_error"],
                                xls_data[zentao_id]["test_wait"])

            self.debug.info("write_data: %s" % xls_data[zentao_id])
            database["case_location"] += 1
        except BaseException:
            self.debug.error(traceback.format_exc())
