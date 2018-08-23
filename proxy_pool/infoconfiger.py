configs = [
    {
        'site': 'xicidaili.com',
        'urls': [f'http://www.xicidaili.com/nn/{i}' for i in range(1, 2)],
        'type': 'xpath',
        'page_info': "//table[@id='ip_list']",
        'ip_port': {'ip': "//td[2]/text()", 'port': "//td[3]/text()"},
    },
]
