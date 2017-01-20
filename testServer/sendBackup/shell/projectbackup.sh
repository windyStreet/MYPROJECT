#! /bin/bash

function incrementalupdate()
{
	lastVersion=$(expr "scale=3;$version - 0.001"|bc)
        echo "$lastVersion  <=  ${version%.*}"
        if [ `echo "$lastVersion  <=  ${version%.*}" | bc` -eq 1 ] ; then
        #if [ $lastVersion -le ${version%.*} ] ; then
                lastVersion=${version%.*}
        fi
        echo "last version number is "$lastVersion
	lastVersiondir=V1.0.$lastVersion"_"$lastversiondate
        echo "last version directory is "$lastVersiondir
	#上个版本的备份
	lastbackuppath=/data/___DEPLOY___/${projectname}/${lastVersiondir}
	lastotherrespath=/data/smbshare/project_update/$projectname/v$lastVersion
	if [ ! -d /data/___DEPLOY___/${projectname}/${lastVersiondir} ] ; then
		echo "last version updateResource not exist "
		echo "/data/___DEPLOY___/${projectname}/${lastVersiondir}"
		exit 1
	fi
	#先复制之前版本的全部内容
	cp -rf /data/___DEPLOY___/${projectname}/${lastVersiondir}/* /data/___DEPLOY___/${projectname}/${versiondir}/
	#再读取现需要更新资源
	cpFlag=None
	updateFile=$otherrespath/update.txt
	if [ -f $updateFile ] ; then
		#复制lib和ResourceLib文件
		cat $updateFile | while read linestr
		do
			#echo $linestr
			tmpvar=${linestr#*[}
			line=${tmpvar%]*}
			if [ "$line" == "lib" ] ; then
				cpFlag="lib"
				continue
			fi
			if [ "$line" == "ResourceLib" ] ; then
				cpFlag="ResourceLib"
				continue
			fi
			if [ "$cpFlag" == "lib" ] ; then
				#检查文件是否存在
				#复制该文件
				libFile=${projectpath}/lib/$line
				if [ -f $libFile ] ; then
					cp -rf $libFile ${backuppath}/lib/
					echo "copy  $libFile to ${backuppath}/lib/ "
				else
					echo "$libFile,not exist,check the project and update file"
				fi
			elif [ "$cpFlag" == "ResourceLib" ] ; then
				ResourceLibFile=${projectpath}/ResourceLib/$line
				if [ -f $ResourceLibFile ] ; then
					cp -rf $ResourceLibFile ${backuppath}/ResourceLib/
					echo "copy $ResourceLibFile to ${backuppath}/ResourceLib/"
				else
					echo "$ResourceLibFile,not exist,check the project and update file"
				fi
			else
				echo "error file content , please check $updateFile file"
			fi
		done
		#复制静态资源
		echo "复制静态资源"
		cp -rf ${otherrespath}/* ${backuppath}/other
		sleep 3s
		echo "incrementalupdate Resource copy finish"
	else
		echo "$updateFile not exist,can not proecssing incremental update"
		echo "please check $updateFile file"
		exit 1
	fi
}

function totalupdate()
{
#【执业证项目】
if [ "$projectname" = "LSIP" ];then
   echo "正在备份【执业证项目】lib...."
   cp -rf ${projectpath}/lib/TICKET.BLL.jar ${backuppath}/lib
   cp -rf ${projectpath}/lib/LEAP.ISIP.* ${backuppath}/lib
   cp -rf ${projectpath}/lib/LEAP.LSIP.* ${backuppath}/lib
   cp -rf ${projectpath}/lib/TESTOL.BLL.jar ${backuppath}/lib
   echo "正在备份【执业证项目】ResourceLib...."
   cp -rf ${projectpath}/ResourceLib/LEAP.LSIP.* ${backuppath}/ResourceLib
   cp -rf ${projectpath}/ResourceLib/TICKET.client.jar ${backuppath}/ResourceLib
   #echo "正在备份【执业证项目】其他资源"
   #cp -r  ${otherrespath}/* ${backuppath}/other
   echo "备份正式包到share"
   cp -rf ${backuppath}  /data/smbshare/project_jar/ZS-LSIP/
   chown -R nobody:nogroup /data/smbshare/project_jar/ZS-LSIP/
#【保宝网项目】
elif [ "$projectname" = "YXYBB" ];then
   echo "正在备份【保宝网项目】lib...."
   cp -rf ${projectpath}/lib/LEAP.LSIP.* ${backuppath}/lib
   cp -rf ${projectpath}/lib/TESTOL.BLL.jar ${backuppath}/lib
   cp -rf ${projectpath}/lib/LUPDP.BLL.jar ${backuppath}/lib
   cp -rf ${projectpath}/lib/LWXP.BLL.jar ${backuppath}/lib
   cp -rf ${projectpath}/lib/RedisCache.jar ${backuppath}/lib
   cp -rf ${projectpath}/lib/CommonUtils.jar ${backuppath}/lib
   cp -rf ${projectpath}/lib/LEAP.LUPDP.Util.jar ${backuppath}/lib
   echo "正在备份【保宝网项目】ResourceLib...."
   cp -rf ${projectpath}/ResourceLib/LUPDP.Client.jar ${backuppath}/ResourceLib
   cp -rf ${projectpath}/ResourceLib/LWXP.Client.jar ${backuppath}/ResourceLib
   echo "正在备份【保宝网项目】其他资源"
   cp -rf  ${otherrespath}/* ${backuppath}/other
#【保宝app项目】
elif [ "$projectname" = "BBT" ];then
   echo "正在备份【保宝app项目】lib...."
   cp -rf ${projectpath}/lib/LEAP.LSIP.* ${backuppath}/lib
   cp -rf ${projectpath}/lib/TESTOL.BLL.jar ${backuppath}/lib
   cp -rf ${projectpath}/lib/BBT.BLL.jar ${backuppath}/lib
   cp -rf ${projectpath}/lib/RedisCache.jar ${backuppath}/lib
   cp -rf ${projectpath}/lib/CommonUtils.jar ${backuppath}/lib
   echo "正在备份【保宝app项目】ResourceLib...."
   cp -rf ${projectpath}/ResourceLib/BBT.Client.jar ${backuppath}/ResourceLib
   echo "正在备份【保宝app项目】其他资源"
   cp -rf  ${otherrespath}/* ${backuppath}/other
#【保易项目】
elif [ "$projectname" = "INSY" ];then
   echo "正在备份【保易项目】lib...."
   cp -rf ${projectpath}/lib/insy.BLL.jar ${backuppath}/lib
   cp -rf ${projectpath}/lib/CDNUploader.jar ${backuppath}/lib
   cp -rf ${projectpath}/lib/CommonUtils.jar ${backuppath}/lib
   echo "正在备份【保易项目】ResourceLib...."
   cp -rf ${projectpath}/ResourceLib/insy.Client.jar ${backuppath}/ResourceLib
   echo "正在备份【保易项目】其他资源"
   cp -rf  ${otherrespath}/* ${backuppath}/other
#【水危职业系统项目】
elif [ "$projectname" = "LWDP" ];then
  echo "正在备份【水危职业系统项目】lib...."
   cp -rf ${projectpath}/lib/TICKET.BLL.jar ${backuppath}/lib
   cp -rf ${projectpath}/lib/LEAP.LSIP.* ${backuppath}/lib
   #cp -rf ${projectpath}/lib/TESTOL.BLL.jar ${backuppath}/lib
   echo "正在备份【水危职业系统项目】ResourceLib...."
   cp -rf ${projectpath}/ResourceLib/LEAP.LSIP.* ${backuppath}/ResourceLib
   cp -rf ${projectpath}/ResourceLib/TICKET.client.jar ${backuppath}/ResourceLib
   #$echo "正在备份【水危职业系统项目】其他资源"
   #cp -rf  ${otherrespath}/* ${backuppath}/other
#【水危web项目】
elif [ "$projectname" = "LSWP" ];then
   echo "正在备份#【水危web项目】lib...."
   cp -rf ${projectpath}/lib/LEAP.LSIP.* ${backuppath}/lib
   cp -rf ${projectpath}/lib/LSWP.BLL.jar ${backuppath}/lib
   cp -rf ${projectpath}/lib/LWXP.BLL.jar ${backuppath}/lib
   #cp -rf ${projectpath}/lib/RedisCache.jar ${backuppath}/lib
   #cp -rf ${projectpath}/lib/CommonUtils.jar ${backuppath}/lib
   #cp -rf ${projectpath}/lib/LEAP.LUPDP.Util.jar ${backuppath}/lib
   #cp -rf ${projectpath}/lib/TESTOL.BLL.jar ${backuppath}/lib
   echo "正在备份#【水危web项目】ResourceLib...."
   cp -rf ${projectpath}/ResourceLib/LSWP.Client.jar ${backuppath}/ResourceLib
   cp -rf ${projectpath}/ResourceLib/LWXP.Client.jar ${backuppath}/ResourceLib
   echo "正在备份#【水危web项目】其他资源"
   cp -rf  ${otherrespath}/* ${backuppath}/other
#【在线测试】
elif [ "$projectname" = "LESP" ];then
   echo "正在备份【保宝网项目】lib...."
   cp -rf ${projectpath}/lib/LEAP.LSIP.* ${backuppath}/lib
   #cp -rf ${projectpath}/lib/TESTOL.BLL.jar ${backuppath}/lib
   cp -rf ${projectpath}/lib/LESP.BLL.jar ${backuppath}/lib
   cp -rf ${projectpath}/lib/LWXP.BLL.jar ${backuppath}/lib
   cp -rf ${projectpath}/lib/RedisCache.jar ${backuppath}/lib
   cp -rf ${projectpath}/lib/CommonUtils.jar ${backuppath}/lib
   cp -rf ${projectpath}/lib/LEAP.LUPDP.Util.jar ${backuppath}/lib
   echo "正在备份【保宝网项目】ResourceLib...."
   cp -rf ${projectpath}/ResourceLib/LESP.Client.jar ${backuppath}/ResourceLib
   #cp -rf ${projectpath}/ResourceLib/LWXP.Client.jar ${backuppath}/ResourceLib
   echo "正在备份【保宝网项目】其他资源"
   cp -rf  ${otherrespath}/* ${backuppath}/other
#【河南服务监督系统项目】
elif [ "$projectname" = "HNIS" ];then
  echo "正在备份【河南服务监督系统项目】lib...."
   cp -rf ${projectpath}/lib/HNIS.BLL.jar ${backuppath}/lib
   #cp -rf ${projectpath}/lib/hnis_server.jar  ${backuppath}/lib
   cp -rf ${projectpath}/lib/ISXS.policydata.interface.jar  ${backuppath}/lib
   cp -rf ${projectpath}/lib/ISXS.policydata.proccess.jar  ${backuppath}/lib
   echo "正在备份【河南服务监督系统项目】ResourceLib...."
   cp -rf ${projectpath}/ResourceLib/HNIS.Client.jar ${backuppath}/ResourceLib
   cp -rf ${projectpath}/ResourceLib/hnis.Resource.jar ${backuppath}/ResourceLib
   #$echo "正在备份【河南服务监督系统项目】其他资源"
   #cp -rf  ${otherrespath}/* ${backuppath}/other
#【贵州服务监督系统项目】
elif [ "$projectname" = "GZIS" ];then
  echo "正在备份【贵州服务监督系统项目】lib...."
   cp -rf ${projectpath}/lib/ISXS.BLL.jar ${backuppath}/lib
   cp -rf ${projectpath}/lib/ISXS.policydata.interface.jar  ${backuppath}/lib
   cp -rf ${projectpath}/lib/ISXS.policydata.proccess.jar  ${backuppath}/lib
   echo "正在备份【贵州服务监督系统项目】ResourceLib...."
   cp -rf ${projectpath}/ResourceLib/ISXS.Client.jar ${backuppath}/ResourceLib
   cp -rf ${projectpath}/ResourceLib/hnis.Resource.jar ${backuppath}/ResourceLib
   #$echo "正在备份【贵州服务监督系统项目】其他资源"
   #cp -rf  ${otherrespath}/* ${backuppath}/other
#【在线广告系统项目】
elif [ "$projectname" = "LAMP" ];then
  echo "正在备份【在线广告系统项目】lib...."
   cp -rf ${projectpath}/lib/LEAP.LAMP.BLL.jar ${backuppath}/lib
   echo "正在备份【在线广告系统项目】ResourceLib...."
   cp -rf ${projectpath}/ResourceLib/LEAP.LAMP.Client.jar ${backuppath}/ResourceLib
   #$echo "正在备份【在线广告系统项目】其他资源"
   #cp -rf  ${otherrespath}/* ${backuppath}/other

fi
}
###########################全量更新配置完毕############################

#备份资源
function backupResource(){
    echo "正在压缩..."
    cd /data/___DEPLOY___/${projectname}
    tar -zcvPf ${versiondir}.tar ./${versiondir}
}

#发送资源
function senResource(){
    if [ "$projectname" = "LSIP" ] || [ "$projectname" = "YXYBB" ] || [ "$projectname" = "BBT" ]  || [ "$projectname" = "INSY" ] ||  [ "$projectname" = "LESP" ] ||  [ "$projectname" = "HNIS" ]  || [ "$projectname" = "GZIS"  ] || [ "$projectname" = "LAMP" ] ;then
      echo "正在连接远程深圳服务器${remote}"
      scp -r -P 62222 ${backuppath}.tar ${remote}
    elif [ "$projectname" = "LWDP" ] || [ "$projectname" = "LSWP" ];then
      echo "正在连接远程水危服务器${remote1}"
      scp -r -P 62222 ${backuppath}.tar ${remote1}
    fi
}
function update(){
    initENV
    if [ "${updatetype}" == "add" ]  ; then
        #增量更新
        incrementalupdate

    elif [  "${updatetype}" == "full" ] ; then
        #全量更新
            totalupdate
    else
        echo "not get updatetype "
        exit 1
    fi
    backupResource
    senResource
}

function initENV(){
    if [ "$projectname" = "LSIP" ];then
        projectpath=/usr/longrise/LSIP/LSIPTEST/WEB-INF
    elif [ "$projectname" = "YXYBB" ];then
        projectpath=/usr/longrise/LUPDPTEST/WEB-INF
    elif [ "$projectname" = "LAMP" ];then
        projectpath=/usr/longrise/LAMPTEST/WEB-INF
    elif [ "$projectname" = "BBT" ];then
        projectpath=/usr/longrise/BBT/WEB-INF
    elif [ "$projectname" = "INSY" ];then
        projectpath=/usr/longrise/insytest/WEB-INF
    elif [ "$projectname" = "LWDP" ];then
        projectpath=/usr/longrise/LWDPTEST/WEB-INF
    elif [ "$projectname" = "LSWP" ];then
        projectpath=/usr/longrise/LSWPTEST/WEB-INF
    elif [ "$projectname" = "LESP" ];then
        projectpath=/usr/longrise/LESPTEST/WEB-INF
    elif [ "$projectname" = "HNIS" ];then
        projectpath=/usr/longrise/hnis/WEB-INF
    elif [ "$projectname" = "GZIS" ];then
        projectpath=/usr/longrise/GZIS/WEB-INF
    else
        echo "项目不存在..."
        exit 1
    fi

    versiondir=V1.0.$version"_"${bakdate}

    #深证服务器【保宝网项目】【执业证项目】【保宝app项目】【保易项目】【在线测试】
    remote=220.231.252.31:/datafile/fileshare/${projectname}JAR
    #北京服务器【水危项目】
    remote1=120.132.117.19:/datafile/fileshare/${projectname}JAR

    backuppath=/data/___DEPLOY___/${projectname}/${versiondir}
    otherrespath=/data/smbshare/project_update/$projectname/v$version


    echo "当前项目路径为：${projectpath}"
    echo "当前备份目录为：${backuppath}"

    mkdir -p ${backuppath}/lib
    mkdir -p ${backuppath}/ResourceLib
    mkdir -p ${backuppath}/other

}

function help(){
    echo "-h help info"
    echo "-P projectname,eg:-P YXYBB"
    echo "-m [update]"
    echo "  upate:proiect update function"
    echo "-t time,eg:-t 20161223"
    echo "-T [add,full]"
    echo "  add:incrementalupdate"
    echo "  full:totalupdate"
    echo "-o lastversiondate,eg -o 20161225"
}

method=""
projectname=""
version=""
bakdate=""
updatetype=""
lastversiondate=""
while getopts ":m:P:v:t:T:o:h" opt
do
        case $opt in
                h ) help
                    ;;
                m ) method=$OPTARG
                    ;;
                P ) projectname=$OPTARG
                    ;;
                v ) version=$OPTARG
                    ;;
                t ) bakdate=$OPTARG
                    ;;
                T ) updatetype=$OPTARG
                    ;;
                o ) lastversiondate=$OPTARG
                    ;;
                ? ) help
                    exit 1;;
        esac
done

#-m update -P YXYBB -v 203.003 -t 20150623 -T add

if [ "$method" == "update" ] ; then
    update
elif [ "$method" == "help" ] ; then
    help
else
    help
    exit 1
fi