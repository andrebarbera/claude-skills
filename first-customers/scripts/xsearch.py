"""Search X for people posting a problem, using your own X API key (pay-per-use, ~$0.005 per post read).
Setup once: get a Bearer Token at developer.x.com, then: export X_BEARER_TOKEN=...
Usage: python3 xsearch.py "<search>" [max=25]
Prints JSON: one line per post with handle, followers, account age, post text, link, time."""
import sys, os, json, urllib.request, urllib.parse
tok = os.environ.get("X_BEARER_TOKEN")
if not tok: sys.exit("Set X_BEARER_TOKEN first (developer.x.com → your app → Keys and tokens → Bearer Token).")
q = sys.argv[1]; n = max(10, min(int(sys.argv[2]) if len(sys.argv) > 2 else 25, 100))
if "lang:" not in q: q += " lang:en"
if "-is:retweet" not in q: q += " -is:retweet"
params = {"query": q, "max_results": n, "expansions": "author_id",
          "tweet.fields": "created_at,public_metrics,note_tweet",
          "user.fields": "username,name,public_metrics,created_at,description,verified"}
req = urllib.request.Request("https://api.x.com/2/tweets/search/recent?" + urllib.parse.urlencode(params),
                             headers={"Authorization": "Bearer " + tok})
try: r = json.load(urllib.request.urlopen(req))
except urllib.error.HTTPError as e: sys.exit(f"X API error {e.code}: {e.read().decode()[:200]}")
users = {u["id"]: u for u in r.get("includes", {}).get("users", [])}
for p in r.get("data", []):
    u = users.get(p["author_id"], {})
    print(json.dumps({"handle": u.get("username"), "name": u.get("name"),
        "followers": u.get("public_metrics", {}).get("followers_count"),
        "account_created": u.get("created_at", "")[:10], "bio": u.get("description", ""),
        "posted": p["created_at"], "text": (p.get("note_tweet") or {}).get("text", p["text"]),
        "link": f"https://x.com/{u.get('username')}/status/{p['id']}"}, ensure_ascii=False))
