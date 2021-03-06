#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.utils.safestring import mark_safe
from time import sleep

class PageInfo(object):
    def __init__(self,currentPage,totalItems,perItems=5,pageNum=6):
        try:
            currentPage = int(currentPage)
        except Exception as e:
            currentPage = 1
        self.current_page = currentPage
        self.per_items = perItems
        self.total_items = totalItems
        self.page_num = pageNum

    @property
    def total_page(self):
        if not self.total_items:
            self.total_items = 0
        val = int(self.total_items / self.per_items) + 1 if self.total_items % self.per_items > 0 else self.total_items / self.per_items
        #print(int(self.total_items / self.per_items),'val',val)
        return val
    @property
    def start(self):
        val = (self.current_page -1 ) * self.per_items
        return val

    @property
    def end(self):
        val = self.current_page * self.per_items
        return val
    def pager(self):
        page_html = []
        page = self.current_page
        all_page_count = self.total_page
        total_items = self.total_items

        first_html = "<li><a href='javascript:void(0)' onclick='ChangePage(1)'>首页</a></li>"
        page_html.append(first_html)

        if page <= 1:
            prev_html = "<li class='disabled'><a href='javascript:void(0)'>上一页</a></li>"
        else:
            prev_html = "<li><a href='javascript:void(0)' onclick='ChangePage(%d)'>上一页</a></li>" %(page-1,)
        page_html.append(prev_html)

        if all_page_count <11:
            begin = 0
            end = all_page_count
        else:
            if page < 6:
                begin = 0
                end = 11
            else:
                if page + 6 > all_page_count:
                    begin = page - 6
                    end = all_page_count
                else:
                    begin = page - 6
                    end = page + 5
        for i in range(int(begin),int(end)):
            print(i,'range')
            if page == i + 1:
                print(page,)
                a_html = "<li class='active'><a href='javascript:void(0)' onclick='ChangePage(%d)'>%d</a></li>" \
                         %(i +1 ,i+1,)
                print(a_html,3)
            else:
                a_html = "<li><a href='javascript:void(0)' onclick='ChangePage(%d)'>%d</a></li>" %(i+1,i+1,)
            page_html.append(a_html)

        if page + 1 > all_page_count:
            next_html = "<li class='disabled'><a href='javascript:void(0)'>下一页</a></li>"
        else:
            next_html = "<li><a href='javascript:void(0)' onclick='ChangePage(%d)'>下一页</a></li>" %(page + 1,)
        page_html.append(next_html)

        end_html = "<li><a href='javascript:void(0)'onclick='ChangePage(%d)'>尾页</a></li>" %(self.total_page,)
        page_html.append(end_html)

        end_html = "<li><a href='javascript:void(0)'>共%d页/%d 条数据</a></li>" %(all_page_count,total_items,)
        page_html.append(end_html)

        page_string = mark_safe(''.join(page_html))
        return page_string


