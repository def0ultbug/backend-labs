from fastapi import APIRouter, HTTPException,Path,Query
from schemas.Book import Book,BookCreate,BookUpdate
from db import db

router = APIRouter(
    prefix="/Books",
)

#show all the Books
@router.get("/")
async def get_all()->dict[str,dict]:
    return {"Books" : db.Books}


@router.post("/",status_code=201)
async def add_book(new_book : BookCreate)->dict[str,Book]:
    # Check if a book with the same name already exists
    for book in db.Books.values():
        if book.title.lower() == new_book.title.lower():
            raise HTTPException(
                status_code=400,
                detail="Book already exists.",
            )
    #Generate ID
    new_id = len(db.Books) + 1

    #Create instance of Books BaseModel
    book = Book(id=new_id, **new_book.model_dump())
    db.Books[new_id] = book
    return {"added" : book}

@router.get('/{id_book}')
async def get_book_by_id(id_book : int)-> Book:
    if id_book not in db.Books:
        raise HTTPException(
                status_code=400,
                detail="Book don't exists.",
            )
    return db.Books[id_book]

@router.delete("/{id}", status_code = 204)
async def delete(id: int)-> None: # None Because there is a Error when return Dict  
    try:
        db.Books.pop(id)
    except KeyError:
        raise HTTPException(
                status_code=400,
                detail="Book don't exists.",
            )

#Update specific field
@router.patch('/{id_book}')
async def Update(
    id_book : int = Path(title="Item ID", description="Unique integer that specifies an item.", ge=0),
    book_data: BookUpdate = Query(...) # Tried Body but Query is better
    )-> dict[str,dict]:
    
    if id_book not in db.Books:
        raise HTTPException(
                status_code=400,
                detail="Book don't exists.",
            )
    # Check if at least one field is provided
    update_data = book_data.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=422,  # 422 = Unprocessable Entity
            detail="No fields to update.",
        )
    
    book = db.Books[id_book]
    for field, value in book_data.model_dump(exclude_unset=True).items():
        setattr(book,field,value) #(list_name,key,value)

    db.Books[id_book] = book
    return {"Book Updated" : book.model_dump()}

