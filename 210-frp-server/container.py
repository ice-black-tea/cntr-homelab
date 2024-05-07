#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author  : Hu Ji
@file    : deploy.py 
@time    : 2023/05/21
@site    :  
@software: PyCharm 

              ,----------------,              ,---------,
         ,-----------------------,          ,"        ,"|
       ,"                      ,"|        ,"        ,"  |
      +-----------------------+  |      ,"        ,"    |
      |  .-----------------.  |  |     +---------+      |
      |  |                 |  |  |     | -==----'|      |
      |  | $ sudo rm -rf / |  |  |     |         |      |
      |  |                 |  |  |/----|`---=    |      |
      |  |                 |  |  |   ,/|==== ooo |      ;
      |  |                 |  |  |  // |(((( [33]|    ,"
      |  `-----------------'  |," .;'| |((((     |  ,"
      +-----------------------+  ;;  | |         |,"
         /_)______________(_/  //'   | +---------+
    ___________________________/___  `,
   /  oooooooooooooooo  .o.  oooo /,   `,"-----------
  / ==ooooooooooooooo==.o.  ooo= //   ,``--{)B     ,"
 /_==__==========__==_ooo__ooo=_/'   /___________,"
"""
import os

from linktools import Config, utils
from linktools.container import BaseContainer
from linktools.decorator import cached_property


class Container(BaseContainer):

    @cached_property
    def configs(self):
        return dict(
            FRPS_TAG="latest",
            FRPS_BIND_PORT=Config.Prompt(default=7000, cached=True, type=int),
            FRPS_BIND_TOKEN=Config.Prompt(default=utils.make_uuid()[:12], cached=True),
            FRPS_VHOST_HTTP_PORT=Config.Prompt(default=80, cached=True, type=int),
            FRPS_VHOST_HTTPS_PORT=Config.Prompt(default=443, cached=True, type=int),
        )

    def on_starting(self):
        self.render_template(
            os.path.join(self.root_path, "frps.ini"),
            self.get_app_path("frps.ini", create_parent=True),
        )
        self.manager.change_owner(
            self.get_app_path(),
            self.manager.user,
        )
