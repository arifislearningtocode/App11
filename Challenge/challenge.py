import pandas
from fpdf import FPDF


df = pandas.read_csv("articles.csv", dtype={"id": str})
print(df)


class Articles:

    def __init__(self, article_id):
        self.article_id = article_id
        self.name = df.loc[df['id'] == self.article_id, 'name'].squeeze()
        self.price = df.loc[df['id'] == self.article_id, 'price'].squeeze()

    def available(self):
        in_stock = df.loc[df['id'] == self.article_id, 'in stock'].squeeze() > 0
        return in_stock

    def remove(self):
        df.loc[df['id'] == self.article_id, 'in stock'] -= 1
        df.to_csv("articles.csv", index=False)


class PrintPDF:

    def __init__(self, article):
        self.article = article

    def pdfprint(self):
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Receipt nr.{self.article.article_id}", ln=1)

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Article: {self.article.name}", ln=1)

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Price: {self.article.price}", ln=1)

        pdf.output("receipt.pdf")


article_index = input("Choose an article to buy: ")
article = Articles(article_index)
if article.available():
    receipt = PrintPDF(article)
    receipt.pdfprint()
    article.remove()
else:
    print("No such article exists")

