import matplotlib
matplotlib.use('agg')
import psutil, datetime
import mpld3
from conf import config as cfg
import platform
from matplotlib import pyplot as plt
import numpy
from lib import timemon
from operator import itemgetter

def get_panel(header, text):
    return str.format("<div class=\"container\">" \
            "<H2> {0} </H2>" \
            "<div class=\"panel panel-default\">" \
            "<div class=\"panel-body\">{1}</div>" \
            "</div>" \
            "</div>", header, text)


def get_contents(graph, text):
    return str.format("<TABLE>"
                      "<TR>"
                      "<TD> {0} </TD>" 
                      "<TD>" 
                      "<DIV class\"container\"> {1} </DIV>" 
                      " </TD>" 
                      "</TR>" 
                      "</TABLE>",
                      graph,
                      text)


def get_disks_usage():
    return_text = ""
    num = 0
    for dp in psutil.disk_partitions():
        fig = plt.figure(figsize=(2 * cfg.fig_hw, cfg.fig_hw))
        plt.subplot(121)
        try:
            di = psutil.disk_usage(dp.mountpoint)
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
        html_graph = mpld3.fig_to_html(fig)
        text = str.format("<div> "
                          "<p class=\"text-info\"> Free memory: {0} MB </p>"
                          "<p class=\"text-info\"> Used memory: {1} MB </p>"
                          "</div>",
                          di.free / 1024 / 1024,
                          di.used / 1024 / 1024)
        contents = get_contents(html_graph, text)
        return_text = return_text + get_panel(str.format("Disk {0} info", dp.mountpoint), contents)
        num = num + 1
    return return_text

def get_mem_info():
    fig = plt.figure(figsize=(2 * cfg.fig_hw,cfg.fig_hw))
    plt.subplot(121)
    mem = psutil.virtual_memory()
    labels = ['Available', 'Used', 'Free']
    fracs = [mem.available, mem.used, mem.free]
    text = str.format("<div> "
                      "<p class=\"text-primary\"> Total memory: {0} MB </p>"
                      "<p class=\"text-info\"> Avaliable memory: {1} MB </p>"
                      "<p class=\"text-info\"> Used memory: {2} MB </p>"
                      "<p class=\"text-info\"> Free memory: {3} MB </p>"
                      "</div>",
                      mem.total / 1024 / 1024,
                      mem.available / 1024 / 1024,
                      mem.used / 1024 / 1024,
                      mem.free / 1024 / 1024)
    if psutil.LINUX:
        labels = numpy.hstack((labels, ['Active', 'Inactive', 'Cached', 'Buffers' , 'Shared']))
        fracs = numpy.hstack((fracs, [mem.active, mem.inactive, mem.cached, mem.buffers, mem.shared]))
        text = text + str.format(
                      "<div>"
                      "<p class=\"text-info\"> Active memory: {0} MB </p>"
                      "<p class=\"text-info\"> Inactive memory: {1} MB </p>"
                      "<p class=\"text-info\"> Cached memory: {2} MB </p>"
                      "<p class=\"text-info\"> Buffers : {3} MB </p>"
                      "<p class=\"text-info\"> Shared: {4} MB </p>"
                      "</div>",
                      mem.active / 1024 / 1024,
                      mem.inactive / 1024 / 1024,
                      mem.cached / 1024 / 1024,
                      mem.buffers / 1024 / 1024,
                      mem.shared / 1024 / 1024)
    plt.pie(fracs, labels=labels, shadow=True, autopct='%1.1f%%')
    plt.subplot(122)
    plt.plot(timemon.mem_info)
    plt.ylabel('MBs')
    plt.xlabel(str.format('Interval {0} s', cfg.time_step))
    plt.title('Avaliable memory')
    plt.tight_layout()
    html_graph = mpld3.fig_to_html(fig)
    contents = get_contents(html_graph, text)
    return get_panel("Memory info", contents)


def get_general_info():
    bi = datetime.datetime.fromtimestamp(psutil.boot_time())
    bd = (datetime.datetime.now() - bi).days
    return "<div class=\"container\">" \
           "<H1> Server information </H1>" \
           + str.format("<H3><span class=\"label label-success\"> "
                        "Active since {0} ({1} days) "
                        "</span></H3>",
                        bi.strftime("%d %B %Y %H:%M:%S"),
                        bd) \
            + str.format("<p class=\"text-info\">"
                        "{0} {1} {2}" 
                        "</p>" 
                        "</div>",
                        platform.system(),
                         platform.release(),
                        platform.version(),
                        bd)