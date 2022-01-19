#!/usr/bin/python3

import sys
import os

from libMain import *


# Класс начальных проверок

class FirstChecking():

  def __init__(self):

    if helper.getUserDomainRole()=="" :
      log.echo( "Error! Пользователь "+helper.getUserName()+" не входит ни в доменную группу Учителя, ни в доменную группу Ученики" )
      log.echo( "Выполнение настройки окружения пользователя невозможно" )
      sys.exit(1)

    if helper.getWhoami()!="root" :
      log.echo( "Error! Скрипт может выполняться только от пользователя root," )
      log.echo( "с установленной переменной USER=<имя доменного пользователя>" )
      log.echo( "Для пользователя "+helper.getWhoami()+ " выполнение скрипта невозможно" )
      sys.exit(1)

    if helper.getWhoami()=="root" and helper.getUserName()=="root" :
      log.echo( "Error! Скрипт не должен выполняться от пользователя root с переменной USER=root" )
      sys.exit(1)

    if helper.getDistId()!="astra16" :
      log.echo( "Error! Автоматическая настройка возможна только для Astra Linux 1.6 Smolensk" )
      sys.exit(1)

    if helper.getProjectName()=="" :
      log.echo( "Error! Невозможно определить конфигурацию сервера Radio или Radar по IP-адресу" )
      sys.exit(1)

    if not os.path.exists( config.mandatUserDir ) :
      log.echo( "Error! Мандатный каталог доменного пользователя не найден: "+config.mandatUserDir )
      sys.exit(1)

    if not os.path.exists( config.mandatUserDir+"/Desktops" ) :
      log.echo( "Error! Мандатный каталог рабочих столов не найден: "+config.mandatUserDir+"/Desktops" )
      sys.exit(1)

    if not os.path.exists( config.mandatUserDir+"/.fly" ) :
      log.echo( "Error! Мандатный каталог настройки FLY не найден: "+config.mandatUserDir+"/.fly" )
      sys.exit(1)
