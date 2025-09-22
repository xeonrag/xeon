from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_URL = "https://sssinstagram.com/api/convert"

HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "priority": "u=1, i",
    "sec-ch-ua": '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    # ⚠ Cookie may expire, replace if request fails
    "cookie": "uid=0e0726d51b8420f1; _ga=GA1.1.879823300.1758550145; ..."
}

@app.route("/api/downloader/insta", methods=["GET"])
def insta_downloader():
    reel_url = request.args.get("url")
    if not reel_url:
        return jsonify({"error": "Missing url parameter"}), 400

    payload = {
        "url": reel_url,
        "ts": 1758550887025,
        "_ts": 1758529858437,
        "_tsc": 0,
        "_s": "b9c03d2f4cc78f71135790dff0d9f614030cebc60f404392580bb459ca312d61"
    }

    try:
        resp = requests.post(API_URL, headers=HEADERS, json=payload)
        resp.raise_for_status()  # Raises error if status != 200
        data = resp.json()

        result = {
            "author": data.get("meta", {}).get("username"),
            "title": data.get("meta", {}).get("title"),
            "thumbnail": data.get("thumb"),
            "video": (data.get("url") or [{}])[0].get("url")
        }

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
