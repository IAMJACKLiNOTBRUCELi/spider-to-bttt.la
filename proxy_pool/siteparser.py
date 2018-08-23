from lxml import etree
import traceback


class Parser(object):
    @staticmethod
    def xpath_parse(resp, parse_config):
        try:
            page = etree.HTML(resp)
            page_info = page.xpath(parse_config['page_info'])[0]
            ip_info = page_info.xpath(parse_config['ip_port']['ip'])
            port_info = page_info.xpath(parse_config['ip_port']['port'])
            proxy_list = []
            for ip, port in zip(ip_info, port_info):
                proxy_list.append({'proxy_ip': ip + ':' + port})
            # print(proxy_list)
            return proxy_list

        except Exception:
            traceback.print_exc()

    @staticmethod
    def re_parse(resp, parse_config):
        try:
            pass

        except Exception:
            traceback.print_exc()

    def who_parse(self, resp, parse_config):
        if parse_config['type'] == 'xpath':
            return self.xpath_parse(resp, parse_config)

        elif parse_config['type'] == 're':
            return self.re_parse(resp, parse_config)

