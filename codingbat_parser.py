"""A python project that can parse data from the CodingBat webpages and display questions and examples."""
import requests
from bs4 import BeautifulSoup

# HTML REQUEST
lang = input("What language would you like to use? Java or Python?")
url = "http://codingbat.com/" + lang.strip().lower()
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
x = soup.find_all("tr")
g = [td.div for td in x]
h = [s for s in g if s is not None]
names = [f.span.string for f in h]
# Todo: Here we make buttons for each of these categories and then formulate a new URL
# Todo: A new get request will be made to this URL
# Todo: The new URL can be formulated by the function described below


def _makenewurl(url: str, lst: list) -> str:
    g = 0
    for x in lst:
        print(g, x, end="\n")
        g += 1
    choice = input("Choose the number or the choice you want to do from above: ")
    return url + "/" + lst[int(choice)]


newurl = _makenewurl(url, names)
newresponse = requests.get(newurl)
newsoup = BeautifulSoup(newresponse.text, 'lxml')
thelist = newsoup.find_all("td")
x = [x.a.string for x in thelist if x.a is not None]
y = [x.a["href"] for x in thelist if x.a is not None]
problist = x[2:]
linklist = y[2:]


def _chosenproblem(prblms: list, lnks: list) -> str:
    prelim = "http://codingbat.com"
    for i in range(len(prblms)):
        print(i, "----> ", prblms[i])
        i += 1
    choice = input("choose the problem number from the above choice: ")
    return prelim + lnks[int(choice)]


newnewurl = _chosenproblem(problist, linklist)
newnewresponse = requests.get(newnewurl)
newnewsoup = BeautifulSoup(newnewresponse.text, 'lxml')
x = newnewsoup.find_all("tr")
result1 = [g.td.div.string for g in x if g.td.div is not None]
QUESTION = result1[0]
# TODO: Parse for the examples
g = newnewsoup.find_all("td", {"valign": "top"})
tester = g[1]
lst = tester.children


def _convert_to_list(l: 'list_iterator') -> list:
    newlist = []
    for child in l:
        gh = str(child.encode('utf-8'))
        newlist.append(gh)

    return newlist


def _stringconverter(s: str) -> str:
    if '\\xe2\\x86\\x92' in s:
        t = s.find('\\xe2\\x86\\x92')
        e = s.rfind('x92')
        return s[1:t] + " ---> " + s[e+4:]


examples = _convert_to_list(lst)
FIRST = _stringconverter(examples[2])
SECOND = _stringconverter(examples[4])
THIRD = _stringconverter(examples[6])


def _display_question(a, b, c, d) -> str:
    s = """\n SOLVE THE FOLLOWING QUESTION, EXAMPLES HAVE BEEN PROVIDED TO HELP: \n
    QUESTION: {}
    \n\n
    EXAMPLES:
    {} \n
    {} \n
    {} \n""".format(d, a, b, c)
    return s


print(_display_question(FIRST, SECOND, THIRD, QUESTION))
