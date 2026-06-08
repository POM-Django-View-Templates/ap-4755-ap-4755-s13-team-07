from django.db import models
from author.models import Author


class Book(models.Model):
    name = models.CharField(max_length=128, default="")
    description = models.TextField(default="", blank=True)
    count = models.IntegerField(default=10)
    authors = models.ManyToManyField(Author, blank=True, related_name="books")

    class Meta:
        ordering = ["id"]

    def __str__(self):
        authors = ", ".join([str(author) for author in self.authors.all()])
        return f"{self.id} {self.name} {self.description} {self.count} {authors}"

    def __repr__(self):
        return f"Book(id={self.id})"

    @staticmethod
    def get_by_id(book_id):
        try:
            return Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return None

    @staticmethod
    def delete_by_id(book_id):
        book = Book.get_by_id(book_id)
        if book:
            book.delete()
            return True
        return False

    @staticmethod
    def create(name, description, count=10, authors=None):
        book = Book(name=name, description=description, count=count)
        book.save()

        if authors:
            book.authors.set(authors)

        return book

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "count": self.count,
            "authors": [author.id for author in self.authors.all()],
        }

    def update(self, name=None, description=None, count=None):
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if count is not None:
            self.count = count

        self.save()

    def add_authors(self, authors):
        self.authors.add(*authors)
        self.save()

    def remove_authors(self, authors):
        self.authors.remove(*authors)
        self.save()

    @staticmethod
    def get_all():
        return Book.objects.all()