"""Reservation module with JSON persistence."""
import os

from base_manager import BaseManager
from hotel import Hotel
from customer import Customer


class Reservation(BaseManager):
    """Manages reservation records with JSON file persistence."""

    DEFAULT_FILE = os.path.join("data", "reservations.json")

    def __init__(self, file_path=None, hotel_file=None,
                 customer_file=None):
        super().__init__(file_path, self.DEFAULT_FILE)
        self.hotel_mgr = Hotel(file_path=hotel_file)
        self.customer_mgr = Customer(file_path=customer_file)

    def create_reservation(self, customer_id, hotel_id):
        """Create a reservation for a customer at a hotel.

        Validates that both customer and hotel exist, and that
        a room is available. Returns the reservation dict or None.
        """
        customer = self.customer_mgr.display_customer_info(customer_id)
        if customer is None:
            print(
                f"Error: Cannot reserve — customer "
                f"{customer_id} not found."
            )
            return None

        hotel = self.hotel_mgr.display_hotel_info(hotel_id)
        if hotel is None:
            print(
                f"Error: Cannot reserve — hotel "
                f"{hotel_id} not found."
            )
            return None

        if not self.hotel_mgr.reserve_room(hotel_id):
            return None

        reservations = self._load()
        new_reservation = {
            "reservation_id": self._next_id(
                reservations, "reservation_id"
            ),
            "customer_id": customer_id,
            "hotel_id": hotel_id,
        }
        reservations.append(new_reservation)
        self._save(reservations)
        return new_reservation

    def cancel_reservation(self, reservation_id):
        """Cancel a reservation and free the hotel room.

        Returns True if cancelled, False otherwise.
        """
        reservations = self._load()
        target = None
        for res in reservations:
            if res["reservation_id"] == reservation_id:
                target = res
                break

        if target is None:
            print(
                f"Error: Reservation with id "
                f"{reservation_id} not found."
            )
            return False

        self.hotel_mgr.cancel_reservation(target["hotel_id"])
        reservations = [
            r for r in reservations
            if r["reservation_id"] != reservation_id
        ]
        self._save(reservations)
        return True
