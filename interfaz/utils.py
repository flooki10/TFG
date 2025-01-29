import customtkinter as ctk
from datetime import datetime

def set_appearance_mode(mode):
    ctk.set_appearance_mode(mode)

def set_default_color_theme(theme):
    ctk.set_default_color_theme(theme)

def validate_date(date_string):
    try:
        datetime.strptime(date_string, "%Y-%m")
        return True
    except ValueError:
        return False

class CustomTheme:
    COLORS = {
        "primary": "#2C3E50",       # Azul oscuro
        "secondary": "#ECEFF1",     # Gris claro
        "accent": "#26A69A",        # Verde azulado
        "bg_primary": "#ECEFF1",    # Gris claro para el fondo principal
        "bg_secondary": "#FFFFFF",  # Blanco
        "text_primary": "#2C3E50",  # Azul oscuro para texto principal
        "text_secondary": "#7F8C8D", # Gris medio para texto secundario
        "text_light": "#FFFFFF",    # Blanco para texto en fondo oscuro
        "error": "#E74C3C",         # Rojo suave para errores
        "success": "#4CAF50",       # Verde suave para éxito
        "icon_bg": "#ECEFF1",       # Gris claro para el fondo de los iconos
        "icon_color": "#26A69A",    # Verde azulado para los iconos
        "barra":"#BDC3C7",
    }

    FONTS = {
        "default": ("Roboto", 12),
        "title": ("Roboto", 24, "bold"),
        "subtitle": ("Roboto", 18, "bold"),
        "button": ("Roboto", 14, "bold"),
    }

    @classmethod
    def apply(cls, widget):
        if isinstance(widget, ctk.CTk):
            widget.configure(fg_color=cls.COLORS["bg_primary"])
        elif isinstance(widget, ctk.CTkFrame):
            widget.configure(fg_color=cls.COLORS["bg_secondary"], corner_radius=10)
        elif isinstance(widget, ctk.CTkButton):
            widget.configure(
                fg_color=cls.COLORS["accent"],
                hover_color=cls.COLORS["primary"],
                text_color=cls.COLORS["text_light"],
                corner_radius=6,
                font=cls.FONTS["button"],
                border_width=0,
            )
        elif isinstance(widget, ctk.CTkEntry):
            widget.configure(
                fg_color=cls.COLORS["bg_secondary"],
                text_color=cls.COLORS["text_primary"],
                border_color=cls.COLORS["primary"],
                corner_radius=6,
                font=cls.FONTS["default"],
            )
        elif isinstance(widget, (ctk.CTkCheckBox, ctk.CTkSwitch)):
            widget.configure(
                fg_color=cls.COLORS["accent"],
                text_color=cls.COLORS["text_primary"],
                border_color=cls.COLORS["primary"],
                corner_radius=6,
                font=cls.FONTS["default"],
            )
        elif isinstance(widget, ctk.CTkLabel):
            widget.configure(text_color=cls.COLORS["text_primary"], font=cls.FONTS["default"])
        elif isinstance(widget, ctk.CTkOptionMenu):
            widget.configure(
                fg_color=cls.COLORS["bg_secondary"],
                button_color=cls.COLORS["accent"],
                button_hover_color=cls.COLORS["primary"],
                text_color=cls.COLORS["text_primary"],
                dropdown_fg_color=cls.COLORS["bg_secondary"],
                dropdown_hover_color=cls.COLORS["secondary"],
                dropdown_text_color=cls.COLORS["text_primary"],
                font=cls.FONTS["default"],
            )
        elif isinstance(widget, ctk.CTkSlider):
            widget.configure(
                button_color=cls.COLORS["accent"],
                button_hover_color=cls.COLORS["primary"],
                progress_color=cls.COLORS["accent"],
            )
        elif isinstance(widget, ctk.CTkRadioButton):
            widget.configure(
                fg_color=cls.COLORS["accent"],
                border_color=cls.COLORS["primary"],
                hover_color=cls.COLORS["primary"],
                text_color=cls.COLORS["text_primary"],
                font=cls.FONTS["default"],
            )
        elif isinstance(widget, ctk.CTkTextbox):
            widget.configure(
                fg_color=cls.COLORS["bg_secondary"],
                text_color=cls.COLORS["text_primary"],
                corner_radius=6,
                font=cls.FONTS["default"],
            )
        
        for child in widget.winfo_children():
            cls.apply(child)

def create_styled_widget(widget_class, parent, **kwargs):
    widget = widget_class(parent, **kwargs)
    CustomTheme.apply(widget)
    return widget

# Convenience functions for creating styled widgets
create_styled_button = lambda parent, **kwargs: create_styled_widget(ctk.CTkButton, parent, **kwargs)
create_styled_entry = lambda parent, **kwargs: create_styled_widget(ctk.CTkEntry, parent, **kwargs)
create_styled_checkbox = lambda parent, **kwargs: create_styled_widget(ctk.CTkCheckBox, parent, **kwargs)
create_styled_label = lambda parent, **kwargs: create_styled_widget(ctk.CTkLabel, parent, **kwargs)
create_styled_frame = lambda parent, **kwargs: create_styled_widget(ctk.CTkFrame, parent, **kwargs)
create_styled_optionemenu = lambda parent, **kwargs: create_styled_widget(ctk.CTkOptionMenu, parent, **kwargs)

