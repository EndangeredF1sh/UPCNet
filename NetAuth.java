import cn.liumengxiao.upcnet.dao.IDoGet;
import cn.liumengxiao.upcnet.dao.IDoPost;
import cn.liumengxiao.upcnet.impl.DoGetImpl;
import cn.liumengxiao.upcnet.impl.DoPostImpl;
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Scanner;

public class NetAuth {
    public static void main(String[] args) throws Exception {
        IDoGet doGet = new DoGetImpl();
        IDoPost doPost = new DoPostImpl();

        if (args.length != 0 && args[0].equals("logout")) {
            try {
                doPost.logout();
                System.out.println("退出成功！");

            } catch (Exception e) {
                System.err.println("退出失败，请重试！");
                System.err.println("详细信息：" + e.toString());
            }
        } else {
            File file = new File("config.txt");
            Scanner scanner = new Scanner(file);

            String number = null;
            String password = null;
            String ISP = null;

            try {
                number = scanner.next();
                password = scanner.next();
                ISP = scanner.next();
            } catch (Exception e) {
                System.err.println("无法从配置文件中读取账号信息，请核实！");
                System.exit(-1);
            }

            try {
                doGet.doGet(number, password, ISP);
                System.out.println("登陆成功！");
            } catch (Exception e) {
                System.err.println("尝试接入网络失败，请检查是否已经登录！");
                System.err.println("详细信息：" + e.toString());
            }
        }

    }
}