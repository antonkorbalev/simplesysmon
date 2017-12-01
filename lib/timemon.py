import threading
import time
import psutil
from conf import config as cfg
import datetime

mem_info = list()
disk_usage = list()

def timer_thread():
    while True:
        time.sleep(cfg.time_step)
        mi = psutil.virtual_memory()
        if mem_info.__len__() >= cfg.max_items_count:
            mem_info.pop(0)
        if disk_usage.__len__() >= cfg.max_items_count:
            disk_usage.pop(0)
        di = list()
        for dp in psutil.disk_partitions():
            try:
                du = psutil.disk_usage(dp.mountpoint)
            except:
                continue
            di.append(du.free / 1024 / 1024)
        mem_info.append([mi.available / 1024 / 1024])
        disk_usage.append(di)

def start():
    t = threading.Thread(target=timer_thread,
                         name="Monitor",
                         args=(),
                         daemon=True)
    t.start()

