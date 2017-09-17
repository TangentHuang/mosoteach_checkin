# -*- coding: utf-8 -*-

import subprocess
import os
import logging


def get_signature(type, datestr):
    cmd = r'java -cp {} com.Ak {} {}'.format('java_code', type, datestr)
    logging.debug(cmd)

    rst = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    rst = rst.communicate()[0].decode('ASCII')
    if os.linesep == '\n':                      # linux
        return rst[:-1]
    else:                                       # windows
        return rst[:-2]


def get_current_open_signature(date, config):
    """
    >>> from config import configs
    >>> config = configs["xwytest"]
    >>> get_current_open_signature("Sat, 16 Sep 2017 06:17:49 GMT+00:00", config)
    'ca98544f9582deb29b42a00ca738ab9fbc0adaa1'
    """
    datestr = ' '.join(map(lambda x: '"{}"'.format(x), [config.USER_ID, date, config.ACCESS_SECRET, config.CLAZZ_COURSE_ID]))

    return get_signature("current_open", datestr)


def get_checkin_signature(date, config):
    datestr = ' '.join(map(lambda x: '"{}"'.format(x), [config.USER_ID, date, config.ACCESS_SECRET]))
    return get_signature("checkin", datestr)


if __name__ == '__main__':
    from config import configs
    logging.basicConfig(level=logging.DEBUG)
    config = configs["xwytest"]
    logging.info(get_current_open_signature("Sat, 16 Sep 2017 06:17:49 GMT+00:00", config))
