from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)

@app.route("/sre", methods=["GET"])
def sre_api():
    try:
        # Get Instagram URL from query params
        keyword = request.args.get("url")
        if not keyword:
            return jsonify({"error": "Missing 'url' parameter"}), 400

        url = "https://lgs.pubpowerplatform.io/sre"

        headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",  # <-- fixed
            "priority": "u=1, i",
            "sec-ch-ua": "\"Chromium\";v=\"140\", \"Not=A?Brand\";v=\"24\", \"Google Chrome\";v=\"140\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "Referer": "https://toolzu.com/"
        }

        payload = {
            "level": "client_logs",
            "message": "js_user_searchs",
            "keyword": keyword,
            "domain": "toolzu.com",
            "device": "pc",
            "operating_system": "Windows",
            "domainId": 12531,
            "pageUrl": "https://toolzu.com/downloader/instagram/video/",
            "jsVer": "1.0.6",
            "cacheTime": int(time.time()),
            "userAgent": request.headers.get("User-Agent", "Flask-API")
        }

        response = requests.post(url, headers=headers, json=payload)

        content_type = response.headers.get("content-type", "")
        result = response.json() if "application/json" in content_type else response.text

        return jsonify({
            "status": response.status_code,
            "response": result
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
