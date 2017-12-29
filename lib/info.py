import matplotlib
matplotlib.use('agg')
import psutil, datetime
import mpld3
from jinja2 import Markup
from conf import config as cfg
import platform
from matplotlib import pyplot as plt
import numpy
from lib import timemon
from operator import itemgetter

def get_blocks():
    blocks = list()
    get_mem_info(blocks)
    get_disks_usage(blocks)
    return blocks

def get_mem_info(blocks):
    fig = plt.figure(figsize=(2 * cfg.fig_hw, cfg.fig_hw))
    plt.subplot(121)
    mem = psutil.virtual_memory()
    labels = ['Available', 'Used', 'Free']
    fracs = [mem.available, mem.used, mem.free]
    lines = list()
    lines.append(str.format('Avaliable memory: {0} MB',mem.available))
    lines.append(str.format('Used memory: {0} MB', mem.used))
    lines.append( str.format('Free memory: {0} MB', mem.free))
    if psutil.LINUX:
        labels = numpy.hstack((labels, ['Active', 'Inactive', 'Cached', 'Buffers', 'Shared']))
        fracs = numpy.hstack((fracs, [mem.active, mem.inactive, mem.cached, mem.buffers, mem.shared]))
        lines.append(str.format('Active memory: {0} MB', mem.active))
        lines.append(str.format('Inactive memory: {0} MB', mem.inactive))
        lines.append(str.format('Cached memory: {0} MB', mem.cached))
        lines.append(str.format('Buffers memory: {0} MB', mem.buffers))
        lines.append(str.format('Shared memory: {0} MB', mem.shared))
    plt.pie(fracs, labels=labels, shadow=True, autopct='%1.1f%%')
    plt.subplot(122)
    plt.plot(timemon.mem_info)
    plt.ylabel('MBs')
    plt.xlabel(str.format('Interval {0} s', cfg.time_step))
    plt.title('Avaliable memory')
    plt.tight_layout()
    graph = mpld3.fig_to_html(fig)
    blocks.append({
            'title': 'Memory info',
            'graph': Markup(graph),
            'data':
                {
                    'primary' : str.format("Total memory: {0} MB", mem.total / 1024 / 1024),
                    'lines' : lines
                }
        })
    print( blocks)

def get_disks_usage(blocks):
    num = 0
    for dp in psutil.disk_partitions():
        fig = plt.figure(figsize=(2 * cfg.fig_hw, cfg.fig_hw))
        plt.subplot(121)
        try:
            di = psutil.disk_usage(dp.mountpoint)
        # gets error on Windows, just continue anyway
        except:
            continue
        labels = ['Free', 'Used', ]
        fracs = [di.free, di.used]
        plt.pie(fracs, labels=labels, shadow=True, autopct='%1.1f%%')
        plt.subplot(122)
        plt.plot(list(map(itemgetter(num), timemon.disk_usage)))
        plt.ylabel('MBs')
        plt.xlabel(str.format('Interval {0} s', cfg.time_step))
        plt.title('Disk available space')
        plt.tight_layout()
        graph = mpld3.fig_to_html(fig)
        blocks.append({
            'title': str.format('Disk {0} info', dp.mountpoint),
            'graph': Markup(graph),
            'data':
                {
                    'primary': '',
                    'lines': [ str.format('Free memory: {0} MB', di.free / 1024 / 1024),
                               str.format('Used memory: {0} MB', di.used / 1024 / 1024) ]
                }
        })
        num = num + 1