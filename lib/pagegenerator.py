from conf import config as cfg
from lib import info as i

def get_index():
    return get_header() + \
           get_body() + \
           get_footer()


def get_header():
    return "<html>" \
           "<head>" \
           "<link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css\">" \
           "<title> Server monitor v." + str(cfg.version) + "</title>" \
           "</head>"


def get_body():
    return "<body>" \
           + i.get_general_info() \
           + i.get_mem_info() \
           + i.get_disks_usage() \
           + "</body>"


def get_footer():
    return "</html>"
