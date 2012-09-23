import sys,e32
disk=sys.argv[0][0]
sys.path.append(disk+":\\resource\\")
cn = lambda x: x.decode('u8')
a=None
try:
  a=sys.argv[1]
  import argv
  argv.set(a)
  e32.start_exe(disk+':\\sys\\bin\\iPro7_0xeff20110.exe', '')
  e32.ao_sleep(2)
  import appuifw
  appuifw.app.set_exit()
except:
  import appuifw
  if a!=None:
    appuifw.note(cn("打开失败"))
  else:
    appuifw.app.body=m=appuifw.Text()
    m.set(cn("               iPro7关联\n【作者】zl@sun\n【使用方法】打开x-plore，依次按菜单—工具—关联程序—菜单—新建—填入py(支持其它格式)—再选择iPro7关联\n\n这样设置后你在x-plore点后缀为py的文件时会自动用iPro7打开文件\n使用时请先退出本程序\n"))