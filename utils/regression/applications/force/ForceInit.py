#
# Copyright (C) [2020] Futurewei Technologies, Inc.
#
# FORCE-RISCV is licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR
# FIT FOR A PARTICULAR PURPOSE.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from classes.ApplicationOption import AppCmdLineOption, AppPathCmdLineOption, ParameterProcessor, CommandLineOption
from common.path_utils import PathUtils
from common.version_ctrl_utils import VersionCtrlUtils
from common.msg_utils import Msg
from common.sys_utils import SysUtils

## Define additional FORCE specific command line parameters
#
class ForceCmdLineOptions(object):

    cGroupName = "FORCE related options"
    cGroupDescription = "Useful FORCE options to control FORCE usage"

    #                               "number of value arguments"
    #                         "option name"               | "additional arguments"
    #                               |    "default value"  |    |   "help text"
    #                               |           |         |    |       |
    cOptions = [AppPathCmdLineOption('path',  "../../bin/force", 1, None, "- Path to FORCE binary", None, "FORCE_PATH")]

## Used to process application specific parameters
#
class ForceParametersProcessor(ParameterProcessor):

    def __init__(self, aCmdLineOptions):
        super().__init__(ForceCmdLineOptions.cOptions, aCmdLineOptions)

        force_path = self.mAppParameters.parameter('path')
        force_bin_dir, _ = PathUtils.split_path(force_path)
        force_dir = PathUtils.real_path(PathUtils.include_trailing_path_delimiter(force_bin_dir) + '../')

        if not PathUtils.check_exe(force_path):
            raise Exception(force_path + " does not exist or is not executable, confirm valid exe")

        #determine svn revision information and store as a parameter
        version_info = VersionCtrlUtils.get_svn_revision(force_dir)
        if version_info[1] is not None:
            Msg.info("Failed to determine Force svn version: " + version_info[1])
            self.mAppParameters.setParameter("version", -1)
        else:
            self.mAppParameters.setParameter("version", version_info[0])
        self.mAppParameters.setParameter("version_dir", force_dir)

## Process force control data
#
def processForceControlData(aControlData, aAppParameters):
    if aAppParameters is None: return # TODO Temporary, to avoid failing in forrest run, to remove.

    key = 'path'
    if aAppParameters.parameter(key):
        aControlData[key] = aAppParameters.parameter(key)

