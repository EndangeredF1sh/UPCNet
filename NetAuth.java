import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Scanner;

public class NetAuth {
    private final String USER_AGENT = "Mozilla/5.0";

    private void sendGet(String number, String password, String ISP) throws Exception {
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
                sendPost(identity, number, password, ISP, wiredOrWireless);
            } else {
                System.err.println("似乎您已经成功登录，再看看？");
                System.exit(0);
            }
        }
    }

    private int doPost(String url, String parameter) throws Exception {
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

        int responseCode = connection.getResponseCode();
        return responseCode;
    }

    private int sendPost(String identity, String number, String password, String ISP, int wiredOrWireless) throws Exception {
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

    private int logout() throws Exception {
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

    public static void main(String[] args) {
        NetAuth netAuth = new NetAuth();

        if (args.length != 0 && args[0].equals("logout")) {
        try {
            netAuth.logout();
            System.out.println("退出成功！");

        } catch (Exception e) {
            System.err.println("退出失败，请重试！");
            System.err.println("详细信息：" + e.toString());
        }
        } else {
            //文件读取重定向
            FileInputStream fileInputStream = null;
            try {
                fileInputStream = new FileInputStream("config.txt");
            } catch (FileNotFoundException e) {
                System.err.println("请检查配置文件是否存在。");
                System.exit(-1);
            }
            System.setIn(fileInputStream);
            Scanner scanner = new Scanner(System.in);

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
                netAuth.sendGet(number, password, ISP);
                System.out.println("登陆成功！");
            } catch (Exception e) {
                System.err.println("尝试接入网络失败，请检查是否已经登录！");
                System.err.println("详细信息：" + e.toString());
            }
        }

    }
}