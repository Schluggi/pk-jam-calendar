# Calendars

Copy the target link via right click.

# Countries
{% for cal in cals -%}
- [{{ cal.name }}](https://raw.githubusercontent.com/Schluggi/pk-jam-calendar/main/calendars/{{ cal.filename }})
{% endfor %}

Use [this link](https://raw.githubusercontent.com/Schluggi/pk-jam-calendar/main/calendars/all.ics) for a combined
calendar with all events of all countries.