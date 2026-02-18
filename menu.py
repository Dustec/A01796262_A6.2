"""Interactive CLI menu for the Reservation System."""
from hotel import Hotel
from customer import Customer
from reservation import Reservation


def _read_int(prompt):
    """Prompt for an integer, return None on invalid input."""
    try:
        return int(input(prompt))
    except ValueError:
        print("Error: Please enter a valid integer.")
        return None


# ---------- Hotel handlers ----------

def _handle_create_hotel(mgr):
    name = input("Hotel name: ").strip()
    location = input("Location: ").strip()
    rooms = _read_int("Number of rooms: ")
    if rooms is not None:
        result = mgr.create_hotel(name, location, rooms)
        if result:
            print(f"Hotel created: {result}")


def _handle_delete_hotel(mgr):
    hotel_id = _read_int("Hotel ID to delete: ")
    if hotel_id is not None and mgr.delete_hotel(hotel_id):
        print("Hotel deleted successfully.")


def _handle_display_hotel(mgr):
    hotel_id = _read_int("Hotel ID: ")
    if hotel_id is not None:
        info = mgr.display_hotel_info(hotel_id)
        if info:
            for key, val in info.items():
                print(f"  {key}: {val}")


def _handle_modify_hotel(mgr):
    hotel_id = _read_int("Hotel ID to modify: ")
    if hotel_id is None:
        return
    print("Leave blank to skip a field.")
    name = input("New name: ").strip() or None
    location = input("New location: ").strip() or None
    rooms_str = input("New number of rooms: ").strip()
    kwargs = {}
    if name:
        kwargs["name"] = name
    if location:
        kwargs["location"] = location
    if rooms_str:
        try:
            kwargs["rooms"] = int(rooms_str)
        except ValueError:
            print("Error: Rooms must be a valid integer.")
            return
    if kwargs:
        result = mgr.modify_hotel_info(hotel_id, **kwargs)
        if result:
            print(f"Hotel updated: {result}")


def _hotel_menu(mgr):
    """Sub-menu for hotel operations."""
    actions = {
        "1": _handle_create_hotel,
        "2": _handle_delete_hotel,
        "3": _handle_display_hotel,
        "4": _handle_modify_hotel,
    }
    while True:
        print("\n--- Hotel Menu ---")
        print("1. Create Hotel")
        print("2. Delete Hotel")
        print("3. Display Hotel Information")
        print("4. Modify Hotel Information")
        print("5. Back to Main Menu")
        choice = input("Select an option: ").strip()
        if choice == "5":
            break
        handler = actions.get(choice)
        if handler:
            handler(mgr)
        else:
            print("Error: Invalid option.")


# ---------- Customer handlers ----------

def _handle_create_customer(mgr):
    name = input("Customer name: ").strip()
    email = input("Email: ").strip()
    result = mgr.create_customer(name, email)
    if result:
        print(f"Customer created: {result}")


def _handle_delete_customer(mgr):
    cust_id = _read_int("Customer ID to delete: ")
    if cust_id is not None and mgr.delete_customer(cust_id):
        print("Customer deleted successfully.")


def _handle_display_customer(mgr):
    cust_id = _read_int("Customer ID: ")
    if cust_id is not None:
        info = mgr.display_customer_info(cust_id)
        if info:
            for key, val in info.items():
                print(f"  {key}: {val}")


def _handle_modify_customer(mgr):
    cust_id = _read_int("Customer ID to modify: ")
    if cust_id is None:
        return
    print("Leave blank to skip a field.")
    name = input("New name: ").strip() or None
    email = input("New email: ").strip() or None
    kwargs = {}
    if name:
        kwargs["name"] = name
    if email:
        kwargs["email"] = email
    if kwargs:
        result = mgr.modify_customer_info(cust_id, **kwargs)
        if result:
            print(f"Customer updated: {result}")


def _customer_menu(mgr):
    """Sub-menu for customer operations."""
    actions = {
        "1": _handle_create_customer,
        "2": _handle_delete_customer,
        "3": _handle_display_customer,
        "4": _handle_modify_customer,
    }
    while True:
        print("\n--- Customer Menu ---")
        print("1. Create Customer")
        print("2. Delete Customer")
        print("3. Display Customer Information")
        print("4. Modify Customer Information")
        print("5. Back to Main Menu")
        choice = input("Select an option: ").strip()
        if choice == "5":
            break
        handler = actions.get(choice)
        if handler:
            handler(mgr)
        else:
            print("Error: Invalid option.")


# ---------- Reservation handlers ----------

def _handle_create_reservation(mgr):
    cust_id = _read_int("Customer ID: ")
    hotel_id = _read_int("Hotel ID: ")
    if cust_id is not None and hotel_id is not None:
        result = mgr.create_reservation(cust_id, hotel_id)
        if result:
            print(f"Reservation created: {result}")


def _handle_cancel_reservation(mgr):
    res_id = _read_int("Reservation ID to cancel: ")
    if res_id is not None and mgr.cancel_reservation(res_id):
        print("Reservation cancelled successfully.")


def _reservation_menu(mgr):
    """Sub-menu for reservation operations."""
    actions = {
        "1": _handle_create_reservation,
        "2": _handle_cancel_reservation,
    }
    while True:
        print("\n--- Reservation Menu ---")
        print("1. Create Reservation")
        print("2. Cancel Reservation")
        print("3. Back to Main Menu")
        choice = input("Select an option: ").strip()
        if choice == "3":
            break
        handler = actions.get(choice)
        if handler:
            handler(mgr)
        else:
            print("Error: Invalid option.")


# ---------- Main ----------

def main():
    """Entry point for the reservation system CLI."""
    hotel_mgr = Hotel()
    customer_mgr = Customer()
    res_mgr = Reservation()

    menus = {
        "1": (hotel_mgr, _hotel_menu),
        "2": (customer_mgr, _customer_menu),
        "3": (res_mgr, _reservation_menu),
    }

    while True:
        print("\n===== Reservation System =====")
        print("1. Hotels")
        print("2. Customers")
        print("3. Reservations")
        print("4. Exit")
        choice = input("Select an option: ").strip()
        if choice == "4":
            print("Goodbye!")
            break
        entry = menus.get(choice)
        if entry:
            mgr, menu_fn = entry
            menu_fn(mgr)
        else:
            print("Error: Invalid option.")


if __name__ == "__main__":
    main()
