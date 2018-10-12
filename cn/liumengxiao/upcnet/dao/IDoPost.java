package cn.liumengxiao.upcnet.dao;

public interface IDoPost {
    public int doPost(String url, String parameter) throws Exception;
    public int login(String identity, String number, String password, String ISP, int wiredOrWireless) throws Exception;
    public int logout() throws Exception;
    public String getCookie(String username, String password) throws Exception;
}
