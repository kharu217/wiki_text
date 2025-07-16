import bs4
from bs4 import BeautifulSoup
import requests
import re
from tqdm import tqdm
from multiprocessing import Pool, freeze_support
import parmap
import time

is_first = True
strain = bs4.SoupStrainer("p")
page_count = 18066

def get_re(url) :
    result_t = ""
    while True :
        try :
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "lxml",parse_only=bs4.SoupStrainer("p"))
            break
        except KeyboardInterrupt :
            raise KeyboardInterrupt
        except :
            continue
    #find paragraph of main page
    for del_tag in soup.find_all("sup", class_="reference") :
        del_tag.decompose()
    for del_tag in soup.find_all("math") :
        del_tag.decompose()
    for txt in soup.select("p", role="paragraph") :
        result_t += txt.get_text()
    return result_t

if __name__ == "__main__" :
    freeze_support()
    page_url = 'https://en.wikipedia.org/wiki/Special:AllPages?from=Folksworth_and_Washingley&to=&namespace=0'
    while page_url != "https://en.wikipedia.org/wiki/Special:AllPages/0" or is_first:
        start = time.time()
        page_count += 1
        is_first = False
        page_response = requests.get(page_url)
        page_soup = BeautifulSoup(page_response.text, "lxml")

        sub_url_l = page_soup.select('div .mw-allpages-body li>a')
        raw_text = ""
        with open("wiki_cxk_point.txt","w+", encoding="utf-8") as p :
            p.write(str(page_count)+"\n")
            main_url = []
            for prgraph_url in sub_url_l :
                main_url.append("https://en.wikipedia.org/" + prgraph_url["href"])
                p.write(main_url[-1]+"\n")

        with open(f"Wikitext\\wiki{page_count}.txt", 'w+', encoding="utf-8") as f :
            for result in parmap.map(get_re, main_url ,pm_pbar=True, pm_processes=10) :
                f.write(result)
            time.sleep(0.01)
        print(f"{time.time()-start}s")
        page_url = "https://en.wikipedia.org" + page_soup.find_all('a', title="Special:AllPages")[1]["href"]
=======
import bs4
from bs4 import BeautifulSoup
import requests
import re
from tqdm import tqdm

is_first = True
strain = bs4.SoupStrainer("p")
page_count = 0

def get_re(url) :
    while True :
        try :
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "lxml",parse_only=bs4.SoupStrainer("p"))
            return soup
        except KeyboardInterrupt :
            raise KeyboardInterrupt
        except :
            continue


page_url = "https://en.wikipedia.org/wiki/Special:AllPages/0"
while page_url != "https://en.wikipedia.org/wiki/Special:AllPages/0" or is_first:
    page_count += 1
    is_first = False
    page_response = requests.get(page_url)
    page_soup = BeautifulSoup(page_response.text, "lxml")

    sub_url_l = page_soup.select('div .mw-allpages-body li>a')
    raw_text = ""
    with open("wiki_cxk_point.txt","w+", encoding="utf-8") as p :
        with open(f".\\Wikitext\\wiki{page_count}.txt", 'w+', encoding="utf-8") as f :
            p.write(str(page_count)+"\n")
            for prgraph_url in tqdm(sub_url_l) :
                main_url ="https://en.wikipedia.org/" + prgraph_url["href"]
                p.write(main_url+"\n")
                main_soup = get_re(main_url)

                #find paragraph of main page
                for del_tag in main_soup.find_all("sup", class_="reference") :
                    del_tag.decompose()
                for del_tag in main_soup.find_all("math") :
                    del_tag.decompose()
                prgraph = main_soup.select("p", role="paragraph")
                for txt in prgraph :
                    f.write(txt.get_text())
            page_url = "https://en.wikipedia.org" + page_soup.find_all('a', title="Special:AllPages")[1]["href"]
f.close()  
p.close()
