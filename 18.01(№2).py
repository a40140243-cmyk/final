import requests
from bs4 import BeautifulSoup as bs

# class ProductParser:
#     def __init__(self, url):
#         self.url = url
#         self.header = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
#             'Accept-Language': 'uk-UA,uk;q=0.9'
#         }
#         self.soup = None
#         self.products = []
#
#     def auditSite(self):
#         try:
#             r = requests.get(self.url, headers=self.header, timeout=10)
#             if r.status_code == 200:
#                 self.soup = bs(r.text, "html.parser")
#             else:
#                 print("Не вдалося підключитися до сайту")
#                 self.soup = None
#         except Exception as e:
#             print("Помилка з'єднання:", e)
#             self.soup = None
#
#     def getInfo(self):
#         if not self.soup:
#             print("Сайт не завантажено")
#             return []
#
#         products = []
#
#         items = self.soup.select("article.product_pod")[:10]
#
#         def clean_number(text):
#
#             text = (text or "").strip()
#             num, dot = "", False
#             for ch in text:
#                 if ch.isdigit():
#                     num += ch
#                 elif ch == '.' and not dot:
#                     num += ch
#                     dot = True
#             try:
#                 return int(float(num))
#             except:
#                 return 0
#
#         for it in items:
#             name_tag = it.select_one("h3 a")
#             price_tag = it.select_one("p.price_color")
#
#             name = name_tag.get("title", "").strip() if name_tag else "Назва відсутня"
#             price = clean_number(price_tag.get_text()) if price_tag else 0
#
#             products.append({"name": name, "price": price})
#
#         self.products = products
#         return self.products
#
#     def showInfo(self, products):
#         print("\nТОП-10 товарів:\n")
#         for i, p in enumerate(products, start=1):
#             print(f"{i}. {p['name']} – {p['price']} грн")
#
#     def buy(self, products):
#         order, total = [], 0
#         while True:
#             try:
#                 print("\nЯкий товар ви хочете придбати? (введіть номер):")
#                 choice = int(input("> ")) - 1
#                 if choice < 0 or choice >= len(products):
#                     print("Невірний номер")
#                     continue
#                 product = products[choice]
#                 print("Скільки одиниць ви хочете купити?:")
#                 qty = int(input("> "))
#                 if qty <= 0:
#                     print("Кількість має бути більшою за 0")
#                     continue
#             except:
#                 print("Невірний ввід")
#                 continue
#
#             sum_price = product['price'] * qty
#             order.append(f"- {product['name']} x{qty} = {sum_price} грн")
#             total += sum_price
#
#             print("Хочете ще щось? (так/ні):")
#             if input("> ").strip().lower() != "так":
#                 break
#
#         print("\nВаше замовлення:")
#         for o in order:
#             print(o)
#         print(f"\nЗагальна сума до сплати: {total} грн")
#
# url = "https://books.toscrape.com/catalogue/category/books_1/index.html"
# obj = ProductParser(url)
# obj.auditSite()
# site = obj.getInfo()
# if site:
#     obj.showInfo(site)
#     obj.buy(site)
# else:
#     print("Жодної інформації не отримано з сайту")


#завдання 2


import requests
from bs4 import BeautifulSoup as bs

class MinfinCurrency:
    def __init__(self, url):
        self.url = url
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
        self.soup = None

    def auditSite(self):
        response = requests.get(self.url, headers=self.header)
        if response.status_code == 200:
            self.soup = bs(response.text, "html.parser")
        else:
            print("Не вдалося підключитися до сайту")

    def getInfo(self):
        Currency = []
        table = self.soup.find_all('tr', class_="sc-1x32wa2-4 dKDsVV")

        if not table:
            print("Не вдалося знайти таблицю валют")
            return Currency

        for i in table[1:6]:
            nameCurrency = i.find("a", class_="sc-1x32wa2-7 ciClTw")
            name = nameCurrency.text.strip() if nameCurrency else "?"

            price = i.find_all("td")

            def clean_number(text):
                text = text.replace(',', '.').strip()
                text = text.split()[0]
                result = ""
                dot_used = False

                for ch in text:
                    if ch.isdigit():
                        result += ch
                    elif ch == '.' and not dot_used:
                        result += ch
                        dot_used = True
                    else:
                        break

                return round(float(result), 2) if result else 0.0

            purchase = clean_number(price[1].text)
            sales = clean_number(price[2].text)

            Currency.append({
                "name": name,
                "buy": purchase,
                "sell": sales
            })

        return Currency

    def showInfo(self, currency):
        index = 1
        print('\nОтримані курси валют:\n')
        for i in currency:
            print(f'{index}. {i["name"]}: Купівля – {i["buy"]} грн, Продаж – {i["sell"]} грн')
            index += 1

    def convert(self, currency):
        print("\nВиберіть дію:\n1 – Купити\n2 – Продати")
        action = input("> ")

        print("\nВиберіть валюту (введіть номер зі списку):")
        currency_index = int(input("> ")) - 1

        print("\nВведіть суму у гривнях:")
        amount = float(input("> "))

        if action == '1':
            rate = currency[currency_index]['sell']
            result = round(amount / rate, 2)
            print(f"\nВи хочете купити {currency[currency_index]['name']} на {amount} грн.")
            print(f"Ви отримаєте: {result} {currency[currency_index]['name']} за курсом {rate} грн.")
        elif action == '2':
            rate = currency[currency_index]['buy']
            result = round(amount / rate, 2)
            print(f"\nВи хочете продати {currency[currency_index]['name']} на {amount} грн.")
            print(f"Ви отримаєте: {result} {currency[currency_index]['name']} за курсом {rate} грн.")
        else:
            print("Невірна дія")


url = "https://minfin.com.ua/ua/currency/"
obj = MinfinCurrency(url)
obj.auditSite()
site = obj.getInfo()
if site:
    obj.showInfo(site)
    obj.convert(site)
else:
    print("Жодної інформації не отримано з сайту")