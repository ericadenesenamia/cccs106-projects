import flet as ft
from database import init_db
from app_logic import display_contacts, add_contact


def main(page: ft.Page):
    page.title = "Contact Book"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.window_width = 400
    page.window_height = 600
    page.theme_mode = ft.ThemeMode.LIGHT  # default theme

    db_conn = init_db()

    # --- Input Fields with Icons + Fixed Width ---
    name_input = ft.TextField(label="Name", prefix_icon=ft.Icons.PERSON, width=350)
    phone_input = ft.TextField(label="Phone", prefix_icon=ft.Icons.PHONE, width=350)
    email_input = ft.TextField(label="Email", prefix_icon=ft.Icons.EMAIL, width=350)

    inputs = [name_input, phone_input, email_input]

    add_button = ft.ElevatedButton(
        text="Add Contact",
        icon=ft.Icons.ADD,
        on_click=lambda e: add_contact(page, inputs, contacts_list_view, db_conn)
    )

    # --- Dark Mode Toggle ---
    def toggle_theme(e):
        page.theme_mode = (
            ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        )
        page.update()

    theme_switch = ft.Switch(label="Dark Mode", on_change=toggle_theme)

    contacts_list_view = ft.ListView(expand=True, spacing=10, padding=10)

    # --- Search Bar ---
    search_field = ft.TextField(
        label="Search by Name",
        prefix_icon=ft.Icons.SEARCH,
        width=350,
        on_change=lambda e: display_contacts(page, contacts_list_view, db_conn, e.control.value)
    )

    # Layout
    page.add(
        ft.Column(
            [
                ft.Text("Enter Contact Details", size=20, weight=ft.FontWeight.BOLD),
                name_input,
                phone_input,
                email_input,
                add_button,
                ft.Divider(),
                ft.Row(
                    [
                        ft.Text("Contacts", size=20, weight=ft.FontWeight.BOLD),
                        theme_switch,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                search_field,
                contacts_list_view,
            ],
            expand=True,
        )
    )

    display_contacts(page, contacts_list_view, db_conn)


ft.app(main)