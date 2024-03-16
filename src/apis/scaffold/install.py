# -*- coding: utf-8 -*-
# Time       : 2022/2/4 12:17
# Author     : QIN2DIM
# Github     : https://github.com/QIN2DIM
# Description:
from typing import Optional, Any

from webdriver_manager.chrome import ChromeDriverManager

from services.settings import logger
from services.utils import CoroutineSpeedup

_HOOK_CDN_PREFIX = "https://curly-shape-d178.qinse.workers.dev/"


def _download_driver(*args, **kwargs):
    """
    下载浏览器驱动。

    :return:
    """
    if not args:
        pass
    version = kwargs.get("version", "latest")

    logger.debug("适配 ChromeDriver...")
    # 在这里指定特定的 ChromeDriver 版本
    driver_path = ChromeDriverManager(version="114.0.5735.90").install()
    # 之后你可能需要将 driver_path 返回出来，以便后续使用
    return driver_path


class PerformanceReleaser(CoroutineSpeedup):
    def __init__(self, docker: Any, power: Optional[int] = None):
        super(PerformanceReleaser, self).__init__(docker=docker, power=power)

    def control_driver(self, task: Any, *args, **kwargs):
        try:
            task(*args, **kwargs)
        except Exception as e:  # noqa
            logger.exception(e)


def run(cdn: Optional[bool] = False):
    """
    下载项目运行所需的各项依赖。

    :return:
    """
    logger.debug("正在下载系统依赖")
    docker = [_download_driver]

    booster = PerformanceReleaser(docker=docker, power=2)
    booster.go(cdn=cdn)

    logger.success("系统依赖下载完毕")
