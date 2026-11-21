"""Everyone who replied to one of your posts, with their profile, so the skill can sort and answer them.
Needs X_BEARER_TOKEN (developer.x.com). ~$0.005 per reply read. Covers the last 7 days.
Usage: python3 xreplies.py <post link or id> [max=100]"""
import sys, os, re, json, urllib.request, urllib.parse
tok = os.environ.get("X_BEARER_TOKEN") or sys.exit("Set X_BEARER_TOKEN first.")
pid = re.findall(r"\d{10,}", sys.argv[1])[-1]; n = int(sys.argv[2]) if len(sys.argv) > 2 else 100
out, nxt = [], None
while len(out) < n:
    p = {"query": f"conversation_id:{pid} -is:retweet", "max_results": 100, "expansions": "author_id",
         "tweet.fields": "created_at,public_metrics,in_reply_to_user_id",
         "user.fields": "username,name,public_metrics,created_at,description"}
    if nxt: p["next_token"] = nxt
    req = urllib.request.Request("https://api.x.com/2/tweets/search/recent?" + urllib.parse.urlencode(p), headers={"Authorization": "Bearer " + tok})
    try: r = json.load(urllib.request.urlopen(req))
    except urllib.error.HTTPError as e: sys.exit(f"X API error {e.code}: {e.read().decode()[:200]}")
    us = {u["id"]: u for u in r.get("includes", {}).get("users", [])}
    for t in r.get("data", []):
        u = us.get(t["author_id"], {})
        out.append({"handle": u.get("username"), "followers": u.get("public_metrics", {}).get("followers_count"),
                    "account_created": u.get("created_at", "")[:10], "bio": u.get("description", ""),
                    "replied": t["created_at"], "text": t["text"], "link": f"https://x.com/{u.get('username')}/status/{t['id']}"})
    nxt = r.get("meta", {}).get("next_token")
    if not nxt: break
for o in out[:n]: print(json.dumps(o, ensure_ascii=False))
