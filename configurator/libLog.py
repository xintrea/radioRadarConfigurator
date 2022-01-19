#!/usr/bin/python3

import sys
import os
import time

from libMain import *


# Класс, который пишет сообщения одновременно в консоль и в лог-файл

class Log():

  def __init__(self):
    self.text=""
    self.fileName=settings.logFile

    self.verificationFileAndPermission()

    self.echo( "===== Start logging at "+time.strftime("%d.%m.%Y %H:%M:%S)")+" v."+settings.version+" =====" )


  def verificationFileAndPermission(self):

    # Создание файла если его еще нет
    f=open(self.fileName, 'at')
    f.close()

    # Установка файлу максимальных прав, чтобы при смене пользователя файл все равно мог изменяться
    os.chmod(self.fileName, 0o777);


  def echo(self, inputText):

    print( inputText+"\n" )

    f = open(self.fileName, 'at')
    f.write(inputText+"\n")
    f.close()

    self.text += inputText+"\n"


  def getAll(self):
    return self.text

