import requests
from bs4 import BeautifulSoup as bs

class ProductParser:
    def __init__(self, url):
        self.url = url
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Accept-Language': 'uk-UA,uk;q=0.9'
        }
        self.soup = None
        self.products = []

    def auditSite(self):
        try:
            r = requests.get(self.url, headers=self.header, timeout=10)
            if r.status_code == 200:
                self.soup = bs(r.text, "html.parser")
            else:
                print("Не вдалося підключитися до сайту")
                self.soup = None
        except Exception as e:
            print("Помилка з'єднання:", e)
            self.soup = None

    def getInfo(self):
        if not self.soup:
            print("Сайт не завантажено")
            return []

        products = []

        items = self.soup.select("article.product_pod")[:10]

        def clean_number(text):

            text = (text or "").strip()
            num, dot = "", False
            for ch in text:
                if ch.isdigit():
                    num += ch
                elif ch == '.' and not dot:
                    num += ch
                    dot = True
            try:
                return int(float(num))
            except:
                return 0

        for it in items:
            name_tag = it.select_one("h3 a")
            price_tag = it.select_one("p.price_color")

            name = name_tag.get("title", "").strip() if name_tag else "Назва відсутня"
            price = clean_number(price_tag.get_text()) if price_tag else 0

            products.append({"name": name, "price": price})

        self.products = products
        return self.products

    def showInfo(self, products):
        print("\nТОП-10 товарів:\n")
        for i, p in enumerate(products, start=1):
            print(f"{i}. {p['name']} – {p['price']} грн")

    def buy(self, products):
        order, total = [], 0
        while True:
            try:
                print("\nЯкий товар ви хочете придбати? (введіть номер):")
                choice = int(input("> ")) - 1
                if choice < 0 or choice >= len(products):
                    print("Невірний номер")
                    continue
                product = products[choice]
                print("Скільки одиниць ви хочете купити?:")
                qty = int(input("> "))
                if qty <= 0:
                    print("Кількість має бути більшою за 0")
                    continue
            except:
                print("Невірний ввід")
                continue

            sum_price = product['price'] * qty
            order.append(f"- {product['name']} x{qty} = {sum_price} грн")
            total += sum_price

            print("Хочете ще щось? (так/ні):")
            if input("> ").strip().lower() != "так":
                break

        print("\nВаше замовлення:")
        for o in order:
            print(o)
        print(f"\nЗагальна сума до сплати: {total} грн")

url = "https://books.toscrape.com/catalogue/category/books_1/index.html"
obj = ProductParser(url)
obj.auditSite()
site = obj.getInfo()
if site:
    obj.showInfo(site)
    obj.buy(site)
else:
    print("Жодної інформації не отримано з сайту")
