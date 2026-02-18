"""Hotel module with JSON persistence."""
import os

from base_manager import BaseManager


class Hotel(BaseManager):
    """Manages hotel records with JSON file persistence."""

    DEFAULT_FILE = os.path.join("data", "hotels.json")

    def __init__(self, file_path=None):
        super().__init__(file_path, self.DEFAULT_FILE)

    def create_hotel(self, name, location, rooms):
        """Create a new hotel and persist it.

        Returns the created hotel dict or None on validation error.
        """
        if not name or not isinstance(name, str) or not name.strip():
            print("Error: Hotel name must be a non-empty string.")
            return None
        if not location or not isinstance(location, str) \
                or not location.strip():
            print("Error: Location must be a non-empty string.")
            return None
        if not isinstance(rooms, int) or rooms <= 0:
            print("Error: Rooms must be a positive integer.")
            return None

        hotels = self._load()
        new_hotel = {
            "hotel_id": self._next_id(hotels, "hotel_id"),
            "name": name.strip(),
            "location": location.strip(),
            "rooms": rooms,
            "available_rooms": rooms,
        }
        hotels.append(new_hotel)
        self._save(hotels)
        return new_hotel

    def delete_hotel(self, hotel_id):
        """Delete a hotel by its id.

        Returns True if deleted, False otherwise.
        """
        hotels = self._load()
        original_len = len(hotels)
        hotels = [h for h in hotels if h["hotel_id"] != hotel_id]
        if len(hotels) == original_len:
            print(f"Error: Hotel with id {hotel_id} not found.")
            return False
        self._save(hotels)
        return True

    def display_hotel_info(self, hotel_id):
        """Return hotel dict for the given id, or None if not found."""
        hotels = self._load()
        for hotel in hotels:
            if hotel["hotel_id"] == hotel_id:
                return hotel
        print(f"Error: Hotel with id {hotel_id} not found.")
        return None

    def modify_hotel_info(self, hotel_id, **kwargs):
        """Modify hotel attributes.

        Allowed keys: name, location, rooms.
        Returns the updated hotel dict or None on error.
        """
        if not self._validate_modify_kwargs(kwargs):
            return None

        hotels = self._load()
        for hotel in hotels:
            if hotel["hotel_id"] == hotel_id:
                self._apply_updates(hotel, kwargs)
                self._save(hotels)
                return hotel

        print(f"Error: Hotel with id {hotel_id} not found.")
        return None

    def _validate_modify_kwargs(self, kwargs):
        """Validate keyword arguments for modify_hotel_info."""
        allowed = {"name", "location", "rooms"}
        invalid_keys = set(kwargs.keys()) - allowed
        if invalid_keys:
            print(f"Error: Invalid fields: {invalid_keys}")
            return False
        if "name" in kwargs:
            val = kwargs["name"]
            if not val or not isinstance(val, str) or not val.strip():
                print("Error: Hotel name must be a non-empty string.")
                return False
        if "location" in kwargs:
            val = kwargs["location"]
            if not val or not isinstance(val, str) or not val.strip():
                print("Error: Location must be a non-empty string.")
                return False
        if "rooms" in kwargs:
            if not isinstance(kwargs["rooms"], int) \
                    or kwargs["rooms"] <= 0:
                print("Error: Rooms must be a positive integer.")
                return False
        return True

    @staticmethod
    def _apply_updates(hotel, kwargs):
        """Apply validated updates to a hotel dict."""
        if "name" in kwargs:
            hotel["name"] = kwargs["name"].strip()
        if "location" in kwargs:
            hotel["location"] = kwargs["location"].strip()
        if "rooms" in kwargs:
            diff = kwargs["rooms"] - hotel["rooms"]
            hotel["rooms"] = kwargs["rooms"]
            hotel["available_rooms"] = max(
                0, hotel["available_rooms"] + diff
            )

    def reserve_room(self, hotel_id):
        """Decrease available rooms by one.

        Returns True on success, False if no rooms or not found.
        """
        hotels = self._load()
        for hotel in hotels:
            if hotel["hotel_id"] == hotel_id:
                if hotel["available_rooms"] <= 0:
                    print("Error: No available rooms.")
                    return False
                hotel["available_rooms"] -= 1
                self._save(hotels)
                return True
        print(f"Error: Hotel with id {hotel_id} not found.")
        return False

    def cancel_reservation(self, hotel_id):
        """Increase available rooms by one (room freed).

        Returns True on success, False if not found or already full.
        """
        hotels = self._load()
        for hotel in hotels:
            if hotel["hotel_id"] == hotel_id:
                if hotel["available_rooms"] >= hotel["rooms"]:
                    print("Error: All rooms are already available.")
                    return False
                hotel["available_rooms"] += 1
                self._save(hotels)
                return True
        print(f"Error: Hotel with id {hotel_id} not found.")
        return False
