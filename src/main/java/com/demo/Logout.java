package com.demo;

import com.demo.base.GetMethod;
import com.demo.base.PostMethod;

import java.io.File;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Scanner;

public class Logout {
    public static void main(String[] args) throws Exception {
        GetMethod doGet = new GetMethod();
        PostMethod doPost = new PostMethod();

        File file = new File("config.txt");
        Scanner scanner = new Scanner(file);

        String username = scanner.next();
        String password = scanner.next();

        //获取包含 Cookie 的原始数据
        String setCookie = doPost.getCookie(username, password);

        //截取字符串
        int strStartIndex = setCookie.indexOf("ounion=");
        int strEndIndex = setCookie.indexOf(";");
        if (strStartIndex < 0 || strEndIndex < 0) {
            System.err.println("获取 Cookie 失败！");
        }
        String cookie = setCookie.substring(strStartIndex, strEndIndex).substring("ounion=".length());

        //下线页面地址
        String offlineUrl = "https://zhxyapp.upc.edu.cn/extensions/wap/networkfee/offline.html";

        //发送 POST 请求
        URL obj = new URL(offlineUrl);
        HttpURLConnection connection = (HttpURLConnection) obj.openConnection();
        connection.setRequestMethod("POST");
        connection.setRequestProperty("User-Agent", "Mozilla/5.0");
        connection.setRequestProperty("Accept-Language", "en-US,en;q=0.5");
        cookie = "appunion=1; ounion=" + cookie;
        connection.setRequestProperty("Cookie", cookie);

        int responseCode = connection.getResponseCode();
        if (responseCode == 200) {
            System.out.println("下线请求提交成功！");
        } else {
            System.err.println("似乎哪里出现了问题，再试一次？");
        }
    }

}
