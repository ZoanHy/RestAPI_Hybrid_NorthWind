import requests
from bs4 import BeautifulSoup, Tag

URL = "https://www.w3schools.com/sql/trysql.asp?filename=trysql_select_all"

#! get customer data


def get_list_objects(filename):
    with open(f"./data_html/{filename}.html", "r", encoding="utf8") as file:
        soup = BeautifulSoup(file, "html.parser")

    list_tr = soup.select(selector="tr")
    list_td = list_tr[0]
    list_data = [list_tr[index] for index in range(len(list_tr)) if index != 0]

    list_objects = []
    for i in range(len(list_data)):
        cus = []
        list_td = list_data[i].select(selector="td")
        for j in range(len(list_td)):
            if j != 0:
                value = list_td[j].getText()
                cus.append(value)
        list_objects.append(cus)
    return list_objects


#! get employee data
