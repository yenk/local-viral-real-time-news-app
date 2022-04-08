import pprint
import requests


def main():
    things_to_do_resp = requests.get(
        "https://api.axios.com/api/render/stream/content?audience_slug=washington-dc&topic_slug=things-to-do"
    ).json()["results"]
    sports_resp = requests.get(
        "https://api.axios.com/api/render/stream/content?audience_slug=washington-dc&topic_slug=sports"
    ).json()["results"]

    things_to_do_content = []
    for id in things_to_do_resp:
        resp = requests.get(f"https://api.axios.com/api/render/content/{id}/")
        things_to_do_content.append(
            {
                "headline": resp.json().get("headline"),
                "permalink": resp.json().get("permalink"),
                "published": resp.json().get("published_date"),
            }
        )

    sports_content = []
    for id in sports_resp:
        resp = requests.get(f"https://api.axios.com/api/render/content/{id}/")
        sports_content.append(
            {
                "headline": resp.json().get("headline"),
                "permalink": resp.json().get("permalink"),
                "published": resp.json().get("published_date"),
            }
        )

    resp = {"Things To Do": things_to_do_content, "Sports": sports_content}
    pprint.pprint(resp)


if __name__ == "__main__":
    main()
