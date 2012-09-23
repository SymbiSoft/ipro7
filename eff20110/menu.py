s.menu=[
(cn('测试'), s.inspect), 
(cn('文件'), (
  (cn('打开文件'), s.fetch_file), 
  (cn('打开历史'), s.fetch_history),
  (cn('新建文件'), s.build_window), 
  (cn('保存文件'), s.ask_save), 
  (cn('另存文件'), s.save_as_new), 
  (cn('全部保存'), s.save_all), 
  (cn('切换编码'), s.change_code), 
  (cn('存为模板'), s.save_as_mould), 
  (cn('文件详情'), s.file_details)
)),
(cn('编辑'), (
  (cn('查找文字'), s.seek), 
  (cn('查找下个'), s.seek_next), 
  (cn('高级查找'), s.senior_seek), 
  (cn('查找替换'), s.seek_replace), 
  (cn('插入模板'), s.insert_mould),
  (cn('清空内容'), s.clear_content),
  (cn('函数浏览'), s.read_funcs)
)),
(cn('跳转'), s.jump), 
(cn('窗口'), s.change_window), 
(cn('设置'), s.set), 
(cn('拓展'), s.execute_extend), 
(cn('运行'), s.run_script), 
(cn('解释'), s.shell), 
(cn('退出'), s.exit)]