"""Unit tests for the Hotel class."""
import json
import os

import pytest

from hotel import Hotel


@pytest.fixture
def hotel_mgr(tmp_path):
    """Return a Hotel manager that uses a temp JSON file."""
    path = str(tmp_path / "hotels.json")
    return Hotel(file_path=path)


# ---------- positive / happy-path tests ----------

class TestCreateHotel:
    """Tests for create_hotel."""

    def test_create_single(self, hotel_mgr):
        result = hotel_mgr.create_hotel("Grand", "NYC", 100)
        assert result is not None
        assert result["name"] == "Grand"
        assert result["hotel_id"] == 1
        assert result["available_rooms"] == 100

    def test_create_multiple_increments_id(self, hotel_mgr):
        hotel_mgr.create_hotel("A", "City A", 10)
        second = hotel_mgr.create_hotel("B", "City B", 20)
        assert second["hotel_id"] == 2

    def test_create_persists_to_file(self, hotel_mgr):
        hotel_mgr.create_hotel("Persisted", "Town", 5)
        with open(hotel_mgr.file_path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        assert len(data) == 1
        assert data[0]["name"] == "Persisted"


class TestDeleteHotel:
    """Tests for delete_hotel."""

    def test_delete_existing(self, hotel_mgr):
        hotel_mgr.create_hotel("Del", "X", 1)
        assert hotel_mgr.delete_hotel(1) is True

    def test_delete_removes_from_file(self, hotel_mgr):
        hotel_mgr.create_hotel("Del", "X", 1)
        hotel_mgr.delete_hotel(1)
        with open(hotel_mgr.file_path, "r", encoding="utf-8") as fh:
            assert json.load(fh) == []


class TestDisplayHotel:
    """Tests for display_hotel_info."""

    def test_display_existing(self, hotel_mgr):
        hotel_mgr.create_hotel("Show", "Here", 3)
        info = hotel_mgr.display_hotel_info(1)
        assert info["name"] == "Show"
        assert info["location"] == "Here"


class TestModifyHotel:
    """Tests for modify_hotel_info."""

    def test_modify_name(self, hotel_mgr):
        hotel_mgr.create_hotel("Old", "Place", 10)
        updated = hotel_mgr.modify_hotel_info(1, name="New")
        assert updated["name"] == "New"

    def test_modify_rooms_adjusts_available(self, hotel_mgr):
        hotel_mgr.create_hotel("H", "P", 10)
        hotel_mgr.reserve_room(1)
        updated = hotel_mgr.modify_hotel_info(1, rooms=15)
        assert updated["rooms"] == 15
        assert updated["available_rooms"] == 14


class TestReserveRoom:
    """Tests for reserve_room."""

    def test_reserve_decrements(self, hotel_mgr):
        hotel_mgr.create_hotel("R", "L", 2)
        assert hotel_mgr.reserve_room(1) is True
        info = hotel_mgr.display_hotel_info(1)
        assert info["available_rooms"] == 1


class TestCancelReservation:
    """Tests for cancel_reservation on Hotel."""

    def test_cancel_increments(self, hotel_mgr):
        hotel_mgr.create_hotel("C", "L", 2)
        hotel_mgr.reserve_room(1)
        assert hotel_mgr.cancel_reservation(1) is True
        info = hotel_mgr.display_hotel_info(1)
        assert info["available_rooms"] == 2


# ---------- negative / error-handling tests ----------

class TestNegativeCases:
    """Negative test cases (>=5 required by rubric)."""

    def test_create_empty_name(self, hotel_mgr):
        assert hotel_mgr.create_hotel("", "NYC", 10) is None

    def test_create_whitespace_name(self, hotel_mgr):
        assert hotel_mgr.create_hotel("   ", "NYC", 10) is None

    def test_create_invalid_rooms_zero(self, hotel_mgr):
        assert hotel_mgr.create_hotel("H", "L", 0) is None

    def test_create_invalid_rooms_negative(self, hotel_mgr):
        assert hotel_mgr.create_hotel("H", "L", -5) is None

    def test_create_rooms_not_int(self, hotel_mgr):
        assert hotel_mgr.create_hotel("H", "L", "ten") is None

    def test_create_empty_location(self, hotel_mgr):
        assert hotel_mgr.create_hotel("H", "", 5) is None

    def test_delete_nonexistent(self, hotel_mgr):
        assert hotel_mgr.delete_hotel(999) is False

    def test_display_nonexistent(self, hotel_mgr):
        assert hotel_mgr.display_hotel_info(999) is None

    def test_modify_nonexistent(self, hotel_mgr):
        assert hotel_mgr.modify_hotel_info(999, name="X") is None

    def test_modify_invalid_field(self, hotel_mgr):
        hotel_mgr.create_hotel("H", "L", 5)
        assert hotel_mgr.modify_hotel_info(1, stars=5) is None

    def test_modify_invalid_name(self, hotel_mgr):
        hotel_mgr.create_hotel("H", "L", 5)
        assert hotel_mgr.modify_hotel_info(1, name="") is None

    def test_modify_invalid_rooms(self, hotel_mgr):
        hotel_mgr.create_hotel("H", "L", 5)
        assert hotel_mgr.modify_hotel_info(1, rooms=-1) is None

    def test_reserve_no_rooms_available(self, hotel_mgr):
        hotel_mgr.create_hotel("H", "L", 1)
        hotel_mgr.reserve_room(1)
        assert hotel_mgr.reserve_room(1) is False

    def test_reserve_nonexistent_hotel(self, hotel_mgr):
        assert hotel_mgr.reserve_room(999) is False

    def test_cancel_nonexistent_hotel(self, hotel_mgr):
        assert hotel_mgr.cancel_reservation(999) is False

    def test_cancel_already_full(self, hotel_mgr):
        hotel_mgr.create_hotel("H", "L", 2)
        assert hotel_mgr.cancel_reservation(1) is False

    def test_load_corrupt_json(self, hotel_mgr):
        os.makedirs(os.path.dirname(hotel_mgr.file_path), exist_ok=True)
        with open(hotel_mgr.file_path, "w", encoding="utf-8") as fh:
            fh.write("{bad json")
        result = hotel_mgr.create_hotel("H", "L", 5)
        assert result is not None
        assert result["hotel_id"] == 1

    def test_load_non_list_json(self, hotel_mgr):
        os.makedirs(os.path.dirname(hotel_mgr.file_path), exist_ok=True)
        with open(hotel_mgr.file_path, "w", encoding="utf-8") as fh:
            json.dump({"not": "a list"}, fh)
        result = hotel_mgr.create_hotel("H", "L", 5)
        assert result is not None

    def test_create_none_name(self, hotel_mgr):
        assert hotel_mgr.create_hotel(None, "L", 5) is None

    def test_create_none_location(self, hotel_mgr):
        assert hotel_mgr.create_hotel("H", None, 5) is None
