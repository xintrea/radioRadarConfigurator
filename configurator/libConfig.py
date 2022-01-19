#!/usr/bin/python3

import sys

from libMain import *


# Класс настроек, определяемых в момент старта программы

class Config():

  def __init__(self):

    # Полный путь до скрипта, который был запущен на выполнение
    self.scriptFile=command.run("readlink -e "+sys.argv[0])[0]

    # Каталог, в котором лежит скрипт, который был запущен на выполнение
    self.scriptDir=command.run("dirname "+self.scriptFile)[0]

    # Имя пользователя, окружение которого необходимо настроить
    self.userName=helper.getUserName()

    # Доменная роль пользователя teacher или student
    self.userDomainRole=helper.getUserDomainRole()

    # Наименование проекта - radio или radar
    self.projectName=helper.getProjectName()

    # Мандатная директория пользователя
    self.mandatUserDir="/"+settings.domainUsersDir+"/"+self.userName+"/"+settings.mandatDir

