package com.demo.base;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.Charset;

public class PostMethod {
    private static final String USER_AGENT = "Mozilla/5.0";
    private static final String WIRELESS_GATEWAY = "http://wlan.upc.edu.cn/";
    private static final String WIRED_GATEWAY = "http://lan.upc.edu.cn/";


    public HttpURLConnection post(String url, String parameter) throws Exception {
        URL obj = new URL(url);
        HttpURLConnection connection = (HttpURLConnection) obj.openConnection();

        connection.setRequestMethod("POST");
        connection.setRequestProperty("User-Agent", USER_AGENT);
        connection.setRequestProperty("Accept-Language", "en-US,en;q=0.5");

        connection.setDoOutput(true);

        DataOutputStream wr = new DataOutputStream(connection.getOutputStream());
        if (parameter != null) {
            wr.writeBytes(parameter);
        }
        wr.flush();
        wr.close();

        return connection;
    }

    public int doPost(String url, String parameter) throws Exception {
        HttpURLConnection connection = post(url, parameter);
        int responseCode = connection.getResponseCode();
        return responseCode;
    }

    public Boolean login(String identity, String number, String password, String ISP, int wiredOrWireless) throws Exception {
        //有线无线不同用户密码提交策略
        String url;
        if (wiredOrWireless == 0) {
            url = WIRED_GATEWAY + "eportal/InterFace.do?method=login";
        } else {
            url = WIRELESS_GATEWAY + "eportal/InterFace.do?method=login";
        }

        String urlParameters = "userId=" + number + "&password=" + password + "&service=" + ISP + "&queryString=" + identity + "&operatorPwd=&operatorUserId=&validcode=&passwordEncrypt=false";
        int reuslt = doPost(url, urlParameters);

        if (reuslt == 200) {
            return true;
        } else {
            return false;
        }
    }

    public int logout() throws Exception {
        String url = WIRED_GATEWAY + "eportal/InterFace.do?method=logout";

        int responseCode = 0;
        boolean wired = true;

        while (wired) {
            String urlParameters = null;
            if (wired) {
                String getInfo = WIRED_GATEWAY + "eportal/InterFace.do?method=getOnlineUserInfo";
                //获取userIndex
                URL obj = new URL(getInfo);
                HttpURLConnection connection = (HttpURLConnection) obj.openConnection();

                connection.setRequestMethod("POST");
                connection.setRequestProperty("User-Agent", USER_AGENT);
                connection.setRequestProperty("Accept-Language", "en-US,en;q=0.5");

                connection.setDoOutput(true);

                DataOutputStream wr = new DataOutputStream(connection.getOutputStream());
                wr.flush();
                wr.close();

                BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream(), "UTF-8"));
                String inputLine;
                StringBuffer response = new StringBuffer();

                while ((inputLine = in.readLine()) != null) {
                    response.append(inputLine);
                }
                in.close();

                if (response.equals("")) {
                    System.err.println("获取userIndex失败，请重试！");
                } else {
                    JSON json = JSON.parseObject(response.toString());
                    String userIndex = ((JSONObject) json).getString("userIndex");
                    urlParameters = "method=logout&userIndex=" + userIndex;
                }

            } else {
                urlParameters = "method=logout";
            }

            doPost(url, urlParameters);

            url = WIRELESS_GATEWAY + "eportal/InterFace.do?method=logout";
            wired = false;
            continue;
        }
        return responseCode;
    }

    public String getCookie(String username, String password) throws Exception {
        String url = "https://zhxyapp.upc.edu.cn/wap/login/commit.html";
        String parameter = "username=" + username + "&password=" + password;

        HttpURLConnection connection = post(url, parameter);

        String cookie = connection.getHeaderField("set-cookie");
        return cookie;
    }
}
