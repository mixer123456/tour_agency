from abc import ABC, abstractmethod
import sqlite3

from fastapi import HTTPException, status

from schemas import NewTour, SavedTour
from storage.base_storage_tour import BaseStorageTour


class StorageSQLite(BaseStorageTour):

    def __init__(self, database_name: str):
        self.database_name = database_name
        self.tour_table_name = 'tours'
        self._create_table()

    def _create_table(self):
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            query = f"""
                CREATE TABLE IF NOT EXISTS {self.tour_table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    description TEXT,
                    price REAL,
                    cover TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP 
                )
            """
            cursor.execute(query)

    def create_tour(self, new_tour: NewTour) -> SavedTour:
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            values = (new_tour.title, new_tour.description, new_tour.price, str(new_tour.cover))
            query = f"""
                INSERT INTO {self.tour_table_name} (title, description, price, cover)
                VALUES (?, ?, ?, ?)
            """
            cursor.execute(query, values)
        return self._get_latest_tour()

    def _get_latest_tour(self) -> SavedTour:
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            query = f"""
                SELECT id, title, description, price, cover, created_at
                FROM {self.tour_table_name}
                ORDER BY id DESC
                LIMIT 1
            """
            result: tuple = cursor.execute(query).fetchone()
            id, title, description, price, cover, created_at = result
            saved_tour = SavedTour(
                id=id, title=title, description=description, price=price, cover=cover, created_at=created_at
            )

            return saved_tour

    def get_tour(self, _id: int) -> SavedTour:
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            query = f"""
                SELECT id, title, description, price, cover, created_at
                FROM {self.tour_table_name}
                WHERE id = {_id}
            """
            result: tuple = cursor.execute(query).fetchone()
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=f'Check your entity id, tour with {_id=} not found'
                )

            id, title, description, price, cover, created_at = result
            saved_tour = SavedTour(
                id=id, title=title, description=description, price=price, cover=cover, created_at=created_at
            )

            return saved_tour

    def get_tours(self, limit: int = 10, q: str = '') -> list[SavedTour]:
        list_of_tours = []

        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            query = f"""
                SELECT id, title, description, price, cover, created_at
                FROM {self.tour_table_name}
                WHERE title LIKE '%{q}%' OR description LIKE '%{q}%'
                ORDER BY id DESC
                LIMIT {limit}
            """
            data: list[tuple] = cursor.execute(query).fetchall()

            for result in data:
                id, title, description, price, cover, created_at = result

                saved_tour = SavedTour(
                    id=id,
                    title=title,
                    description=description[:30],
                    price=price,
                    cover=cover,
                    created_at=created_at
                )

                list_of_tours.append(saved_tour)
        return list_of_tours

    def update_tour_price(self, _id: int, new_price: float) -> SavedTour:
        self.get_tour(_id)

        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            query = f"""
                        UPDATE {self.tour_table_name}
                        SET
                            price = :Price
                        WHERE id = :Id
                    """
            cursor.execute(query, {'Price': new_price, 'Id': _id})

        saved_tour = self.get_tour(_id)
        return saved_tour

    def delete_tour(self, _id: int):
        self.get_tour(_id)
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            query = f"""
                                DELETE FROM {self.tour_table_name}
                                WHERE id = :Id
                    """
            cursor.execute(query, {'Id': _id})


storage = StorageSQLite('database/tours.sqlite')
