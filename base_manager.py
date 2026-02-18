"""Base persistence manager shared by Hotel, Customer, Reservation."""
import json
import os


class BaseManager:
    """Provides common JSON persistence and validation logic."""

    def __init__(self, file_path, default_file):
        self.file_path = file_path or default_file

    def load(self):
        """Load a list of records from the JSON file."""
        if not os.path.exists(self.file_path):
            return []
        try:
            with open(self.file_path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
                if not isinstance(data, list):
                    print(
                        f"Error: {self.file_path} "
                        f"does not contain a list."
                    )
                    return []
                return data
        except (json.JSONDecodeError, OSError) as exc:
            print(f"Error loading {self.file_path}: {exc}")
            return []

    def save(self, records):
        """Persist a list of records to the JSON file."""
        directory = os.path.dirname(self.file_path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(self.file_path, "w", encoding="utf-8") as fh:
            json.dump(records, fh, indent=2)

    def next_id(self, records, id_field):
        """Return the next available id for *id_field*."""
        if not records:
            return 1
        return max(r[id_field] for r in records) + 1

    @staticmethod
    def validate_allowed_keys(kwargs, allowed):
        """Return True if all keys in *kwargs* are in *allowed*."""
        invalid_keys = set(kwargs.keys()) - allowed
        if invalid_keys:
            print(f"Error: Invalid fields: {invalid_keys}")
            return False
        return True

    @staticmethod
    def validate_non_empty_string(value, field_name):
        """Return True if *value* is a non-empty string."""
        if not value or not isinstance(value, str) \
                or not value.strip():
            print(
                f"Error: {field_name} must be a non-empty string."
            )
            return False
        return True
