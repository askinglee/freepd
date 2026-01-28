import requests

def push_to_baidu(urls):
    """
    将 URL 列表推送到百度搜索资源平台。
    """
    api_url = "http://data.zz.baidu.com/urls?site=https://freepd.cn&token=M36TxpkZpQ8WKavs"
    
    # 将列表转换为换行符分隔的字符串
    data = "\n".join(urls)
    
    headers = {
        "Content-Type": "text/plain"
    }
    
    try:
        response = requests.post(api_url, data=data, headers=headers)
        response.raise_for_status() # 检查请求是否成功
        
        # 解析返回结果
        result = response.json()
        print("推送成功！")
        print(f"成功推送数量: {result.get('success', 0)}")
        print(f"今日剩余配额: {result.get('remain', 0)}")
        
        if 'not_same_site' in result:
            print(f"由于不是本站地址而未导入的 URL: {result['not_same_site']}")
        if 'not_valid' in result:
            print(f"无效的 URL: {result['not_valid']}")
            
    except requests.exceptions.HTTPError as e:
        print(f"请求发生错误: {e}")
        try:
            # 百度通常会在错误时也返回 JSON 描述
            error_info = response.json()
            print(f"详细错误信息: {error_info}")
        except:
            pass
    except Exception as e:
        print(f"发生意外错误: {e}")

if __name__ == "__main__":
    # 在这里填写你想要推送的 URL
    urls_to_push = [
        'https://freepd.cn/fonts/alibaba-puhuiti/',
        'https://freepd.cn/fonts/harmonyos-sans/',
    ]
    
    push_to_baidu(urls_to_push)
