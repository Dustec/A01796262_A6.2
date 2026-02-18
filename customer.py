"""Customer module with JSON persistence."""
import os
import re

from base_manager import BaseManager


class Customer(BaseManager):
    """Manages customer records with JSON file persistence."""

    DEFAULT_FILE = os.path.join("data", "customers.json")
    EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    def __init__(self, file_path=None):
        super().__init__(file_path, self.DEFAULT_FILE)

    def create_customer(self, name, email):
        """Create a new customer and persist it.

        Returns the created customer dict or None on validation error.
        """
        if not self.validate_non_empty_string(
            name, "Customer name"
        ):
            return None
        if not email or not isinstance(email, str):
            print("Error: Email must be a non-empty string.")
            return None
        if not self.EMAIL_RE.match(email):
            print("Error: Invalid email format.")
            return None

        customers = self.load()
        new_customer = {
            "customer_id": self.next_id(
                customers, "customer_id"
            ),
            "name": name.strip(),
            "email": email.strip(),
        }
        customers.append(new_customer)
        self.save(customers)
        return new_customer

    def delete_customer(self, customer_id):
        """Delete a customer by id.

        Returns True if deleted, False otherwise.
        """
        customers = self.load()
        original_len = len(customers)
        customers = [
            c for c in customers
            if c["customer_id"] != customer_id
        ]
        if len(customers) == original_len:
            print(
                f"Error: Customer with id "
                f"{customer_id} not found."
            )
            return False
        self.save(customers)
        return True

    def display_customer_info(self, customer_id):
        """Return customer dict for the given id, or None."""
        customers = self.load()
        for customer in customers:
            if customer["customer_id"] == customer_id:
                return customer
        print(f"Error: Customer with id {customer_id} not found.")
        return None

    def modify_customer_info(self, customer_id, **kwargs):
        """Modify customer attributes.

        Allowed keys: name, email.
        Returns updated customer dict or None on error.
        """
        if not self._validate_customer_kwargs(kwargs):
            return None

        customers = self.load()
        for customer in customers:
            if customer["customer_id"] == customer_id:
                if "name" in kwargs:
                    customer["name"] = kwargs["name"].strip()
                if "email" in kwargs:
                    customer["email"] = kwargs["email"].strip()
                self.save(customers)
                return customer

        print(
            f"Error: Customer with id {customer_id} not found."
        )
        return None

    def _validate_customer_kwargs(self, kwargs):
        """Validate keyword arguments for modify_customer_info."""
        allowed = {"name", "email"}
        if not self.validate_allowed_keys(kwargs, allowed):
            return False
        if "name" in kwargs:
            if not self.validate_non_empty_string(
                kwargs["name"], "Customer name"
            ):
                return False
        if "email" in kwargs:
            val = kwargs["email"]
            if not val or not isinstance(val, str):
                print("Error: Email must be a non-empty string.")
                return False
            if not self.EMAIL_RE.match(val):
                print("Error: Invalid email format.")
                return False
        return True
