#!/usr/bin/python3

import os
from subprocess import Popen, PIPE

import re
import time
import stat
import datetime


# Класс для выполнения консольных команд

class Command():

  # Запуск внешней программы
  def run(self, cmd):
    p=Popen(cmd, stdout=PIPE, shell=True)
    stdOutData, stdErrData = p.communicate()
    errCode=p.returncode

    outData=""
    errData=""

    if not stdOutData is None :
      outData=stdOutData.decode()

    if not stdErrData is None :
      errData=stdErrData.decode()

    # Убирается последний перенос строк, чтобы в конце небыло пустой строки
    outData=re.sub("\n$", '', outData)
    errData=re.sub("\n$", '', errData)

    return(outData, errData, errCode)


  # Запуск внешней команды, которая может зависнуть по I/O
  def runHard(self, cmd, waitTime):

    # Удаляется предыдущий исполнимый файл
    if os.path.exists('./run.sh'):
      os.remove('./run.sh')

    # Команды записываются в исполнимый файл
    fileDescriptor = open('./run.sh', 'w')
    fileDescriptor.write('#!/bin/sh'+"\n")
    fileDescriptor.write(cmd)
    fileDescriptor.close()

    os.chmod('./run.sh', stat.S_IRUSR | stat.S_IWUSR | stat.S_IEXEC)

    print( "Запускаются команды во внешнем процессе:\n" )
    print( cmd+"\n" )

    # Запускается выполнение команд
    errCode=os.system('./runHardProcess.sh '+str(waitTime))

    # Удаляются созданные исполнимые файлы
    if os.path.exists('./run.sh'):
      os.remove('./run.sh')
    if os.path.exists('./runHardProcess.sh'):
      os.remove('./runHardProcess.sh')

    return errCode

