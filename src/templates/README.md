# Calendars

Copy the target link via right click.

{% for cal in cals -%}
- [{{ cal.name }}](https://raw.githubusercontent.com/Schluggi/pk-jam-calendar/main/calendars/{{ cal.filename }})
{% endfor %}
