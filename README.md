# claude skills for getting customers

free claude skills for builders who need users, by [@andrebarbera_](https://x.com/andrebarbera_)

## first-customers

turns the people engaging with your X posts into paying customers. it learns what you sell, qualifies everyone who replied against your product, keeps a lead sheet, and drafts every message: public replies that start real conversations, a DM that opens with something useful, the offer with an incentive, and specific follow-ups. finds new buyers too if you're small

**install**

1. download the [`first-customers`](first-customers) folder (SKILL.md + scripts)
2. put it in `~/.claude/skills/first-customers/`
3. optional but recommended: add an X API Bearer Token (`export X_BEARER_TOKEN=...`) so it searches X on its own
4. open claude code and say "get me my first customers for" + your product link + your X handle

it never posts or DMs for you. you read everything and send it yourself

## buyer-finder

finds people on X asking for what you built, scores them for buying intent and writes a reply for each one

**install**

1. download [`buyer-finder/SKILL.md`](buyer-finder/SKILL.md)
2. put it in `~/.claude/skills/buyer-finder/SKILL.md`
3. open claude code and say "find buyers for" + your app link

it never posts anything for you. you read the replies and send the ones you like
