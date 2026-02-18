"""Unit tests for the Customer class."""
import json
import os

import pytest

from customer import Customer


@pytest.fixture
def cust_mgr(tmp_path):
    """Return a Customer manager that uses a temp JSON file."""
    path = str(tmp_path / "customers.json")
    return Customer(file_path=path)


# ---------- positive / happy-path tests ----------

class TestCreateCustomer:
    """Tests for create_customer."""

    def test_create_single(self, cust_mgr):
        result = cust_mgr.create_customer("Alice", "alice@mail.com")
        assert result is not None
        assert result["name"] == "Alice"
        assert result["customer_id"] == 1

    def test_create_multiple_increments_id(self, cust_mgr):
        cust_mgr.create_customer("A", "a@mail.com")
        second = cust_mgr.create_customer("B", "b@mail.com")
        assert second["customer_id"] == 2

    def test_create_persists_to_file(self, cust_mgr):
        cust_mgr.create_customer("Saved", "saved@mail.com")
        with open(cust_mgr.file_path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        assert len(data) == 1
        assert data[0]["email"] == "saved@mail.com"


class TestDeleteCustomer:
    """Tests for delete_customer."""

    def test_delete_existing(self, cust_mgr):
        cust_mgr.create_customer("Del", "del@mail.com")
        assert cust_mgr.delete_customer(1) is True

    def test_delete_removes_from_file(self, cust_mgr):
        cust_mgr.create_customer("Del", "del@mail.com")
        cust_mgr.delete_customer(1)
        with open(cust_mgr.file_path, "r", encoding="utf-8") as fh:
            assert json.load(fh) == []


class TestDisplayCustomer:
    """Tests for display_customer_info."""

    def test_display_existing(self, cust_mgr):
        cust_mgr.create_customer("Show", "show@mail.com")
        info = cust_mgr.display_customer_info(1)
        assert info["name"] == "Show"
        assert info["email"] == "show@mail.com"


class TestModifyCustomer:
    """Tests for modify_customer_info."""

    def test_modify_name(self, cust_mgr):
        cust_mgr.create_customer("Old", "old@mail.com")
        updated = cust_mgr.modify_customer_info(1, name="New")
        assert updated["name"] == "New"

    def test_modify_email(self, cust_mgr):
        cust_mgr.create_customer("C", "old@mail.com")
        updated = cust_mgr.modify_customer_info(1, email="new@mail.com")
        assert updated["email"] == "new@mail.com"


# ---------- negative / error-handling tests ----------

class TestNegativeCases:
    """Negative test cases for Customer."""

    def test_create_empty_name(self, cust_mgr):
        assert cust_mgr.create_customer("", "a@mail.com") is None

    def test_create_whitespace_name(self, cust_mgr):
        assert cust_mgr.create_customer("   ", "a@mail.com") is None

    def test_create_none_name(self, cust_mgr):
        assert cust_mgr.create_customer(None, "a@mail.com") is None

    def test_create_invalid_email_no_at(self, cust_mgr):
        assert cust_mgr.create_customer("C", "invalid") is None

    def test_create_invalid_email_no_domain(self, cust_mgr):
        assert cust_mgr.create_customer("C", "a@") is None

    def test_create_empty_email(self, cust_mgr):
        assert cust_mgr.create_customer("C", "") is None

    def test_create_none_email(self, cust_mgr):
        assert cust_mgr.create_customer("C", None) is None

    def test_delete_nonexistent(self, cust_mgr):
        assert cust_mgr.delete_customer(999) is False

    def test_display_nonexistent(self, cust_mgr):
        assert cust_mgr.display_customer_info(999) is None

    def test_modify_nonexistent(self, cust_mgr):
        assert cust_mgr.modify_customer_info(999, name="X") is None

    def test_modify_invalid_field(self, cust_mgr):
        cust_mgr.create_customer("C", "c@mail.com")
        assert cust_mgr.modify_customer_info(1, phone="123") is None

    def test_modify_empty_name(self, cust_mgr):
        cust_mgr.create_customer("C", "c@mail.com")
        assert cust_mgr.modify_customer_info(1, name="") is None

    def test_modify_invalid_email(self, cust_mgr):
        cust_mgr.create_customer("C", "c@mail.com")
        assert cust_mgr.modify_customer_info(1, email="bad") is None

    def test_load_corrupt_json(self, cust_mgr):
        os.makedirs(os.path.dirname(cust_mgr.file_path), exist_ok=True)
        with open(cust_mgr.file_path, "w", encoding="utf-8") as fh:
            fh.write("<<<not json>>>")
        result = cust_mgr.create_customer("C", "c@mail.com")
        assert result is not None
        assert result["customer_id"] == 1

    def test_load_non_list_json(self, cust_mgr):
        os.makedirs(os.path.dirname(cust_mgr.file_path), exist_ok=True)
        with open(cust_mgr.file_path, "w", encoding="utf-8") as fh:
            json.dump({"wrong": "type"}, fh)
        result = cust_mgr.create_customer("C", "c@mail.com")
        assert result is not None
