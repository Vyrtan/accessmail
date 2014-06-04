__author__ = 'Vyrtan'

class addressbook():
    global book

    book = []

    def add(self, a):
        book.append(self, a)

    def remove(self, n):
        book.remove(self, n)

    def get(self, x, y):
        return book[x:y]
