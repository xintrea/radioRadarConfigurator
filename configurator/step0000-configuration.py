#!/usr/bin/python3

from libMain import *

def main():

    log.echo( "Выполняется скрипт: "+config.scriptFile )
    log.echo( "Версия: "+settings.version )
    log.echo( "Доменная роль пользователя: "+config.userDomainRole )
    log.echo( "Проект: "+config.projectName )
    log.echo( "Мандатная директория пользователя: "+config.mandatUserDir )

    displaySwitchOffBlocking()

    if config.userDomainRole=="teacher" and config.projectName=="radio" :
      teacherInRadio()

    if config.userDomainRole=="student" and config.projectName=="radio" :
      studentInRadio()

    if config.userDomainRole=="student" and config.projectName=="radar" :
      studentInRadar()

    log.echo( "Настройка успешно завершена" )


def teacherInRadio():
  log.echo( "Настройка окружения Учителя в конфигарции Радио" )

  log.echo( "Копирование ярлыков на рабочий стол" )
  fileNames=[ 'cam1.desktop',
              'cam2.desktop',
              'teacherRadio.desktop',
              'teacherRadar.desktop' ]
  for fileName in fileNames :
    shutil.copyfile( config.scriptDir+"/../files/desktop/"+fileName, 
                     config.mandatUserDir+"/Desktops/Desktop1/"+fileName )

  log.echo( "Копирование файлов VLC-потоков в каталог пользователя" )
  fileNames=[ 'cam1.xspf',
              'cam2.xspf']
  for fileName in fileNames :
    shutil.copyfile( config.scriptDir+"/../files/xspf/"+fileName, 
                     config.mandatUserDir+"/"+fileName )

  log.echo( "Копирование файла настройки VLC" )
  shutil.copyfile( config.scriptDir+"/../files/vlc/vlcrc", 
                   config.mandatUserDir+"/.config/vlc/vlcrc" )


def studentInRadio():
  log.echo( "Настрока окружения Ученика в конфигурации Радио" )

  # Отключение всего ненужного (только для Учеников)
  removeUnnecessary()

  log.echo( "Копирование ярлыков на рабочий стол" )
  fileNames=[ 'exit.desktop',
              'studentRadio.desktop' ]
  for fileName in fileNames :
    copyDesktopIcon( config.scriptDir+"/../files/desktop/"+fileName, 
                     config.mandatUserDir+"/Desktops/Desktop1/"+fileName,
                     True )

  log.echo( "Добавление ярлыка Радио в автозапуск" )
  fileName='studentRadio.desktop'
  shutil.copyfile( config.scriptDir+"/../files/desktop/"+fileName, 
                   config.mandatUserDir+"/.config/autostart/"+fileName )

  # Для компьютера, на котором должен быть настроена связка Радио-Радар
  if( settings.radioRadarKtgIp in helper.getIpAddresses() ) :
    # В автозапуске не должно быть ярлыка Радио
    fileName='studentRadio.desktop'
    command.run("rm -f "+config.mandatUserDir+"/.config/autostart/"+fileName)

    # Добавление на рабочий стол ярлыка Радио-Радар
    fileName='radioRadarUdoKtg.desktop'
    copyDesktopIcon( config.scriptDir+"/../files/desktop/"+fileName,
                     config.mandatUserDir+"/Desktops/Desktop1/"+fileName,
                     True )


def studentInRadar():
  log.echo( "Настрока окружения Ученика в конфигурации Радар" )

  # Отключение всего ненужного (только для Учеников)
  removeUnnecessary()

  log.echo( "Копирование ярлыков на рабочий стол" )
  fileNames=[ 'exit.desktop',
              'studentRadar.desktop' ]
  for fileName in fileNames :
    copyDesktopIcon( config.scriptDir+"/../files/desktop/"+fileName, 
                     config.mandatUserDir+"/Desktops/Desktop1/"+fileName,
                     True )

  log.echo( "Добавление ярлыка Радар в автозапуск" )
  fileName='studentRadar.desktop'
  shutil.copyfile( config.scriptDir+"/../files/desktop/"+fileName, 
                   config.mandatUserDir+"/.config/autostart/"+fileName )


# Отключение всего ненужного для Ученика
def removeUnnecessary() :

  desktopsDir=config.mandatUserDir+"/Desktops"
  flyDir=config.mandatUserDir+"/.fly"
  filesDir=config.scriptDir+"/../files"


  log.echo( "Удаление всех ярлыков с 4-х рабочих столов" )
  dirNames=[ 'Desktop1', 
             'Desktop2', 
             'Desktop3', 
             'Desktop4' ]
  for dirName in dirNames :
    command.run("cd "+desktopsDir+"/"+dirName+" ; rm -f *")


  log.echo( "Настройка локали и отключение горячих клавиш" )
  fileNames=[ 'ru_RU.UTF-8.fly-wmrc',
              'ru_RU.UTF-8.miscrc',
              'keyshortcutrc',
              'sessrc' ]
  for fileName in fileNames :
    shutil.copyfile( filesDir+"/fly/"+fileName, flyDir+"/"+fileName )


  log.echo( "Отключение панели задач" )
  shutil.copyfile( filesDir+"/theme/current.themerc", 
                   flyDir+"/theme/current.themerc" )


def copyDesktopIcon(fromFileName, toFileName, readOnly=False) :

  # Копирование
  shutil.copyfile( fromFileName, toFileName )

  # Установка прав только на чтение, если это необходимо
  if(readOnly) :
    # command.run("chown root:root "+toFileName) # Невозможно сделать chown для доменного пользователя
    command.run("chmod 444 "+toFileName)



def displaySwitchOffBlocking() :
  command.run("xset -dpms")
  command.run("xset s off")

  # Настройка файла /.config/powermanagementprofilesrc в каталоге пользователя
  # В нем надо удалить секцию [AC][DPMSControl]
  # Это делается через sed, который умеет работать с диапазоном строк, заданных через запятую
  # То есть, перед командой (символом действия) задается два регвыра, разделенных запятой.
  # Первый регвыр - это начало области, второй регвыр - это место завершения области,
  # в которой будут производиться действия.
  # Удаление происходит через команду s, после которой снова указывается два регвыра,
  # что на что меняется, в данном случае меняется все, что находится в выбранном диапазоне
  # на пустую строку
  fileName=config.mandatUserDir+"/.config/powermanagementprofilesrc"
  sedCommand="sed -i '/\[AC\]\[DPMSControl\]/,/^[^\[]/s/.*//' ~/.config/powermanagementprofilesrc "+fileName
  command.run(sedCommand)


# Конструкция чтобы работала функция main()
if __name__ == '__main__':
  main()
