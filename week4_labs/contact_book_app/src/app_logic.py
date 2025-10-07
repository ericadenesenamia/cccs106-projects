import flet as ft
from database import update_contact_db, delete_contact_db, add_contact_db, get_all_contacts_db


def display_contacts(page, contacts_list_view, db_conn, search_term=None):
    """Fetches and displays all contacts in the ListView."""
    contacts_list_view.controls.clear()
    contacts = get_all_contacts_db(db_conn, search_term)

    for contact in contacts:
        contact_id, name, phone, email = contact

        contacts_list_view.controls.append(
            ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(name, size=18, weight=ft.FontWeight.BOLD),
                            ft.Row([ft.Icon(ft.Icons.PHONE), ft.Text(phone or "No phone")]),
                            ft.Row([ft.Icon(ft.Icons.EMAIL), ft.Text(email or "No email")]),
                            ft.Row(  # Buttons row inside the card
                                [
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT,
                                        tooltip="Edit",
                                        on_click=lambda _, c=contact: open_edit_dialog(page, c, db_conn, contacts_list_view)
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE,
                                        tooltip="Delete",
                                        on_click=lambda _, cid=contact_id: confirm_delete(page, cid, db_conn, contacts_list_view)
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.END
                            ),
                        ]
                    ),
                    padding=10,
                ),
            )
        )

    page.update()


def add_contact(page, inputs, contacts_list_view, db_conn):
    """Adds a new contact and refreshes the list."""
    name_input, phone_input, email_input = inputs

    # Validation
    has_error = False
    if not name_input.value.strip():
        name_input.error_text = "Name cannot be empty"
        has_error = True
    else:
        name_input.error_text = None

    if not phone_input.value.strip():
        phone_input.error_text = "Phone cannot be empty"
        has_error = True
    else:
        phone_input.error_text = None

    if not email_input.value.strip():
        email_input.error_text = "Email cannot be empty"
        has_error = True
    else:
        email_input.error_text = None

    page.update()

    if has_error:
        return

    # Insert into DB
    add_contact_db(db_conn, name_input.value, phone_input.value, email_input.value)

    for field in inputs:
        field.value = ""

    display_contacts(page, contacts_list_view, db_conn)
    page.update()


def delete_contact(page, contact_id, db_conn, contacts_list_view):
    """Deletes a contact and refreshes the list."""
    delete_contact_db(db_conn, contact_id)
    display_contacts(page, contacts_list_view, db_conn)


def confirm_delete(page, contact_id, db_conn, contacts_list_view):
    """Asks user to confirm before deleting a contact."""
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirm Delete"),
        content=ft.Text("Are you sure you want to delete this contact?"),
        actions=[
            ft.TextButton("No", on_click=lambda e: close_dialog(page, dialog)),
            ft.TextButton(
                "Yes",
                on_click=lambda e: (
                    delete_contact(page, contact_id, db_conn, contacts_list_view),
                    close_dialog(page, dialog)
                ),
            ),
        ],
    )
    page.open(dialog)


def close_dialog(page, dialog):
    dialog.open = False
    page.update()


def open_edit_dialog(page, contact, db_conn, contacts_list_view):
    """Opens a dialog to edit a contact's details."""
    contact_id, name, phone, email = contact

    edit_name = ft.TextField(label="Name", value=name)
    edit_phone = ft.TextField(label="Phone", value=phone)
    edit_email = ft.TextField(label="Email", value=email)

    def save_and_close(e):
        update_contact_db(db_conn, contact_id, edit_name.value, edit_phone.value, edit_email.value)
        dialog.open = False
        page.update()
        display_contacts(page, contacts_list_view, db_conn)

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Edit Contact"),
        content=ft.Column([edit_name, edit_phone, edit_email]),
        actions=[
            ft.TextButton("Cancel", on_click=lambda e: close_dialog(page, dialog)),
            ft.TextButton("Save", on_click=save_and_close),
        ],
    )

    page.open(dialog)