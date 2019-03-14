#  Copyright 2018 U.C. Berkeley RISE Lab
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from misc_pb2 import *


# create generic error response
error = GenericResponse()
error.success = False

# create generic OK response
ok = GenericResponse
ok.success= True
OK_RESP = ok.SerializeToString()

# shared constants
FUNCOBJ = 'funcs/index-allfuncs'
FUNC_PREFIX = 'funcs/'
BIND_ADDR_TEMPLATE = 'tcp://*:%d'

PIN_PORT = 5000
UNPIN_PORT = 5001
FUNC_EXEC_PORT = 5002
DAG_QUEUE_PORT = 5003
DAG_EXEC_PORT = 5004

def _get_func_kvs_name(fname):
    return FUNC_PREFIX + fname


def _retrieve_function(name, kvs):
    kvs_name = _get_func_kvs_name(name)
    latt = kvs.get(kvs_name)

    if latt:
        return function_ser.load(latt.value)
    else:
        return None


def _push_status(schedulers, status):
    msg = status.SerializeToString()

    # tell all the schedulers your new status
    for sched in schedulers:
        sckt = ctx.socket(zmq.PUSH)
        sckt.connect(_get_status_ip(sched))
        sckt.send_string(msg)
