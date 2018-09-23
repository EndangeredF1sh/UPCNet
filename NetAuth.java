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

    private int sendPost(String identity, String number, String password, String ISP, int wiredOrWireless) throws Exception {
        //有线无线不同用户密码提交策略
        String url;
        if (wiredOrWireless == 0) {
            url = "http://lan.upc.edu.cn/eportal/InterFace.do?method=login";
        } else {
            url = "http://121.251.251.217/eportal/InterFace.do?method=login";
        }
        URL obj = new URL(url);
        HttpURLConnection connection = (HttpURLConnection) obj.openConnection();

        connection.setRequestMethod("POST");
        connection.setRequestProperty("User-Agent", USER_AGENT);
        connection.setRequestProperty("Accept-Language", "en-US,en;q=0.5");

        //用户密码密码等参数
        String urlParameters = "userId=" + number + "&password=" + password + "&service=" + ISP + "&queryString=" + identity + "&operatorPwd=&operatorUserId=&validcode=&passwordEncrypt=false";

        connection.setDoOutput(true);

        DataOutputStream wr = new DataOutputStream(connection.getOutputStream());
        wr.writeBytes(urlParameters);
        wr.flush();
        wr.close();

        int responseCode = connection.getResponseCode();
        return responseCode;

//        BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
//        String inputLine;
//        StringBuffer response = new StringBuffer();
//
//        while ((inputLine = in.readLine()) != null) {
//            response.append(inputLine);
//        }
//        in.close();
//
//        //打印结果
//        //System.out.println(response.toString());
    }


    public static void main(String[] args) {
        //文件读取重定向
        FileInputStream fileInputStream = null;
        try {
            fileInputStream = new FileInputStream("config.txt");
        } catch (FileNotFoundException e) {
            System.err.println("请检查配置文件是否存在。");
            System.exit(0);
        }
        System.setIn(fileInputStream);
        Scanner scanner = new Scanner(System.in);
        String number = scanner.next();
        String password = scanner.next();
        String ISP = scanner.next();

        NetAuth netAuth = new NetAuth();
        try {
            netAuth.sendGet(number, password, ISP);
            System.out.println("登陆成功！");
        } catch (Exception e) {
            System.err.println("尝试接入网络失败，请检查是否已经登录！");
        }

    }
}
