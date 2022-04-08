import requests


def main():
    resp = requests.get(
        "https://api.axios.com/api/render/stream/content?audience_slug=washington-dc&topic_slug=things-to-do"
    )
    print(resp.json())


if __name__ == "__main__":
    main()
