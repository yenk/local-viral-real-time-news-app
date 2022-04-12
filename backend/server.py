import datetime
import pandas
import pendulum
import pprint
import requests
from google.transit import gtfs_realtime_pb2
import urllib
import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
from google.protobuf.json_format import MessageToJson


def sluggify(value):
    return value.replace(" ", "-").lower()


def get_topic_key(content_topics, req_topics):
    current_topic = next(
        topic.get("name") for topic in content_topics if topic.get("name") in req_topics
    )
    return current_topic


def get_dash_content(audience, topics):
    """
    grabs latest axios stories for the given audience and topics

    param audience: string, the local audience the content is targeted for (ie "Washington DC")
    param topics: array[string], a list of topics the content is tagged as (ie ["Sports", "Things to Do", "Food and Drink"])

    return: json data with headline, permalink, and publish date for each story by topic (see example output below)
    {
        'Sports': [
            {
                'headline': 'How to fake it: Your guide to the Nats 2022 season',
                'permalink': 'https://www.axios.com/local/washington-dc/2022/04/07/washington-nationals-2022-season-guide',
                'published': '2022-04-07T10:20:02Z'
            },
            {
                'headline': 'How to fake it: Your guide to the Nats 2022 season',
                'permalink': 'https://www.axios.com/local/washington-dc/2022/04/07/washington-nationals-2022-season-guide',
                'published': '2022-04-07T10:20:02Z'
            },
            {
                'headline': 'What to expect at Nats Park in 2022',
                'permalink': 'https://www.axios.com/local/washington-dc/2022/04/04/what-to-expect-nats-park-2022',
                'published': '2022-04-04T10:20:20Z'
            }
        ],
        'Things to Do': [
            {
                'headline': 'How did you meet your D.C. bestie?',
                'permalink': 'https://www.axios.com/local/washington-dc/2022/04/08/how-did-you-meet-your-dc-bestie',
                'published': '2022-04-08T10:20:15Z'
            },
            {
                'headline': 'Your Washington Weekend: April 8-10',
                'permalink': 'https://www.axios.com/local/washington-dc/2022/04/08/your-washington-weekend-april-8-10',
                'published': '2022-04-08T10:17:38Z'
            }
        ]
    }
    """

    dash_content = {}
    content_ids = []

    for topic in topics:
        resp = (
            requests.get(
                f"https://api.axios.com/api/render/stream/content?audience_slug={sluggify(audience)}&topic_slug={sluggify(topic)}"
            )
            .json()
            .get("results")
        )
        content_ids.extend(resp)
        dash_content[topic] = []

    for id in content_ids:
        resp = requests.get(f"https://api.axios.com/api/render/content/{id}/")
        dash_content[get_topic_key(resp.json().get("topics"), topics)].append(
            {
                "headline": resp.json().get("headline"),
                "permalink": resp.json().get("permalink"),
                "published": resp.json().get("published_date"),
            }
        )

    return dash_content


def get_local_avg_covid_data(county):
    """
    grabs rolling average covid data for the given county

    param county: string, the US county to return data for (ie "District of Columbia")
    return: csv data containing rolling averages for the given county in 2022 (see example output below)

        ,date,geoid,county,state,cases,cases_avg,cases_avg_per_100k,deaths,deaths_avg,deaths_avg_per_100k
        2928,2022-01-01,USA-11001,District of Columbia,District of Columbia,0,2103.0,297.98,0,0.4,0.06
        6188,2022-01-02,USA-11001,District of Columbia,District of Columbia,0,2103.0,297.98,0,0.4,0.06
        9448,2022-01-03,USA-11001,District of Columbia,District of Columbia,9201,2103.14,298.0,7,1.29,0.18
        12708,2022-01-04,USA-11001,District of Columbia,District of Columbia,2006,2122.86,300.79,2,1.38,0.19
        15968,2022-01-05,USA-11001,District of Columbia,District of Columbia,1326,2110.57,299.05,2,1.71,0.24
        ...
        325436,2022-04-10,USA-11001,District of Columbia,District of Columbia,0,143.57,20.34,0,0.29,0.04
    """

    avg_data = pandas.read_csv(
        "https://raw.githubusercontent.com/nytimes/covid-19-data/master/rolling-averages/us-counties-2022.csv",
    )

    avg_data = avg_data[avg_data["county"] == county]
    return avg_data.to_csv()


def get_local_live_covid_data(county):
    """
    grabs live covid data for the given county on the current day

    param county: string, the US county to return data for (ie "District of Columbia")
    return: csv data containing live for the given county today (see example output below)

        ,date,county,state,fips,cases,deaths,confirmed_cases,confirmed_deaths,probable_cases,probable_deaths
        322,2022-04-11,District of Columbia,District of Columbia,11001.0,137603,1331.0,134623.0,1319.0,2980.0,12.0
    """

    live_data = pandas.read_csv(
        "https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-counties.csv"
    )

    live_data = live_data[live_data["county"] == county]
    return live_data.to_csv()


def get_local_weather_data(zip):
    """
    grabs today's weather data for the given US zip code

    param zip: stringified US zip code (ie 20001 for Washington DC)
    return: json data with today's weather stats (see example output below)
    {
        'base': 'stations',
        'clouds': {'all': 0},
        'cod': 200,
        'coord': {'lat': 38.9122,'lon': -77.0177},
        'dt': 1649709422,
        'id': 4138106,
        'main': {
            'feels_like': 291.36,
            'humidity': 41,
            'pressure': 1016,
            'temp': 292.32,
            'temp_max': 294.83,
            'temp_min': 288.13
        },
        'name': 'District of Columbia',
        'sys': {
            'country': 'US',
            'id': 2002287,
            'sunrise': 1649673433,
            'sunset': 1649720432,
            'type': 2
        },
        'timezone': -14400,
        'visibility': 10000,
        'weather': [{
            'description': 'clear sky',
            'icon': '01d',
            'id': 800,
            'main': 'Clear'
        }],
        'wind': {'deg': 150,'speed': 5.14}
    }
    """

    api_key = "fb8d8414adc882229cec5abc077b21e1"

    resp = requests.get(
        f"http://api.openweathermap.org/geo/1.0/zip?zip={zip},US&appid={api_key}"
    )
    lat = resp.json().get("lat")
    lon = resp.json().get("lon")

    weather_data = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
    ).json()

    return weather_data


def get_local_event_data(zip, radius):
    """
    grabs upcoming weekend events for the given US zip code and mile radius

    param zip: stringified US zip code (ie 20001 for Washington DC)
    param radius: radius to search in miles (ie 50 for a 50 mile radius around the given zip code)

    return: json data with event info (see example output below)
    {
        'events': [
            {
                'description': None,
                'end': '',
                'name': 'Melvin Seals & JGB with special guest Ron Holloway ',
                'start': 'Friday, April 15, 12:00',
                'url': 'https://www.ticketmaster.com/melvin-seals-jgb-with-special-guest-washington-district-of-columbia-04-14-2022/event/15005B8A0F6F75D2',
                'venue': '9:30 CLUB'
            },
            {
                'description': None,
                'end': '',
                'name': 'Man On Man',
                'start': 'Sunday, April 17, 12:00',
                'url': 'https://www.ticketmaster.com/event/Z7r9jZ1Ad8paP',
                'venue': 'DC9 Nightclub'
            },
            {
                'description': None,
                'end': '',
                'name': "So Fetch: All the Best Music from the '00s",
                'start': 'Saturday, April 16, 12:00',
                'url': 'https://www.ticketmaster.com/so-fetch-all-the-best-music-washington-district-of-columbia-04-15-2022/event/15005C8B8EEC1464',
                'venue': '9:30 CLUB'
            }
        ]
    }
    """

    api_key = "dDtYgvRTpfJgiiACZzfWQW6922qTTqX2"

    weekend_start = pendulum.now().next(pendulum.FRIDAY).strftime("%Y-%m-%dT%H:%M:%SZ")
    weekend_end = pendulum.now().next(pendulum.SUNDAY).strftime("%Y-%m-%dT%H:%M:%SZ")

    resp = requests.get(
        f"https://app.ticketmaster.com/discovery/v2/events?apikey={api_key}&locale=*&startDateTime={str(weekend_start)}&endDateTime={str(weekend_end)}&postalCode={str(zip)}&radius={str(radius)}&unit=miles"
    )

    events = {"events": []}
    for event in resp.json().get("_embedded").get("events"):
        details = {}
        details["name"] = event.get("name")
        details["url"] = event.get("url")
        details["description"] = event.get("description")

        # get formatted date and time based on given time zone
        tz = event.get("dates").get("start").get("timezone")
        start = event.get("dates").get("start").get("dateTime")
        if start != "":
            start = (
                datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%SZ")
                .replace(tzinfo=tz)
                .strftime("%A, %B %d, %I:%M")
            )
        end = event.get("dates").get("end", {}).get("dateTime", "")
        if end != "":
            end = (
                datetime.datetime.strptime(end, "%Y-%m-%dT%H:%M:%SZ")
                .replace(tzinfo=tz)
                .strftime("%I:%M")
            )

        details["start"] = start
        details["end"] = end
        details["venue"] = event.get("_embedded").get("venues")[0].get("name")

        events["events"].append(details)

    return events


def get_metro_alert_data():
    """
    grabs latest metro alerts such as stop moved, unforeseen events affecting a
    station, route or the entire network

    return: json data with entity info (see example output below)
    {
        'Incidents': [
            {
                'DateUpdated': '2022-04-11T04:42:52',
                'DelaySeverity': None,
                'Description': 'Trains will operate every 20 minutes w/6-car '
                            'trains. Delays possible, plan additional '
                            'travel time.',
                'EmergencyText': None,
                'EndLocationFullName': None,
                'IncidentID': '1F15F226-8FCD-4806-901F-7A13DAFCF955',
                'IncidentType': 'Alert',
                'LinesAffected': 'GR; YL;',
                'PassengerDelay': 0.0,
                'StartLocationFullName': None
            },
            {
                'DateUpdated': '2022-04-11T04:42:09',
                'DelaySeverity': None,
                'Description': 'Trains will operate every 20 minutes w/6-car '
                            'trains. Delays possible, plan additional '
                            'travel time.',
                'EmergencyText': None,
                'EndLocationFullName': None,
                'IncidentID': '56FEC0BD-09F7-489D-8B87-42FF20966D92',
                'IncidentType': 'Alert',
                'LinesAffected': 'BL; OR; SV;',
                'PassengerDelay': 0.0,
                'StartLocationFullName': None
            },
            {
                'DateUpdated': '2022-04-11T04:41:22',
                'DelaySeverity': None,
                'Description': 'Trains will operate every 10 minutes w/6-car '
                            'trains. Delays possible, plan additional '
                            'travel time.',
                'EmergencyText': None,
                'EndLocationFullName': None,
                'IncidentID': '0A4755D3-0A04-473E-B4E0-7BDBBF9FFB3B',
                'IncidentType': 'Alert',
                'LinesAffected': 'RD;',
                'PassengerDelay': 0.0,
                'StartLocationFullName': None
            }
        ]
    }
    """
    headers = {
        "api_key": "3ee0597845df41f3a0d77a2668cf3e24",
    }

    try:
        data = requests.get(
            "https://api.wmata.com/Incidents.svc/json/Incidents", headers=headers
        )
        return data.json()

    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e))


def get_metro_trip_update_data():
    """
    gets information about delays, cancellations, changed routes

    return: json data with entity info (see example output below)
    {
        "entity": [{
            "id": "0",
            "tripUpdate": {
                "trip": {
                    "tripId": "4205056_19092",
                    "startTime": "14:40:00",
                    "startDate": "20220412",
                    "scheduleRelationship": "SCHEDULED",
                    "routeId": "RED",
                    "directionId": 0
                },
                "stopTimeUpdate": [
                    {
                        "stopSequence": 1,
                        "departure": {
                            "time": "1649788833",
                            "uncertainty": 0
                        },
                        "stopId": "PF_A15_C",
                        "scheduleRelationship": "SCHEDULED"
                    },
                    {
                        "stopSequence": 2,
                        "arrival": {
                            "time": "1649789154",
                            "uncertainty": 0
                        },
                        "stopId": "PF_A14_C",
                        "scheduleRelationship": "SCHEDULED"
                    },
                    {
                        "stopSequence": 3,
                        "arrival": {
                            "time": "1649789371",
                            "uncertainty": 0
                        },
                        "stopId": "PF_A13_C",
                        "scheduleRelationship": "SCHEDULED"
                    },
                ]
            }
        }]
    }

    """

    headers = {
        "api_key": "3ee0597845df41f3a0d77a2668cf3e24",
    }
    params = urllib.parse.urlencode({})

    try:
        conn = http.client.HTTPSConnection("api.wmata.com")
        conn.request(
            "GET", "/gtfs/rail-gtfsrt-tripupdates.pb?%s" % params, "{body}", headers
        )
        response = conn.getresponse()
        data = response.read()
        feedmessage = gtfs_realtime_pb2.FeedMessage()
        feedmessage.ParseFromString(data)
        trip_updates = gtfs_realtime_pb2.FeedMessage()

        for feedentity in feedmessage.entity:
            if feedentity.HasField("trip_update"):
                e = trip_updates.entity.add()
                e.CopyFrom(feedentity)

        return MessageToJson(trip_updates)

    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


def get_metro_vehicles_position_data():
    """
    gets information about the vehicles including location and congestion level

    return: json data with entity info (see example output below)
    {
      "entity": [{
            "id": "0",
            "isDeleted": false,
            "vehicle": {
                "trip": {
                    "tripId": "4205179_19092",
                    "startTime": "14:20:00",
                    "startDate": "20220412",
                    "scheduleRelationship": "SCHEDULED",
                    "routeId": "RED",
                    "directionId": 0
                },
                "position": {
                    "latitude": 38.92471,
                    "longitude": -77.05227,
                    "bearing": 156.0
                },
                "currentStopSequence": 12,
                "currentStatus": "INCOMING_AT",
                "timestamp": "1649789705",
                "stopId": "PF_A04_C",
                "vehicle": {
                    "id": "393",
                    "label": "107",
                    "licensePlate": "6"
                },
                "occupancyStatus": "MANY_SEATS_AVAILABLE"
            }
        }]
    }
    """

    headers = {
        "api_key": "3ee0597845df41f3a0d77a2668cf3e24",
    }
    params = urllib.parse.urlencode({})

    try:
        conn = http.client.HTTPSConnection("api.wmata.com")
        conn.request(
            "GET",
            "/gtfs/rail-gtfsrt-vehiclepositions.pb?%s" % params,
            "{body}",
            headers,
        )
        response = conn.getresponse()
        data = response.read()
        feedmessage = gtfs_realtime_pb2.FeedMessage()
        feedmessage.ParseFromString(data)
        vehicles = gtfs_realtime_pb2.FeedMessage()

        for feedentity in feedmessage.entity:
            if feedentity.HasField("vehicle"):
                e = vehicles.entity.add()
                e.CopyFrom(feedentity)

        return MessageToJson(vehicles)

    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


def get_bus_alert_data():
    """
    grabs bus alert data for the dc metro area

    returns: json data with bus incident info for DC (see example output below)
    {
        'BusIncidents': [
            {
                'DateUpdated': '2022-04-12T16:36:33',
                'Description': 'Due to emergency activity at MacArthur Blvd '
                                '& Cathedral Ave NW, buses may experience '
                                'possible delays and detours in both '
                                'directions.',
                'IncidentID': '801C22D8-79B6-4652-A8C7-9E52EA456C61',
                'IncidentType': 'Alert',
                'RoutesAffected': ['D6']
            }
        ]
    }
    """

    headers = {
        "api_key": "3ee0597845df41f3a0d77a2668cf3e24",
    }

    try:
        data = requests.get(
            f"https://api.wmata.com/Incidents.svc/json/BusIncidents", headers=headers
        )
        return data.json()

    except Exception as e:
        print(f"[Errno {e.errno}] {e}")


if __name__ == "__main__":
    pprint.pprint(get_dash_content("Washington DC", ["Things to Do", "Food and Drink"]))
    print(get_local_avg_covid_data("District of Columbia"))
    print(get_local_live_covid_data("District of Columbia"))
    pprint.pprint(get_local_weather_data("20001"))
    pprint.pprint(get_local_event_data("20001", 50))
    pprint.pprint(get_metro_alert_data())
    pprint.pprint(get_metro_trip_update_data())
    pprint.pprint(get_metro_vehicles_position_data())
    pprint.pprint(get_bus_alert_data())
