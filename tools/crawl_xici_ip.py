import requests
from scrapy.selector import Selector
import pymysql
conn = pymysql.connect(host='127.0.0.1',
                       user='root',
                       password='123',
                       db='db_gys',
                       charset='utf8',
                       use_unicode=True)

cursor = conn.cursor()


def crawl_ips():
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
                             " Ubuntu Chromium/58.0.3029.110 Chrome/58.0.3029.110 Safari/537.36"}
    MAX_PAGE = 5
    for i in range(MAX_PAGE):
        re = requests.get(url='http://www.xicidaili.com/wt/{0}'.format(i), headers=headers)
        selector = Selector(text=re.text)
        all_trs = selector.css('#ip_list tr')
        ip_list = []
        for tr in all_trs[1:]:
            speed_str = tr.css('.bar::attr(title)').extract()[0]
            if speed_str:
                speed = float(speed_str.split('秒')[0])
            all_texts = tr.css('td::text').extract()
            ip = all_texts[0]
            port = all_texts[1]
            proxy_type = all_texts[5]  # http
            if speed < 1:
                ip_list.append((ip, port, speed, proxy_type))
            print(ip)

        # 将爬取到的ip地址信息，保存到mysql数据库中
        for ip_info in ip_list:
            cursor.execute("INSERT INTO proxy_ip VALUES('{0}', '{1}', {2}, "
                           "'HTTP')".format(ip_info[0], ip_info[1], ip_info[2]))
            conn.commit()


class getIP(object):

    def delete_ip(self, ip):
        # 从数据库中删除无效的ip
        delete_sql = "delete from proxy_ip where ip='{0}'".format(ip)
        cursor.execute(delete_sql)
        conn.commit()
        return True

    def judge_ip(self, ip, port):
        # 判断ip是否可用
        http_url = 'http://www.baidu.com'
        proxy_url = 'http://{0}:{1}'.format(ip, port)
        print("proxy_url:", proxy_url)
        try:
            proxy_dict = {
                "http": proxy_url
            }
            response = requests.get(http_url, proxies=proxy_dict, timeout=20)
            print(response.status_code)
        except Exception as e:
            print("invalid ip and port")
            self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            print(code)
            if 200 <= code <= 300:
                print("effective ip")
                return True
            else:
                print("invalid ip and port")
                self.delete_ip(ip)
                return False

    def get_random_ip(self):
        # 从数据库中随机获取一个可用的ip
        random_sql = "select ip, port, speed from proxy_ip order by RAND() limit 1"
        result = cursor.execute(random_sql)
        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]
            speed = ip_info[2]
        print("speed:", speed)
        if speed < 1:
            self.delete_ip(ip)
            judge_res = self.judge_ip(ip, port)
            if judge_res:
                return "http://{0}:{1}".format(ip, port)
            else:
                return self.get_random_ip()
        else:
            return self.get_random_ip()


if __name__ == '__main__':
    get_ip = getIP()
    ip_information = get_ip.get_random_ip()
    print("final_result:", ip_information)
