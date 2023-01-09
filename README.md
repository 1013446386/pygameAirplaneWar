# pygameAirplaneWar

练手项目: PyGame飞机大战

生成二进制文件: 

1.进入项目根目录 
2.执行pyinstaller main.spec



空格发射, esc/c/v/b暂停


打包命令（用上面的生成二进制就可以）


Windows:pyinstaller -i resources/icon/d5_64x64.ico --add-data resources:resources -Fw main.py

Mac:pyinstaller -i resources/icon/LOGO.icns --add-data resources:resources -Fw main.py