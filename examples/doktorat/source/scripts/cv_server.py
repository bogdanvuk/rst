'''
Created on Feb 19, 2015

@author: bvukobratovic
'''

import serial
import re
import json
from collections import OrderedDict
import time
import subprocess
import threading

def eval_arg_parse(*args, **kwargs):
    return args, kwargs

class SerialCmd():
    def __init__(self, fname):
        self.fname = fname

    def __enter__(self):
        try:
            with open(self.fname) as data_file:
                self.res = json.load(data_file)
        except FileNotFoundError:
            self.res = {}

        self.t = threading.Timer(10, self.dump_res)
        self.t.start()
        self.dump_res()

        return self

    def __exit__(self, type, value, traceback):
        self.dump_res()
        self.t.cancel()

    def dump_res(self):
        with open(self.fname, 'w') as outfile:
            json.dump(self.res, outfile, indent = 4)
        
        # try:
        #     self.t.cancel()
        # except:
        #     pass
        
        
        #self.t.start()

    def cmd_efti_config(self, *args, **kwargs):
        self.res['efti_config'] = {}
        for k in kwargs:
            self.res['efti_config'][k] = float(kwargs[k])

#         self.dump_res()

    def cmd_dataset(self, *args, **kwargs):
        name = kwargs['name']

        if 'dataset' not in self.res:
            self.res['dataset'] = {}

        dataset = self.res['dataset']

        dataset[name] = {}

        for k in kwargs:
            if k != 'name':
                dataset[name][k] = float(kwargs[k])

#         self.dump_res()

    def add_run_to_res(self, run_hier=[], res={}, run_data={}):
        if run_hier:
            if run_hier[0] not in res:
                res[run_hier[0]] = {}

            self.add_run_to_res(run_hier[1:], res[run_hier[0]], run_data)

        else:
            for k,v in run_data.items():
                res[k] = float(v)

    def store_res(self, res_name, **kwargs):
        if res_name not in self.res:
            self.res[res_name] = []

#         run_data = {}

#         for k in kwargs:
# #            if k not in ('dataset'):
#             try:
#                 run_data[k] = float(kwargs[k])
#             except ValueError:
#                 run_data[k] = kwargs[k]


        self.res[res_name].append(kwargs)

#         self.dump_res()

    def cmd_cv_hw_run(self, *args, **kwargs):
        self.store_res("hw_run", **kwargs)

    def cmd_cv_arm_run(self, *args, **kwargs):
        self.store_res("arm_run", **kwargs)

    def cmd_cv_pc_run(self, *args, **kwargs):
        self.store_res("pc_run", **kwargs)

    def cmd_decode(self, line):
        try:
            if line[0] == '$':
                result = re.search('\$(.*):', line)
                cmd = result.group(1)
                result = re.search(':(.*)\n', line)
                args, kwargs = eval('eval_arg_parse(' + result.group(1) + ')')
                getattr(self, 'cmd_' + cmd)(*args, **kwargs)
        except Exception as e:
            print(str(e))
            print("Error decoding the command!")

def start_server(port, baud=115200):
    ser_cmd = SerialCmd("cv_{0}_arm.js".format(time.strftime("%Y%m%d_%H%M%S")));
    ser = serial.Serial(port, baud, timeout=1)
    ser.flush()
    while (1):
        line = ser.readline()   # read a '\n' terminated line
        if line:
            print(time.strftime("%H:%M:%S %d.%m.%Y. - "), line.decode(), end='');
            cmd_decode(ser_cmd, line.decode())

    ser.close()
    ser_cmd.dump_res()

def file_decode(fname):
    ser_cmd = SerialCmd("cv_{0}_arm.js".format(time.strftime("%Y%m%d_%H%M%S")));

    with open(fname) as openfileobject:
        for line in openfileobject:
            if line:
                cmd_decode(ser_cmd, line)

    ser_cmd.dump_res()

if __name__ == '__main__':
#     ser_cmd = SerialCmd("cross1.js");
#     cmd_decode(ser_cmd, "$efti_config:max_iterations=50000,topology_mutation_rate=3.000000e-03,weights_mutation_rate=2.000000e-02,search_probability=1.000000e-03,search_probability_raise_due_to_stagnation_step=1.000000e-03,weight_mutation_rate_raise_due_to_stagnation_step=1.000000e-04,return_to_best_prob_iteration_increment=5.000000e-11,complexity_weight=5.000000e-02\r\n")
#     subprocess.call("xsdb elf_download_2.tcl", shell=True)
    start_server(port='/dev/ttyACM0')
#     file_decode('/home/bvukobratovic/personal/doktorat/results/efti_pc_cw.log')

#     cmd_decode(None, "$cv_hw_run:dataset='ausc',run=0,id=3,seed=28,train_cnt=552,test_cnt=138,fitness=0.895860,accuracy=0.833333,leaves=3,depth=[1, 1],nonleaves=2,timing=3.609133,fitness_calc_cycle_timing=5.454000e-06\n")
