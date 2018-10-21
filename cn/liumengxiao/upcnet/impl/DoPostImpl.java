package cn.liumengxiao.upcnet.impl;

import cn.liumengxiao.upcnet.dao.IDoPost;
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class DoPostImpl implements IDoPost {
    private static final String USER_AGENT = "Mozilla/5.0";

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

    @Override
    public int doPost(String url, String parameter) throws Exception {
        HttpURLConnection connection = post(url, parameter);
        int responseCode = connection.getResponseCode();
        return responseCode;
    }

    @Override
    public int login(String identity, String number, String password, String ISP, int wiredOrWireless) throws Exception {
        //有线无线不同用户密码提交策略
        String url;
        if (wiredOrWireless == 0) {
            url = "http://lan.upc.edu.cn/eportal/InterFace.do?method=login";
        } else {
            url = "http://121.251.251.217/eportal/InterFace.do?method=login";
        }

        String urlParameters = "userId=" + number + "&password=" + password + "&service=" + ISP + "&queryString=" + identity + "&operatorPwd=&operatorUserId=&validcode=&passwordEncrypt=false";
        int reuslt = doPost(url, urlParameters);
        return reuslt;
    }

    @Override
    public int logout() throws Exception {
        String url = "http://lan.upc.edu.cn/eportal/InterFace.do?method=logout";

        int responseCode = 0;
        boolean wired = true;

        while (wired) {
            String urlParameters = null;
            if (wired) {
                String getInfo = "http://lan.upc.edu.cn/eportal/InterFace.do?method=getOnlineUserInfo";
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

                BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
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

            url = "http://121.251.251.217/eportal/InterFace.do?method=logout";
            wired = false;
            continue;
        }
        return responseCode;
    }

    @Override
    public String getCookie(String username, String password) throws Exception {
        String url = "https://zhxyapp.upc.edu.cn/wap/login/commit.html";
        String parameter = "username="+username+"&password="+password;

        HttpURLConnection connection = post(url, parameter);

        String cookie = connection.getHeaderField("set-cookie");
        return cookie;
    }
}
