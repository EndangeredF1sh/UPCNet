os_release_path="/etc/os-release"
openwrt_release_path="/etc/openwrt_release"
SHELL_FOLDER=$(dirname $(readlink -f "$0"))
if [ -f "$os_release_path" ];then
	source /etc/os-release
else
	if [ -f "$openwrt_release_path" ];then
		ID="openwrt"
	fi
fi
	
if [[ $ID != "openwrt" ]];then
	read -r -p "Mismatch Operation System Detected, Are you sure to install? [Y/n] " response
	if [[ $response != "y" && $response != "Y" ]];then
		exit 0
	fi
fi

echo "Auto install start ..."
opkg update
opkg install curl
wget --no-check-certificate https://raw.githubusercontent.com/EndangeredF1sh/UPCNet/bash/UPCNet.sh && chmod +x UPCNet.sh
echo -n "input stuID -> "
read stuID
echo -n "input password -> "
read passwd
echo "Select your service:
1. Campus Network Service
2. China Unicom Network Service
3. China Mobile Network Service
4. China Telecom Network Service
5. Campus Intranet
"
read -p "Enter selection [1-5] -> " num
	if [ $num -lt 1 ] || [ $num -gt 5 ];then
	echo "invalid selection, exit."; 
	exit;
	fi
 
	if [[ $num == 1 ]]; then
		service="default"
	fi
	
	if [[ $num == 2 ]]; then
		service="unicom"
	fi
	
	if [[ $num == 3 ]]; then
		service="cmcc"
	fi
	
	if [[ $num == 4 ]]; then
		service="ctcc"
	fi

	if [[ $num == 5 ]]; then
		service="local"
	fi


sed -i '1,3d' UPCNet.sh
sed -i "1i service=\"$service\"" UPCNet.sh
sed -i "1i password=\"$passwd\"" UPCNet.sh
sed -i "1i username=\"$stuID\"" UPCNet.sh


croncmd="sh ${SHELL_FOLDER}"/UPCNet.sh""
cronjob="*/1 * * * * $croncmd"
( crontab -l | grep -v -F "$croncmd" ; echo "$cronjob" ) | crontab -

sed -i "2a ${croncmd}" /etc/rc.local

echo "Auto Install Finished. Enjoy."
rm -- "$0"
