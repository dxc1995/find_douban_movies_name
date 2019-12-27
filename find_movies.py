import  requests 
from bs4 import BeautifulSoup

# 请求豆瓣网址
def open_url(url):
    headers = {'user-agent':'Mozilla/5.0.html (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.html.963.84 Safari/535.11 SE 2.X MetaSr 1.0.html'}
    res = requests.get(url, headers= headers)
    return res

# 解析html查找豆瓣电影名称
def find_movies(res):
    soup = BeautifulSoup(res.text, "html.parser")
    
    # 电影名
    movies = []
    targets = soup.find_all("div", class_="hd") 
    for each in targets:
        movies.append(each.a.span.text)
    # 评分
    ranks = []
    targets = soup.find_all("span", class_="rating_num")
    for each in targets:
        ranks.append("评分: %s" % each.text)
    # 资料
    messages = []
    targets = soup.find_all("div", class_="bd")
    for each in targets:
        try:
            messages.append(each.p.text.split("\n")[1].strip("\n")[1].strip() + each.p.text.split("\n")[2].strip())
        except:
            continue
    
    result = []
    length = len(movies)
    for i in range(length):
        result.append(movies[i] + "\t" + ranks[i] + "\t" + messages[i] + "\n")
    return result

    # 找出一共有多少个页面
def find_depth(res):
    soup = BeautifulSoup(res.text, "html.parser")
    depth = soup.find("span", class_="next").previous_sibling.previous_sibling.text
    return int(depth)

def main():
    host = "https://movie.douban.com/top250"
    res  = open_url(host)
    depth = find_depth(res)

    result = []

    for i in range(depth):
        url = host + "/?start=" +str(25 * i)
        res = open_url(url)
        result.extend(find_movies(res))
    
    with open("豆瓣电影Top250电影.txt", "w", encoding="utf-8") as f:
        for each in result:
            f.write(each)

if __name__ == "__main__":
    main()





    



    
    