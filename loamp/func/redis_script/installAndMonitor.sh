#!/bin/sh

#######################
#适用于redis与外网隔离
#redis-master容灾脚本，运行在两台redis上，一台master，一台slave。如有其他slave-redis slaveof地址指向VIP。
#采用VIP的方式，实现redis-master的热备，如果master宕机或redis进程异常终止，备用redis可以在几秒内接管服务。
#######################
#下面几项是需要修改的地方
VIP="192.168.3.248"  #需要指定VIP
NETMASKIP="255.255.255.0"
PORT=6379 #指定端口
REDIS_PATH="/usr/local/redis" #指定程序运行目录
#######################

VIP_INTERFACE=""
create_time=`date +'%Y%m%d%H%m%S'`
date_time=`date +'%Y-%m-%d-%H-%m'`
filename=`ls|grep redis*.tar.gz`

#安装redis
if [[ -d $REDIS_PATH ]]
then
  echo "$date_time The directory is exist! It will be backup!" >>redis_info.log
  /bin/mv $REDIS_PATH "${REDIS_PATH}_${create_time}bak"
fi
mkdir -p $REDIS_PATH
tar -xzf $filename
cd ${filename%%".tar.gz"} && make
if [ "$?" != "0" ]
then
  echo "${date_time} redis make error,please check the dependent packages" >>../redis_info.log
  exit -1
fi
cd src && /bin/cp redis-server redis-cli $REDIS_PATH
/bin/cp ../../redis.conf $REDIS_PATH

#获取并设置网卡
num=`echo $VIP|cut -d "." -f 4`
str=`echo $VIP|cut -d '.' -f 1,2,3`
port_list=`ifconfig|grep "Link encap"|grep -v "lo"|awk -F " " '{print $1}'`
for p in $port_list
do
str1=`ifconfig $p|grep $str|wc -l`
if [[ $str1 == 1 ]]
then
  VIP_INTERFACE="$p:$num"
fi
break
done
echo $VIP_INTERFACE

#初始化启动redis
ping -c 3 $VIP
if [[ "$?" != "0" ]]
then
  ifconfig $VIP_INTERFACE $VIP netmask $NETMASKIP up 2>&1 >> up.log
  sed -i '/slaveof/d' redis.conf >/dev/null 2>&1
  $REDIS_PATH/redis-server $REDIS_PATH/redis.conf
else
  sed -i '/slaveof/d' redis.conf >/dev/null 2>&1
  echo "slaveof $SLAVEIP $PORT" >>redis.conf
  $REDIS_PATH/redis-server $REDIS_PATH/redis.conf
fi

#循环监控master状态
while(true)
do
re_str=`ps -ef|grep /redis-server|grep $PORT|grep -v grep|wc -l`
str=""
ping -c 3 $VIP
if [ "$?" != "0" ]
then
  if [[ $re_str -ge "1" ]]
  then
    echo `date` >> up.log
    ifconfig $VIP_INTERFACE $VIP netmask $NETMASKIP up 2>&1 >> up.log
    sed -i '/slaveof/d' redis.conf >/dev/null 2>&1
    $REDIS_PATH/redis-cli shutdown
    $REDIS_PATH/redis-server $REDIS_PATH/redis.conf
  fi
else
  re_str1=`ifconfig|grep $VIP|wc -l`
  if [[ $re_str -lt "1" ]]
  then
    if [[ $re_str1 == "1" ]]
    then
      ifconfig $VIP_INTERFACE down >/dev/null 2>&1
      sed -i '/slaveof/d' redis.conf >/dev/null 2>&1
      echo "slaveof $SLAVEIP $PORT" >>redis.conf
    fi
  fi
fi

sleep 1
done
