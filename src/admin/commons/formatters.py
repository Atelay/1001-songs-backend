from datetime import datetime
from markupsafe import Markup

from src.config import settings


class MediaFormatter:
    def __init__(self, is_file: bool = False) -> None:
        self.is_file = is_file

    def __call__(self, m, a):
        file = getattr(m, a, None)
        if file:
            if self.is_file:
                icon_url = f"{settings.BASE_URL}/static/interface/pdf_icon.svg"
                grid_html = f'<a href="{settings.BASE_URL}/{file}"><img class="grid-item" src="{icon_url}"></a>'

            else:
                grid_html = f'<img class="grid-item" src="{settings.BASE_URL}/{file}">'
        return Markup(grid_html)


class MediaSplitFormatter:
    def __init__(self, media_fields: list[str]) -> None:
        self.media_fields = media_fields

    def __call__(self, m, a):
        grid_html = ""
        for field in self.media_fields:
            image = getattr(m, field, None)
            if image:
                grid_html += f'<img class="grid-item" src={settings.BASE_URL}/{image}>'
        return Markup(grid_html)


def format_quill(m, a):
    if field_data := getattr(m, a, None):
        return Markup(f"<div class='quill-column'>{field_data}</div>")


def format_datetime(m, a):
    if field_data := getattr(m, a, None):
        field_data: datetime
        return field_data.strftime("%d/%m/%Y, %H:%M")


def format_array_of_string(m, a):
    if field_data := getattr(m, a, None):
        res = ""
        for data in field_data:
            res += f"<br>{data}"
        return Markup(res)
