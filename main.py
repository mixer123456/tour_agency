from fastapi import FastAPI, status, Query, Path

from schemas import NewTour, SavedTour, TourPrice, DeletedTour
from storage.sqlite_storage_tour import storage

app = FastAPI(
    debug=True,
    title='Tour in Ukraine',
)


@app.post('/', include_in_schema=False)
def index():
    return {'subject': 'Hello!'}


# CRUD

# CREATE
@app.post('/api/tour/', description='create tour', status_code=status.HTTP_201_CREATED, tags=['API', 'Tour'])
def add_tour(new_tour: NewTour) -> SavedTour:
    print(new_tour)
    saved_tour = storage.create_tour(new_tour)
    return saved_tour


# READ
@app.get('/api/tour/', tags=['API', 'Tour'])
def get_tours(
    limit: int = Query(default=10, description='no more than tour', gt=0), q: str = '',
) -> list[SavedTour]:
    result = storage.get_tours(limit=limit, q=q)
    return result


@app.get('/api/tour/{tour_id}', tags=['API', 'Tour'])
def get_tour(tour_id: int = Path(ge=1, description='tour id')) -> SavedTour:
    result = storage.get_tour(tour_id)
    return result


# UPDATE
@app.patch('/api/tour/{tour_id}', tags=['API', 'Tour'])
def update_tour_price(new_price: TourPrice, tour_id: int = Path(ge=1, description='tour id')) -> SavedTour:
    result = storage.update_tour_price(tour_id, new_price=new_price.price)
    return result


# DELETE
@app.delete('/api/tour/{tour_id}', tags=['API', 'Tour'])
def delete_tour_price(tour_id: int = Path(ge=1, description='tour id')) -> DeletedTour:
    storage.delete_tour(tour_id)
    return DeletedTour(id=tour_id)