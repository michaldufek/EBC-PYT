from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Book(BaseModel):
    id: int
    title: str
    author: str
    published_year: int

books = [
    Book(id=1, title="1984", author="George Orwell", published_year=1949),
    Book(id=2, title="To Kill a Mockingbird", author="Harper Lee", published_year=1960),
    Book(id=3, title="The Great Gatsby", author="F. Scott Fitzgerald", published_year=1925)
]

@app.get("/")
def read_root():
    return {"message": "Welcome to the Book Management API"}

@app.get("/books", response_model=List[Book])
def get_books():
    return books

@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    book = next((book for book in books if book.id == book_id), None)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.post("/books", response_model=Book)
def add_book(book: Book):
    if any(b.id == book.id for b in books):
        raise HTTPException(status_code=400, detail="Book with this ID already exists")
    books.append(book)
    return book

@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, updated_book: Book):
    for idx, current_book in enumerate(books):
        if current_book.id == book_id:
            books[idx] = updated_book
            return updated_book
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{book_id}", response_model=Book)
def delete_book(book_id: int):
    for idx, book in enumerate(books):
        if book.id == book_id:
            return books.pop(idx)
    raise HTTPException(status_code=404, detail="Book not found")

# Serve the favicon
@app.get("/favicon.ico")
def favicon():
    return FileResponse("favicon.ico")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
