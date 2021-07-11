导出不蒜子的访问数据，并采用json格式存储到文件中。更多信息请见[导出不蒜子的访问量数据](https://pkemb.com/2021/07/export-busuanzi-data/)。

json数据的格式如下：

```json
{
    "page_puv_statistics": [
        {
            "time": "yyyy-mm-dd HH:MM:SS.ms"
            "page_puv": [
                {
                    "url": "url",
                    "site_uv": xx,
                    "page_pv": xx,
                    "site_pv": xx
                },
            ],
        }
    ]
}
```

