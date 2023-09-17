back=""
username=""
password=""
service=""
usernameB=""
passwordB=""
serviceB=""

DATE=`date +%Y-%m-%d-%H:%M:%S`
tries=0
echo "Start detecting network connection status......"
while [[ $tries -lt 2 ]]
do
        ip_list="119.29.29.29,223.5.5.5"
        ips=$(echo "$ip_list" | tr ',' ' ')
        for ip in $ips
        do
                if /bin/ping -c 1 "$ip" >/dev/null
                then
                        echo "The network connection is normal, enjoy~"
                        echo "---close script---"
                        exit 0
                fi
        done
        tries=$((tries+1))
        sleep 1
done
echo "!!!ERROR: Network connection exception!!!"
echo "Start writing to the log and execute the login script..."
echo $DATE network offline and try to restart... ... >>my_watchdog.log
# /etc/init.d/network restart
# 重启网卡需要吗？
# sleep 3
parameter='userId='${username}'&password='${password}'&service='${service}'&queryString='
location='http://121.251.251.207/eportal/InterFace.do?method=login'
url=`curl -Ls -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36" -o /dev/null -w %{url_effective} http://121.251.251.217`
url=${url#*/eportal/index.jsp?}
url=${url//=/%253D}
url=${url//&/%2526}
url=${url//:/%253A}
url=${url//\//%252F}
parameter=${parameter}${url}'&operatorPwd=&operatorUserId=&validcode=&passwordEncrypt=false'
# echo $parameter
echo -e "Try to log in using the primary account\n"
curl -X POST -d $parameter $location
sleep 8
if [ $back == 2 ]
then
triesagain=0

while [[ $triesagain -lt 2 ]]
do
        ip_list="119.29.29.29,223.5.5.5"
        ips=$(echo "$ip_list" | tr ',' ' ')
        for ip in $ips
        do
                if /bin/ping -c 1 "$ip" >/dev/null
                then
                        echo -e "\n"
                        echo "Log in with your primary account, the network is back to normal, enjoy~"
                        echo "---close script---"
                        exit 0
                fi
        done
        tries=$((triesagain+1))
        sleep 1
done
echo -e "FAILED, Start trying to log in with an alternate account\n"
parameterB='userId='${usernameB}'&password='${passwordB}'&service='${serviceB}'&queryString='
parameterB=${parameterB}${url}'&operatorPwd=&operatorUserId=&validcode=&passwordEncrypt=false'
# echo $parameterB
curl -X POST -d $parameterB $location
triesagain2=0
while [[ $triesagain2 -lt 2 ]]
do
        ip_list="119.29.29.29,223.5.5.5"
        ips=$(echo "$ip_list" | tr ',' ' ')
        for ip in $ips
        do
                if /bin/ping -c 1 "$ip" >/dev/null
                then
                        echo -e "\n"
                        echo "Log in with your alternate account, the network is back to normal, enjoy~"
                        echo "---close script---"
                        exit 0
                fi
        done
        tries=$((triesagain2+1))
        sleep 1
done
echo "You can't sign in with your existing account. Please check your configuration and other network settings and close script"
fi
