#!/usr/bin/python3

import sys

from libMain import *


# Класс с различными вспомогательными методами

class Helper():

  # Получение доменной роли текущего пользователя
  def getUserDomainRole(self):
    groups=command.run("id -Gn $USER")[0]

    if settings.teacherDomainGroupName in groups:
      return "teacher"

    if settings.studentDomainGroupName in groups:
      return "student"

    return ""


  # Получение имени текущего настраиваемого пользователя из переменной окружения USER,
  # оно может отличаться от того пользователя, под которым происходит работа (whoami)
  def getUserName(self):
    userName=command.run("echo $USER")[0]
    return userName


  # Получение реального имени пользователя через команду whoami
  def getWhoami(self):
    userName=command.run("whoami")[0]
    return userName


  # Получение идентификатора дистрибутива
  def getDistId(self):
    issue=command.run("cat /etc/issue.net")[0]

    if issue=="Astra Linux SE 1.3 (smolensk)" :
      return "astra13"

    if issue=="Astra Linux SE 1.6 (smolensk)" :
      return "astra16"

    return ""


  # Получение наименования проекта - radio или radar
  def getProjectName(self):

    # Получение списка всех IP-адресов, принадлежащих данному компьютеру
    # Это строка из IP-адресов, разделенных пробелами
    ipAddresses=command.run("ip addr | grep -P '^\s*inet' | grep -P -o 'inet\s+\d+.\d+.\d+.\d+' | grep -P -o '\d+.*' | xargs")[0]

    # Создается массив масок IP-адресов, где октеты с 1 по 3 остаются прежними, а октет 4 заменяется на 0
    maskIpAddresses=[]
    for text in ipAddresses.split() :
      chunk=text.strip().split(".")
      
      if(len(chunk)!=4) :
        log.echo("Error! Incorrect IP address for detect project name: "+maskIpAddress)
        return ""

      maskIp=chunk[0]+"."+chunk[1]+"."+chunk[2]+".0"
      maskIpAddresses.append( maskIp )

    if settings.radioDomainIpMask in maskIpAddresses :
      return "radio"

    if settings.radarDomainIpMask in maskIpAddresses :
      return "radar"

    return ""


  # Получение списка IP-адресов хоста
  def getIpAddresses(self):

    # Получение списка всех IP-адресов, принадлежащих данному компьютеру
    # Это строка из IP-адресов, разделенных пробелами
    ipAddresses=command.run("ip addr | grep -P '^\s*inet' | grep -P -o 'inet\s+\d+.\d+.\d+.\d+' | grep -P -o '\d+.*' | xargs")[0]

    return ipAddresses.split()
