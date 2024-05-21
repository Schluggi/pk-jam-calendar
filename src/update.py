from datetime import datetime, timedelta
from sys import argv, exit

from icalendar import Calendar, Event, vCalAddress, vText
from jinja2 import Environment, FileSystemLoader
from requests import get

if len(argv) != 4:
    exit('main.py <output> <prodid> <url>')

output = argv[1]
prodid = argv[2]
url = argv[3]

data = get(url).json()

calendars = {}

data['categories'].append({'name': 'all'})

for category in data['categories']:
    cal = Calendar()
    cal.add('prodid', prodid)
    cal.add('version', '2.0')

    calendars[category['name']] = cal

for event_data in data['events']:
    print(event_data)
    event = Event()

    event.add('uid', event_data['id'])
    event.add('summary', event_data['title'].title())
    event.add('description', event_data['desc'])

    if event_data['all_day'] == 1:
        start = datetime.strptime(event_data['start'], '%Y-%m-%d').date()
        end = datetime.strptime(event_data['end'], '%Y-%m-%d').date()
    else:
        start = datetime.strptime(event_data['start'], '%Y-%m-%dT%H:%M')
        end = datetime.strptime(event_data['end'], '%Y-%m-%dT%H:%M')

    if event_data['start'] != event_data['end']:
        end += timedelta(days=1)

    event.add('dtstart', start)
    event.add('dtend', end)

    organizer = vCalAddress(f'MAILTO:{event_data["organizer"]["email"]}')
    organizer.params['cn'] = vText(event_data['organizer']['name'])
    organizer.params['phone'] = vText(event_data['organizer']['phone'])
    organizer.params['website'] = vText(event_data['organizer']['website'])
    event['organizer'] = organizer

    event['location'] = vText(event_data['venue']['address'])

    if 'lat' in event_data['venue'] and 'long' in event_data['venue'] \
            and event_data['venue']['lat'] and event_data['venue']['long']:
        event.add('geo', (event_data["venue"]["lat"], event_data["venue"]["long"]))

    for cat in event_data['categories']:
        calendars[cat['name']].add_component(event)

    calendars['all'].add_component(event)

cals = []
for calendar in calendars:
    filename = f'{calendar.replace(" ", "_").lower()}.ics'
    cals.append({
        'name': calendar,
        'filename': filename
    })

    with open(f'{output}/{filename}', 'wb') as f:
        print(f'saving calendar {calendar}')
        f.write(calendars[calendar].to_ical())

cals.sort(key=lambda x: x['name'])
env = Environment(loader=FileSystemLoader('templates/'))
template = env.get_template("README.md")

with open(f'{output}/README.md', 'w', encoding='utf-8') as f:
    f.write(template.render(cals=[c for c in cals if c['name'] != 'all']))
