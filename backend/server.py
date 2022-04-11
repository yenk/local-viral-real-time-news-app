import pprint
import requests


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

    pprint.pprint(dash_content)
    return dash_content


if __name__ == "__main__":
    get_dash_content("Washington DC", ["Things to Do", "Sports"])
