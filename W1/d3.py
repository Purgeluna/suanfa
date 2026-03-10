# linux 操作
cd  # 切换目录
pwd  # 显示当前目录
mkdir  # 创建目录
rm # 删除文件或目录        rm -rf  # 强制删除目录
cp a.txt + 路径  # 复制文件
mv  a.txt + 路径  # 移动文件
ls # 列出目录下的文件和目录
cat a.txt  # 显示文件内容
less a.txt  # 分页显示文件内容

# 进程管理
ps -ef # 显示所有进程
top  # 实时显示系统资源使用情况和进程信息
kill 进程ID  # 终止指定进程
kill -9 进程ID  # 强制终止指定进程
nohup command &  # 在后台运行命令，并忽略挂起信号

# 权限管理
chmod 755 file.txt  # 修改文件权限
chmod 644 file.txt  # 修改文件权限   只读加可写
chown user:group file.txt  # 修改文件所有者和所属组
sudo command  # 以超级用户权限执行命令

# grep 过滤
grep 'pattern' file.txt  # 在文件中搜索匹配的行
grep -i 关键词  # 忽略大小写搜索关键词
grep -v 关键词  # 显示不包含关键词的行
grep -r 关键词 目录  # 在目录中递归搜索关键词
·ls | grep 关键词  # 列出目录下包含关键词的文件

conda 命令

conda --version
conda create -n myenv python=3.9
conda activate myenv
conda install numpy pandas matplotlib

conda list
conda env list
conda deactivate       #退出当前环境
conda remove -n myenv --all  #删除环境

conda list
conda export >envirment.yml  # 导出环境配置到文件

# shell 脚本
# !/bin/bash   # 指定脚本解释器
echo "Hello, World!"  # 输出文本

$变量名  引用变量
if [条件]; then
    # 条件为真时执行的代码
else
    # 条件为假时执行的代码
fi
# d3 结束le