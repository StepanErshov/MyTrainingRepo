from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Book(BaseModel):
    id: int
    title: str
    author: str

books_db = [
    Book(id=1, title="Python для начинающих", author="Иван Иванов"),
    Book(id=2, title="Продвинутый Python", author="Петр Петров"),
    Book(id=3, title="ML for ALL", author="Рамзан Хациев")
]

@app.get("/books/", response_model=List[Book], status_code=202)
async def get_books():
    books_db.sort(key=lambda book: book.id)
    return books_db

@app.get("/books/{book_id}", response_model=Book, status_code=200)
async def read_book(book_id: int):
    for book in books_db:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.post("/books/", response_model=Book, status_code=201)
async def create_book(book: Book):
    books_db.append(book)
    return book


@app.delete("/books/{book_id}", status_code=204)
async def del_book(book_id: int):
    for i, book in enumerate(books_db):
        if book.id == book_id:
            del books_db[i]
            return
    raise HTTPException(status_code=404, detail="Book not found")

@app.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: int, updated_book: Book):
    
    if updated_book.id != book_id:
        raise HTTPException(status_code=400, detail="ID in URL and body must match")

    for i, book in enumerate(books_db):
        if book.id == book_id:
            books_db[i] = updated_book
            return updated_book
    
    raise HTTPException(status_code=404, detail="Book not found")
