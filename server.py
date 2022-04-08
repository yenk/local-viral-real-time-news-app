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
