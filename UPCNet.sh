username=""
password=""
service=""
DATE=`date +%Y-%m-%d-%H:%M:%S`
tries=0
echo --- my_watchdog start ---
while [[ $tries -lt 3 ]]
do
        if /bin/ping -c 1 114.114.114.114 >/dev/null
        then
                echo --- exit ---
                exit 0
        fi
        tries=$((tries+1))
        sleep 1
done

echo $DATE network restart >>my_watchdog.log
/etc/init.d/network restart
sleep 10
parameter='userId='${username}'&password='${password}'&service='${service}'&queryString='
location='http://lan.upc.edu.cn/eportal/InterFace.do?method=login'
url=`curl -Ls -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36" -o /dev/null -w %{url_effective} http://121.251.251.217`
url=${url#http://lan.upc.edu.cn/eportal/index.jsp?}
url=${url//=/%253D}
url=${url//&/%2526}
url=${url//:/%253A}
url=${url//\//%252F}
parameter=${parameter}${url}'&operatorPwd=&operatorUserId=&validcode=&passwordEncrypt=false'
echo $parameter
curl -X POST -d $parameter $location
