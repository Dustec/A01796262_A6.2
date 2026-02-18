"""Unit tests for the Reservation class."""
import json
import os

import pytest

from reservation import Reservation


@pytest.fixture
def res_mgr(tmp_path):
    """Return a Reservation manager with temp JSON files."""
    return Reservation(
        file_path=str(tmp_path / "reservations.json"),
        hotel_file=str(tmp_path / "hotels.json"),
        customer_file=str(tmp_path / "customers.json"),
    )


def _seed(res_mgr):
    """Create a hotel and customer for reservation tests."""
    res_mgr.hotel_mgr.create_hotel("Plaza", "Downtown", 5)
    res_mgr.customer_mgr.create_customer("Ana", "ana@mail.com")


# ---------- positive / happy-path tests ----------

class TestCreateReservation:
    """Tests for create_reservation."""

    def test_create_single(self, res_mgr):
        _seed(res_mgr)
        result = res_mgr.create_reservation(
            customer_id=1, hotel_id=1
        )
        assert result is not None
        assert result["reservation_id"] == 1
        assert result["customer_id"] == 1
        assert result["hotel_id"] == 1

    def test_create_decrements_room(self, res_mgr):
        _seed(res_mgr)
        res_mgr.create_reservation(1, 1)
        hotel = res_mgr.hotel_mgr.display_hotel_info(1)
        assert hotel["available_rooms"] == 4

    def test_create_multiple(self, res_mgr):
        _seed(res_mgr)
        res_mgr.create_reservation(1, 1)
        second = res_mgr.create_reservation(1, 1)
        assert second["reservation_id"] == 2

    def test_create_persists_to_file(self, res_mgr):
        _seed(res_mgr)
        res_mgr.create_reservation(1, 1)
        with open(res_mgr.file_path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        assert len(data) == 1


class TestCancelReservation:
    """Tests for cancel_reservation."""

    def test_cancel_existing(self, res_mgr):
        _seed(res_mgr)
        res_mgr.create_reservation(1, 1)
        assert res_mgr.cancel_reservation(1) is True

    def test_cancel_frees_room(self, res_mgr):
        _seed(res_mgr)
        res_mgr.create_reservation(1, 1)
        res_mgr.cancel_reservation(1)
        hotel = res_mgr.hotel_mgr.display_hotel_info(1)
        assert hotel["available_rooms"] == 5

    def test_cancel_removes_from_file(self, res_mgr):
        _seed(res_mgr)
        res_mgr.create_reservation(1, 1)
        res_mgr.cancel_reservation(1)
        with open(res_mgr.file_path, "r", encoding="utf-8") as fh:
            assert json.load(fh) == []


# ---------- negative / error-handling tests ----------

class TestNegativeCases:
    """Negative test cases for Reservation."""

    def test_create_nonexistent_customer(self, res_mgr):
        res_mgr.hotel_mgr.create_hotel("H", "L", 5)
        assert res_mgr.create_reservation(999, 1) is None

    def test_create_nonexistent_hotel(self, res_mgr):
        res_mgr.customer_mgr.create_customer("C", "c@m.com")
        assert res_mgr.create_reservation(1, 999) is None

    def test_create_no_rooms_available(self, res_mgr):
        res_mgr.hotel_mgr.create_hotel("H", "L", 1)
        res_mgr.customer_mgr.create_customer("C", "c@m.com")
        res_mgr.create_reservation(1, 1)
        assert res_mgr.create_reservation(1, 1) is None

    def test_cancel_nonexistent(self, res_mgr):
        assert res_mgr.cancel_reservation(999) is False

    def test_create_both_nonexistent(self, res_mgr):
        assert res_mgr.create_reservation(999, 888) is None

    def test_load_corrupt_json(self, res_mgr):
        os.makedirs(
            os.path.dirname(res_mgr.file_path), exist_ok=True
        )
        with open(res_mgr.file_path, "w", encoding="utf-8") as fh:
            fh.write("not valid json!")
        _seed(res_mgr)
        result = res_mgr.create_reservation(1, 1)
        assert result is not None
        assert result["reservation_id"] == 1

    def test_load_non_list_json(self, res_mgr):
        os.makedirs(
            os.path.dirname(res_mgr.file_path), exist_ok=True
        )
        with open(res_mgr.file_path, "w", encoding="utf-8") as fh:
            json.dump({"bad": "data"}, fh)
        _seed(res_mgr)
        result = res_mgr.create_reservation(1, 1)
        assert result is not None
