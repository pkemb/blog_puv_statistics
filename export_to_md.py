#!/usr/bin/env python2
#-*- coding: UTF-8 -*-

import json
import os

# 单个页面的统计结果
class page_puv_statistical:
    def __init__(self, puv):
        self.url = puv['url']
        self.site_uv = puv['site_uv']
        self.site_pv = puv['site_pv']
        self.page_pv = puv['page_pv']

# 站点的单次统计结果
class site_puv_statistical:
    def __init__(self, site_puv):
        self.time = site_puv['time']
        self.page_puvs = list()
        for page_puv in site_puv['page_puv']:
            self.page_puvs.append(page_puv_statistical(page_puv))
        self.count = 0

    def get_page_puv(self, url):
        for page_puv in self.page_puvs:
            if page_puv.url == url:
                return page_puv
        return None

    def get_site_uv(self):
        if len(self.page_puvs) > 1:
            return self.page_puvs[0].site_uv
        else:
            return 0

    def get_site_pv(self):
        if len(self.page_puvs) == 0:
            return 0

        total_pv = 0
        for page_puv in self.page_puvs:
            total_pv += page_puv.site_pv
        return int(total_pv/len(self.page_puvs))

    def __iter__(self):
        return self

    def next(self):
        if self.count < len(self.page_puvs):
            result = self.page_puvs[self.count]
            self.count += 1
            return result
        else:
            self.count = 0
            raise StopIteration

# 所有的统计结果
class puv_statistical:
    def __init__(self, stat_files):
        self.site_puvs = list()
        for stat_file in stat_files:
            with open(stat_file, "r") as f:
                value=f.read()
                if value:
                    stat_array = json.loads(value)['page_puv_statistics']
                    for site_puv in stat_array:
                        self.site_puvs.append(site_puv_statistical(site_puv))

    def export_site_uv(self):
        for site_puv in self.site_puvs:
            site_uv = site_puv.get_site_uv()
            print(site_puv.time + " " + str(site_uv))

    def export_site_pv(self):
        for site_puv in self.site_puvs:
            site_pv = site_puv.get_site_pv()
            print(site_puv.time + " " + str(site_pv))

    def export_site_puv_to_md(self, file):
        with open(file, 'w') as f:
            f.seek(0)
            f.truncate()
            f.write("| 时间 | pv | uv |\n")
            f.write("| - | - | - |\n")
            for site_puv in self.site_puvs:
                site_uv = site_puv.get_site_uv()
                site_pv = site_puv.get_site_pv()
                f.write("| %s | %d | %d |\n" % (site_puv.time, site_pv, site_uv))

    def export_page_pv_to_md(self, file):
        stat_by_url = dict()
        for site_puv in self.site_puvs:
            for page_pv in site_puv:
                if page_pv.url not in stat_by_url.keys():
                    stat_by_url[page_pv.url] = list()
                stat_by_url[page_pv.url].append({"time":site_puv.time,"page_pv":page_pv.page_pv})

        with open(file, 'w') as f:
            f.seek(0)
            f.truncate()
            for url in stat_by_url.keys():
                page_pvs = stat_by_url[url]
                f.write("# %s\n\n" % (url))
                f.write("| 时间 | pv |\n")
                f.write("| - | - |\n")
                for page_pv in page_pvs:
                    f.write("| %s | %d |\n" % (page_pv["time"], page_pv["page_pv"]))
                f.write("\n")

if __name__=='__main__':
    stat_file_list = list()
    for file in os.listdir(os.getcwd()):
        if file.startswith('page_puv_statistics_'):
            stat_file_list.append(file)

    puv_stat = puv_statistical(stat_file_list)
    puv_stat.export_page_pv_to_md('page_pv.md')
