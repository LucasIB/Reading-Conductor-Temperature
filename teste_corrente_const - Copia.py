#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
`  @@@@@@@@`-@@@@@@@@@@@@@@@@@@@  `
`  @@@@@@@     .@@@@@@@@@@@@@@@@  `
`  @@@@@:    `@@@:.   -@@@@@@@@@  `
`  @@@@:   .@@:`       .@@@@@@@@  `
`  @@@@  `@@-   `.@@@@@@@@@@@@@@  `
`  @@@. -@: .@@@@@- ``      .@@@  `
`  @@@ -@.:@@-              `@@@  `
`  @@@.@@@@@@@@@:-``@@@@@@. `@@@  `
`  @@@@@-    .@@@@@:`   .@@@@@@@  `
`  @@@@        @@@@@@@:`    .:@@  `
`  @@@@        @@@@@@@@@@`        `
`                                 `
Created on 06/07/2017
@author: lucas.balthazar
'''
#Import library
import time
import matplotlib.pyplot as plt        
from matplotlib import style
import numpy as np
import threading
import Agilent_34970A

#Connecting Data Acquisition 34970A
try:
    a = Agilent_34970A.SerialCom(6)
    a.Conectar()
except:
    raise TypeError("Oups! Connection Fail. Ask Lucas for Why")

# Modifying the plot style
style.use('fivethirtyeight')

class monitor(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self._stop()
   
    def read_temperature(self):
        # reading temperature
        _tmp = a.Enviar(':READ?')  # Faz a leitura de todas as entradas configuradas de PT100 e tensão de uma só vez. 
        time.sleep(1)
        _read = a.Ler(200).split(',')   
        temperature = np.asarray(_read, dtype=float)
        volt = temperature[0]
        current = volt*32
        temperature = np.append(temperature,current)
        return temperature

    def read_datetime(self):
        # reading datetime from system
        tmp = time.localtime()
        _datetime = time.strftime('%d/%m/%Y %H:%M:%S',tmp)
        return _datetime

    def monitoring_Temp_and_time(self, ntimes, interval):
        tmp = time.localtime()
        self._date = '{0:1d}-{1:1d}-{2:1d}'.format(tmp.tm_mday,tmp.tm_mon,tmp.tm_year)
        try:
            f = open('Monitoring_save_data ' + self._date+ '.dat', 'w')
            f.writelines('DateTime\t\tVolt(V)\t\t\tTemp1(ºC)\tCurrent(A)\n')
        except:
            return
        for i in range(ntimes):
            _datetime = self.read_datetime()
            _temperature = self.read_temperature()
            
            f.write(_datetime + '\t' + str(_temperature[0]) + '\t\t' + str(_temperature[1])+ '\t\t' + str(_temperature[2]))
            f.write('\n')    
            
            time.sleep(interval)
          
        f.close()
        self.animate()

    def animate(self):
        temp_arr = []
        try:
            graph_data = open('Monitoring_save_data ' + self._date+ '.dat','r')
        except:
            raise TypeError("Reading Fail")
        
        config = graph_data.read().split('\n')
        graph_data.close()

        for i in range(1, len(config)-1):
            config[i]=config[i].split('\t')
            temp = config[i][3].format("{0:.2f}")
            temp_arr.append(float(temp))
##        print(temp_arr)
        plt.plot(temp_arr)
        plt.grid(True)
        plt.ylabel('Temp 1 [°C]')
##        plt.ylim(22.000,23.000)
        plt.show()
        
     


