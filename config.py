import re
import uuid
from typing import List

import toml

from const import *
from data_struct import ConfigInterface
from log import *
from sign import getACSRFTokenForAMS, getDjcSignParams
from util import *

encoding_error_str = "Found invalid character in key name: '#'. Try quoting the key name. (line 1 column 2 char 1)"


class AccountInfoConfig(ConfigInterface):
    def __init__(self):
        # 手动登录需要设置的信息
        self.uin = "o123456789"
        self.skey = "@a1b2c3d4e"

        # 自动登录需要设置的信息
        self.account = "123456789"
        self.password = "使用账号密码自动登录有风险_请审慎决定"


class MobileGameRoleInfoConfig(ConfigInterface):
    def __init__(self):
        # 手游名称: 无/任意手游/剑网3:指尖江湖/和平精英/王者荣耀/QQ飞车手游/天天酷跑/其他任意游戏，可参考djc_biz_list.json获取完整列表
        self.game_name = "任意手游"

    def enabled(self):
        return self.game_name not in ["无", "none"]

    def use_any_binded_mobile_game(self):
        return self.game_name in ["任意手游"]


class ExchangeItemConfig(ConfigInterface):
    def __init__(self):
        self.iGoodsId = "753"
        self.sGoodsName = "装备品级调整箱（5个）"
        self.count = 2


class DnfHelperChronicleExchangeItemConfig(ConfigInterface):
    def __init__(self):
        self.sLbcode = "ex_0003"
        self.sName = "装备提升礼盒*1"
        self.count = 3


class XinYueOperationConfig(ConfigInterface):
    def __init__(self):
        self.iFlowId = "512411"
        self.package_id = ""  # 仅礼包兑换需要这个参数，如兑换【勇者宝库】的【装备提升礼盒】的package_id为702218
        self.sFlowName = "输出我的任务积分"
        self.count = 1


class WegameGuoqingExchangeItemConfig(ConfigInterface):
    def __init__(self):
        self.iFlowId = "703514"
        self.sGoodsName = "强化器-4分"
        self.count = 1


class ArkLotteryAwardConfig(ConfigInterface):
    def __init__(self):
        self.name = "勇士归来礼包"
        self.ruleid = 25947
        self.count = 1


class ArkLotteryConfig(ConfigInterface):
    def __init__(self):
        # 用于完成幸运勇士的区服ID和角色ID，若服务器ID留空，则使用道聚城绑定的dnf角色信息
        self.lucky_dnf_server_id = ""  # 区服id可查阅reference_data/dnf_server_list.js
        self.lucky_dnf_role_id = ""  # 角色ID，不知道时可以填写区服ID，该数值留空，这样处理到抽卡的时候会用黄色字体打印出来信息
        # 是否消耗所有卡牌来抽奖（建议在兑换完所有礼包后再开启这个功能）
        self.cost_all_cards_and_do_lottery = False
        # 尝试领取礼包的次数：勇士归来礼包=25947，超低门槛=25948，人人可玩=25966，幸运礼包=25939
        self.take_awards = []  # type: List[ArkLotteryAwardConfig]

        # 是否展示在概览界面
        self.show_status = True
        # 卡牌数目使用特定的颜色
        self.show_color = ""

    def auto_update_config(self, raw_config: dict):
        super().auto_update_config(raw_config)

        if 'take_awards' in raw_config:
            self.take_awards = []
            for cfg in raw_config["take_awards"]:
                ei = ArkLotteryAwardConfig()
                ei.auto_update_config(cfg)
                self.take_awards.append(ei)


class DnfHelperInfoConfig(ConfigInterface):
    def __init__(self):
        # userId/nickName的获取方式为，点开dnf助手中点开右下角的【我的】，然后点击右上角的【编辑】按钮，则社区ID即为userId，昵称即为nickname，如我的这俩值为504051073、风之凌殇
        # 社区ID
        self.userId = ""
        # 昵称
        self.nickName = ""
        # 登录票据，目前需手动更新。
        # 流程：
        #   1. 打开dnf助手并确保已登录账户，点击活动，找到【艾丽丝的密室，塔罗牌游戏】并点开，点击右上角分享，选择QQ好友，发送给【我的电脑】。
        #   2. 在我的电脑聊天框中的链接中找到请求中的token（形如&token=tW7AbaM7，则token为tW7AbaM7），将其进行更新到配置文件中
        #
        # ps: 如果有多个账号需要领取这个，请不要在手机上依次登入登出执行上述步骤来获取token，因为你在登陆下一个账号的时候，之前的账号的token就因为登出而失效了
        #       有这个需求的话，请使用安卓模拟器的多开功能来多开dnf助手去登陆各个账号。如果手机支持多开app，也可以使用对应功能。具体多开流程请自行百度搜索： 手机 app 多开
        self.token = ""

        # dnf助手编年史是否开启抽奖
        self.chronicle_lottery = False
        # dnf助手编年史兑换道具信息，其他奖励信息可查阅reference_data/dnf助手编年史活动_可兑换奖励列表.json
        self.chronicle_exchange_items = []  # type: List[DnfHelperChronicleExchangeItemConfig]

    def auto_update_config(self, raw_config: dict):
        super().auto_update_config(raw_config)

        if 'chronicle_exchange_items' in raw_config:
            self.chronicle_exchange_items = []
            for cfg in raw_config["chronicle_exchange_items"]:
                ei = DnfHelperChronicleExchangeItemConfig()
                ei.auto_update_config(cfg)
                self.chronicle_exchange_items.append(ei)


class HelloVoiceInfoConfig(ConfigInterface):
    def __init__(self):
        # hello语音的用户ID
        # 获取方式：打开hello语音，点击右下角【我的】tab，在最上方头像框的右侧，昵称下方，有形如【ID：XXXXXX】的字样，其中ID后面这串数字就是用户ID
        self.hello_id = ""


class FunctionSwitchesConfig(ConfigInterface):
    def __init__(self):
        # 是否领取道聚城
        self.get_djc = True
        # 是否领取心悦特权专区
        self.get_xinyue = True
        # 是否领取腾讯游戏信用相关礼包
        self.get_credit_xinyue_gift = True
        # 是否领取每月黑钻等级礼包
        self.get_heizuan_gift = True
        # 是否领取DNF进击吧赛利亚活动
        self.get_xinyue_sailiyam = True
        # 是否领取wegame国庆活动
        self.get_wegame_guoqing = True
        # 是否领取阿拉德集合站活动
        self.get_dnf_922 = True
        # 是否领取2020DNF闪光杯返场赛活动
        self.get_dnf_shanguang = True
        # 是否领取qq视频活动
        self.get_qq_video = True
        # 是否领取10月女法师三觉活动
        self.get_dnf_female_mage_awaken = True
        # 是否领取管家蚊子腿活动
        self.get_guanjia = True
        # 是否启用许愿功能，用于完成《有理想》。目前仅限安卓版本道聚城上绑定王者荣耀时可使用
        self.make_wish = True
        # 是否启用集卡功能
        self.get_ark_lottery = True
        # 是否领取DNF助手排行榜活动
        self.get_dnf_rank = True
        # 是否启用阿拉德勇士征集令活动
        self.get_dnf_warriors_call = True
        # 是否领取dnf助手编年史活动
        self.get_dnf_helper_chronicle = True
        # 是否启用hello语音奖励兑换功能
        self.get_hello_voice = True


class AccountConfig(ConfigInterface):
    def __init__(self):
        # 是否启用该账号
        self.enable = True
        # 账号名称，仅用于区分不同账号
        self.name = "默认账号"
        # 测试模式，若开启，则一些实验性功能将会启用
        self.test_mode = False
        # 登录模式
        # by_hand：      手动登录，在skey无效的情况下会弹出活动界面，自行登录后将cookie中uin和skey提取到下面的配置处
        # qr_login：     二维码登录，每次运行时若本地缓存的.skey文件中存储的skey过期了，则弹出登录页面，扫描二维码后将自动更新skey，进行后续操作
        # auto_login：   自动登录，每次运行若本地缓存的.skey文件中存储的skey过期了，根据填写的账密信息，自动登录来获取uin和skey，无需手动操作
        self.login_mode = "by_hand"
        # 是否无法在道聚城绑定dnf，比如被封禁或者是朋友的QQ（主要用于小号，被风控不能注册dnf账号，但是不影响用来当抽卡等活动的工具人）
        self.cannot_band_dnf = False
        # 各功能开关
        self.function_switches = FunctionSwitchesConfig()
        # 腾讯系网页登录通用账号凭据与token
        self.account_info = AccountInfoConfig()
        # 完成《礼包达人》任务所需的手游的名称信息
        self.mobile_game_role_info = MobileGameRoleInfoConfig()
        # 兑换道具信息
        self.exchange_items = []  # type: List[ExchangeItemConfig]
        # 心悦相关操作信息
        self.xinyue_operations = []  # type: List[XinYueOperationConfig]
        # 抽卡相关配置
        self.ark_lottery = ArkLotteryConfig()
        # wegame国庆活动兑换道具，具体道具的iFlowId和描述可参考reference_data/wegame国庆活动.json
        self.wegame_guoqing_exchange_items = []  # type: List[WegameGuoqingExchangeItemConfig]
        # dnf助手信息
        self.dnf_helper_info = DnfHelperInfoConfig()
        # hello语音相关信息
        self.hello_voice = HelloVoiceInfoConfig()

    def auto_update_config(self, raw_config: dict):
        super().auto_update_config(raw_config)

        if 'exchange_items' in raw_config:
            self.exchange_items = []
            for cfg in raw_config["exchange_items"]:
                ei = ExchangeItemConfig()
                ei.auto_update_config(cfg)
                self.exchange_items.append(ei)

        if 'xinyue_operations' in raw_config:
            self.xinyue_operations = []
            for cfg in raw_config["xinyue_operations"]:
                ei = XinYueOperationConfig()
                ei.auto_update_config(cfg)
                self.xinyue_operations.append(ei)

        if 'wegame_guoqing_exchange_items' in raw_config:
            self.wegame_guoqing_exchange_items = []
            for cfg in raw_config["wegame_guoqing_exchange_items"]:
                ei = WegameGuoqingExchangeItemConfig()
                ei.auto_update_config(cfg)
                self.wegame_guoqing_exchange_items.append(ei)

        self.on_config_update(raw_config)

    def is_enabled(self):
        return self.enable

    def on_config_update(self, raw_config: dict):
        self.sDeviceID = self.getSDeviceID()
        self.aes_key = "84e6c6dc0f9p4a56"
        self.rsa_public_key_file = "public_key.der"

        self.updateUinSkey(self.account_info.uin, self.account_info.skey)

    def updateUinSkey(self, uin, skey):
        self.account_info.uin = uin
        self.account_info.skey = skey

        self.g_tk = str(getACSRFTokenForAMS(self.account_info.skey))
        self.sDjcSign = getDjcSignParams(self.aes_key, self.rsa_public_key_file, uin2qq(self.account_info.uin), self.sDeviceID, appVersion)

    def getSDeviceID(self):
        sDeviceIdFileName = os.path.join(cached_dir, ".sDeviceID.{}.txt".format(self.name))

        if os.path.isfile(sDeviceIdFileName):
            with open(sDeviceIdFileName, "r", encoding="utf-8") as file:
                sDeviceID = file.read()
                if len(sDeviceID) == 36:
                    # print("use cached sDeviceID", sDeviceID)
                    return sDeviceID

        sDeviceID = str(uuid.uuid1())
        # print("create new sDeviceID", sDeviceID, len(sDeviceID))

        with open(sDeviceIdFileName, "w", encoding="utf-8") as file:
            file.write(sDeviceID)

        return sDeviceID


class LoginConfig(ConfigInterface):
    def __init__(self):
        # 重试次数
        self.max_retry_count = 3
        # 重试间隔时间（秒）
        self.retry_wait_time = 1
        # 打开网页后等待时长
        self.open_url_wait_time = 3
        # 加载页面的超时时间，以登录按钮出现为完成标志
        self.load_page_timeout = 60
        # 点击登录按钮后的超时时间，加载登录iframe，以其显示出来为完成标志
        self.load_login_iframe_timeout = 8
        # 登录的超时时间，从登录界面显示为开始，以用户完成登录为结束标志
        self.login_timeout = 600
        # 等待登录完成的超时时间，以活动结束的按钮弹出来标志
        self.login_finished_timeout = 60


class RetryConfig(ConfigInterface):
    def __init__(self):
        # 每次兑换请求之间的间隔时间（秒），避免请求过快而报错，目前测试1s正好不会报错~
        self.request_wait_time = 1
        # 当提示【"msg": "系统繁忙，请稍候再试。", "ret": "-9905"】时的最大重试次数
        self.max_retry_count = 3
        # 上述情况下的重试间隔时间（秒）
        self.retry_wait_time = 1


class XinYueConfig(ConfigInterface):
    def __init__(self):
        # 在每日几点后才尝试提交心悦的成就点任务，避免在没有上游戏时执行心悦成就点任务，导致高成就点的任务没法完成，只能完成低成就点的
        self.submit_task_after = 0


class FixedTeamConfig(ConfigInterface):
    reg_qq = r'\d+'

    def __init__(self):
        # 是否启用该固定队
        self.enable = False
        # 固定队伍id，仅用于本地区分用
        self.id = "1"
        # 固定队成员，必须是三个，则必须都配置在本地的账号列表中了，否则将报错，不生效
        self.members = ["小队第一个账号的QQ号", "小队第二个账号的QQ号", "小队第三个账号的QQ号"]

    def check(self) -> bool:
        if len(self.members) != 3:
            return False

        for qq in self.members:
            if re.fullmatch(self.reg_qq, qq) is None:
                return False

        return True


class CommonConfig(ConfigInterface):
    log_level_map = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL,
    }

    def __init__(self):
        # 测试用开关，将仅运行首个账号配置
        self._debug_run_first_only = False
        # 是否展示小助手的累积使用情况
        self._show_usage = False
        # 是否强制使用打包附带的便携版chrome
        self.force_use_portable_chrome = False
        # http(s)请求超时时间(秒)
        self.http_timeout = 10
        # 是否展示chrome的debug日志，如DevTools listening，Bluetooth等
        self._debug_show_chrome_logs = False
        # 自动登录模式是否不显示浏览器界面
        self.run_in_headless_mode = False
        # 日志等级, 级别从低到高依次为 "debug", "info", "warning", "error", "critical"
        self.log_level = "info"
        # 是否检查更新
        self.check_update_on_start = True
        self.readme_page = "https://github.com/fzls/djc_helper/blob/master/README.MD"
        self.changelog_page = "https://github.com/fzls/djc_helper/blob/master/CHANGELOG.MD"
        # 正式模式运行成功时是否弹出打赏图片
        self.show_support_pic = True
        # 自动赠送卡片的目标QQ数组，这些QQ必须是配置的账号之一，若配置则会在程序结束时尝试从其他小号赠送最需要的卡片给这些账号，若不配置则不启用。
        self.auto_send_card_target_qqs = []
        # 登录各个阶段的最大等待时间，单位秒（仅二维码登录和自动登录需要配置，数值越大容错性越好）
        self.login = LoginConfig()
        # 各种操作的通用重试配置
        self.retry = RetryConfig()
        # 心悦相关配置
        self.xinyue = XinYueConfig()
        # 固定队相关配置。用于本地三个号来组成一个固定队伍，完成心悦任务。
        self.fixed_teams = []  # type: List[FixedTeamConfig]
        # 赛利亚活动拜访目标QQ列表
        self.sailiyam_visit_target_qqs = []

    def auto_update_config(self, raw_config: dict):
        super().auto_update_config(raw_config)

        if 'fixed_teams' in raw_config:
            self.fixed_teams = []
            for cfg in raw_config["fixed_teams"]:
                ei = FixedTeamConfig()
                ei.auto_update_config(cfg)
                self.fixed_teams.append(ei)

        consoleHandler.setLevel(self.log_level_map[self.log_level])


class Config(ConfigInterface):
    def __init__(self):
        # 所有账号共用的配置
        self.common = CommonConfig()
        # 兑换道具信息
        self.account_configs = []  # type: List[AccountConfig]

    def auto_update_config(self, raw_config: dict):
        super().auto_update_config(raw_config)

        if 'account_configs' in raw_config:
            self.account_configs = []
            for cfg in raw_config["account_configs"]:
                ei = AccountConfig()
                ei.auto_update_config(cfg)
                self.account_configs.append(ei)

        if not self.check():
            logger.error("配置有误，请根据提示信息修改")
            exit(-1)

    def check(self) -> bool:
        name2index = {}
        for _idx, account in enumerate(self.account_configs):
            idx = _idx + 1

            # 检查是否填写名称
            if len(account.name) == 0:
                logger.error(color("fg_bold_red") + "第{}个账号未设置名称，请确保已填写对应账号配置的name".format(idx))
                return False

            # 检查名称是否重复
            if account.name in name2index:
                logger.error(color("fg_bold_red") + "第{}个账号的名称 {} 与第{}个账号的名称重复，请调整为不同的名字".format(idx, account.name, name2index[account.name]))
                return False
            name2index[account.name] = idx

            # 检查dnf助手的userId是否误填为了昵称
            dhi = account.dnf_helper_info
            if dhi.userId != "":
                try:
                    int(dhi.userId)
                except ValueError:
                    logger.error(color("fg_bold_red") + "第{}个账号配置的dnf助手信息的社区ID(userId)=[{}]似乎为昵称，请仔细检查是否与昵称(nickName)=[{}]的值填反了？id应该类似[504051073]，而昵称则形如[风之凌殇]".format(
                        idx, dhi.userId, dhi.nickName
                    ))
                    return False

        return True


g_config = Config()


# 读取程序config
def load_config(config_path="config.toml", local_config_path="config.toml.local"):
    global g_config
    # 首先尝试读取config.toml（受版本管理系统控制）
    try:
        raw_config = toml.load(config_path)
        g_config.auto_update_config(raw_config)
    except UnicodeDecodeError as error:
        logger.error(color("fg_bold_yellow") + "{}的编码格式有问题，应为utf-8，如果使用系统自带记事本的话，请下载vscode或notepad++等文本编辑器\n错误信息：{}\n".format(config_path, error))
        exit(0)
    except Exception as error:
        if encoding_error_str in str(error):
            logger.error(color("fg_bold_yellow") + "{}的编码格式有问题，应为utf-8，如果使用系统自带记事本的话，请下载vscode或notepad++等文本编辑器\n错误信息：{}\n".format(config_path, error))
            exit(0)

        logger.error(color("fg_bold_red") + "读取{}文件出错，是否直接在压缩包中打开了或者toml语法有问题？\n具体出错为：{}\n".format(config_path, error) +
                     color("fg_bold_yellow") + "若未完整解压，请先解压。否则请根据上面的英文报错信息，自行百度学习toml的基本语法，然后处理对应行的语法错误（看不懂的话自行用百度翻译或有道翻译）")
        exit(-1)

    # 然后尝试读取本地文件（不受版本管理系统控制）
    try:
        raw_config = toml.load(local_config_path)
        g_config.auto_update_config(raw_config)
    except Exception as e:
        pass


def config():
    return g_config


if __name__ == '__main__':
    load_config("config.toml", "config.toml.local")
    logger.info(config())
