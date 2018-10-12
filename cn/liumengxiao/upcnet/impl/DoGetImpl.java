package cn.liumengxiao.upcnet.impl;

import cn.liumengxiao.upcnet.dao.IDoGet;
import cn.liumengxiao.upcnet.dao.IDoPost;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class DoGetImpl implements IDoGet {
    private static final String USER_AGENT = "Mozilla/5.0";

    @Override
    public void doGet(String number, String password, String ISP) throws Exception {
        URL urlObject = new URL("http://121.251.251.217/&userlocation=ethtrunk/62:3501.0");
        HttpURLConnection connection = (HttpURLConnection) urlObject.openConnection();
        connection.setRequestMethod("GET");
        connection.setRequestProperty("User-Agent", USER_AGENT);

        int responseCode = connection.getResponseCode();

        //判断是否被劫持，同时判断有线无线
        String authGateway;
        int wiredOrWireless;
        if (responseCode == 200) {
            wiredOrWireless = 0;
            authGateway = "http://lan.upc.edu.cn";
        } else {
            URL urlObjectWireless = new URL("http://121.251.251.217/");
            connection = (HttpURLConnection) urlObjectWireless.openConnection();
            responseCode = connection.getResponseCode();
            wiredOrWireless = 1;
            authGateway = "http://121.251.251.217";
        }

        //接收数据流的处理
        BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
        String inputLine;
        StringBuffer response = new StringBuffer();
        while ((inputLine = in.readLine()) != null) {
            response.append(inputLine);
        }
        in.close();

        //判断是否在线
        String getURL = connection.getURL().toString();
        if ("http://www.upc.edu.cn".equals(getURL)) {
            System.err.println("似乎您已经成功登录，再看看？");
            System.exit(0);
        } else {
            if (getURL.indexOf("index.jsp") != -1) {
                String identity = getURL.substring(getURL.indexOf(".jsp?") + 5);
                identity = identity.replaceAll("&", "%2526");
                identity = identity.replaceAll("=", "%253D");
                IDoPost doPost = new DoPostImpl();
                doPost.login(identity, number, password, ISP, wiredOrWireless);
            } else {
                System.err.println("似乎您已经成功登录，再看看？");
                System.exit(0);
            }
        }
    }
}

