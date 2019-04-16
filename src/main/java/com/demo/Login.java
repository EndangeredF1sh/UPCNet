package com.demo;

import com.demo.base.GetMethod;
import com.demo.base.PostMethod;

import java.io.File;
import java.util.Scanner;

public class Login {
    public static void main(String[] args) throws Exception {
        GetMethod doGet = new GetMethod();
        PostMethod doPost = new PostMethod();

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
                System.out.println("登录成功！");
            } catch (Exception e) {
                System.err.println("尝试接入网络失败，请检查是否已经登录！");
                System.err.println("详细信息：" + e.toString());
            }
        }
    }
}
