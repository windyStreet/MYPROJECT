#!/bin/sh


#######################
#redis容灾脚本，当前的redis-master遇到宕机可以在几秒内接管服务。
#######################
#采用VIP的方式，实现redis-master的热备，如果master宕机或redis进程异常终止，备用master服务器可以自动接管服务
#两台服务器，关掉任意一台，另外一台作为master，重新启动的作为slave

MASTERIP="192.168.3.173"  #当前程序运行主机IP
SLAVEIP="192.168.3.168"   #另外一台主机IP
NETMASKIP="255.255.255.0"
VIP="192.168.3.248"       #虚拟IP，所有的read服务器都指向这地址
PORT=6379
REDIS_PATH="/usr/local/redis"
num=`echo $VIP|cut -d "." -f 4`
VIP_INTERFACE="eth0:$num"
str_sentinel=`ps -ef|grep $REDIS_PATH/redis-sentinel|grep -v grep|wc -L`


#初始化启动redis服务
ping -c 3 $VIP
if [[ "$?" != "0" ]]
then
  echo "11"
  ifconfig $VIP_INTERFACE $VIP netmask $NETMASKIP up 2>&1 >> up.log
  ch_str=`sed -n '/127.0.0.1/p' redis.conf|grep -v "#"`
  sed -i "s#$ch_str#bind 127.0.0.1 $MASTERIP $VIP#g" redis.conf >/dev/null 2>&1
  sed -i '/slaveof/d' redis.conf >/dev/null 2>&1
  $REDIS_PATH/redis-server $REDIS_PATH/redis.conf
else
  echo "22"
  ch_str=`sed -n '/127.0.0.1/p' redis.conf|grep -v "#"`
  sed -i "s#$ch_str#bind 127.0.0.1 $MASTERIP#g" redis.conf >/dev/null 2>&1
  sed -i '/slaveof/d' redis.conf >/dev/null 2>&1
  echo "slaveof $SLAVEIP $PORT" >>redis.conf
  $REDIS_PATH/redis-server $REDIS_PATH/redis.conf
fi

#监听redis或VIP网络状态
while(true)
do
re_str=`ps -ef|grep /redis-server|grep $PORT|grep -v grep|wc -l`
str=""
ping -c 3 $VIP
if [ "$?" != "0" ]
then
  if [[ $re_str -ge "1" ]]
  then
    echo "a"
    echo `date` >> up.log
    ifconfig $VIP_INTERFACE $VIP netmask $NETMASKIP up 2>&1 >> up.log
    ch_str=`sed -n '/127.0.0.1/p' redis.conf|grep -v "#"`
    sed -i "s#$ch_str#bind 127.0.0.1 $MASTERIP $VIP#g" redis.conf >/dev/null 2>&1
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
      echo "b"
      ifconfig $VIP_INTERFACE down >/dev/null 2>&1
      ch_str=`sed -n '/127.0.0.1/p' redis.conf|grep -v "#"`
      sed -i "s#$ch_str#bind 127.0.0.1 $MASTERIP#g" redis.conf >/dev/null 2>&1
      sed -i '/slaveof/d' redis.conf >/dev/null 2>&1
      echo "slaveof $SLAVEIP $PORT" >>redis.conf
    fi
  fi
fi

sleep 1
done
