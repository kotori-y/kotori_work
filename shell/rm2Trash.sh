# .bashrc

# via: https://www.cnblogs.com/paul8339/p/9722756.html

### 重定义rm命令 ### 
 
# 定义回收站目录 
trash_path='~/.trash' 
 
# 判断 $trash_path 定义的文件是否存在，如果不存在，那么就创建 $trash_path. 
if [ ! -d $trash_path ]; then 
 mkdir -p $trash_path 
fi 
 
# 定义别名：使用 rm 就调用 trash 
alias rm=trash 
 
# 使用 rl 就调用 'ls ~/.trash' 
# 如果更改上面的回收站目录这里的目录也需要修改 
alias rl='ls ~/.trash' 
 
# 使用 unrm 就调用 restorefile，需要在删除目录的父目录下执行 
alias unrm=restorefile 
 
# 使用 rmtrash 就调用 claearteash 
alias rmtrash=cleartrash 
 
# 恢复文件的函数 
restorefile() 
{ 
 mv -i ~/.trash/$@ ./ 
} 
 
# 删除文件的函数 
trash() 
{ 
 mv $@ ~/.trash/ 
} 
 
# 清空回收站的函数 
cleartrash() 
{ 
 read -p "确定要清空回收站吗?[y/n]" confirm 
 [ $confirm == 'y' ] || [ $confirm == 'Y' ] && /bin/rm -rf ~/.trash/* 
}