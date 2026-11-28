# Writing brief: The Marketing School articles

Site: themarketingschool.com, a static site on Vercel. Evan Baker runs it. He's run paid media for 20+ years on Google, Meta, YouTube, TikTok and LinkedIn, has managed $200M+ in ad spend and served 150+ businesses, and teaches live classes twice a week. The business sells done-for-you ad management (the Done-For-You Ads plan is for businesses spending under $10k a month on ads; Full Agency is for $30k+ a month). Every buyer path ends at a free account review at /contact.

There are two content sections:
- **learn** (`/learn/<slug>`): tutorials for people learning to run ads themselves (students, solo marketers, owners doing it themselves). Teach for real. A reader should be able to follow the steps and do the thing. The page template adds an email signup box automatically, so don't pitch the agency in the body.
- **guide** (`/<slug>`): articles for business owners deciding how to get their ads run. Answer the question honestly. They can mention once, near the end and naturally, that The Marketing School offers a free account review. The template adds an offer box automatically.

## How to make a page
1. Write a JSON spec at `content/learn/<slug>.json` or `content/guides/<slug>.json`. The fields are documented at the top of `scripts/build.py`. Read that file first.
2. Render it with `python3 scripts/build.py page content/<dir>/<slug>.json`.
3. Do NOT run `build.py index`, git or deploy commands, and do NOT edit any other files. The coordinator does all of that.

Spec rules:
- `date` is "2026-11-28".
- `title` is 50–60 characters, keyword first. `description` is 140–158 characters. `card` is one short sentence for the hub card. `crumb` is a short label in sentence case, usually a question or topic. `eyebrow` is "Learn · Google Ads" (or the right platform/topic) for learn pages and "Guide · <Topic>" for guides.
- Start `body_html` with `<div class="tldr"><p><strong>Short answer:</strong> …</p></div>`, a 2–3 sentence direct answer. Search engines and AI answer engines quote this.
- Then 5–8 `<section>` blocks, each with an `<h2>` that people would actually search for (questions are good). Use `<h3>`, `<ol>`/`<ul>` for steps and checklists, `<strong>`, and a table where it helps (`<div class="table-wrap"><table>…</table></div>`). Aim for 1,200–1,800 words of body.
- Write 3–5 `faqs` with real, specific answers. Plain text, or simple inline HTML in `a`.
- Give 3–4 `related` links. Use only URLs that exist or are being written in this batch:
  - Learn: /learn/how-to-set-up-google-ads, /learn/google-ads-negative-keywords, /learn/google-ads-search-terms-report, /learn/meta-ads-for-beginners, /learn/meta-ads-creative-testing, /learn/conversion-tracking-basics, /learn/how-to-calculate-customer-acquisition-cost, /learn/how-to-write-ad-copy, /learn
  - Guides: /should-i-hire-an-ad-agency-or-learn-ads-myself, /how-much-does-an-ad-agency-cost, /questions-to-ask-before-hiring-an-ad-agency, /signs-your-ads-are-wasting-money, /google-ads-vs-meta-ads, /how-much-should-i-spend-on-ads, /can-ai-run-my-google-ads, /done-for-you-ads, /guides
  - Services: /google-ads-management, /meta-ads-management, /tiktok-ads-management, /linkedin-ads-management, /ai-ads-management, /contact
  - Also link 2–4 of these inside the body copy where it's natural (internal links matter for SEO).

## Voice
Plain, direct, practical, like an experienced operator talking to a smart friend. Use short sentences and second person. No hype words ("unlock", "supercharge", "game-changer", "in today's digital landscape"). No em-dash-heavy writing. Every section should give the reader something they can use: a number to check, a step, a rule of thumb, a mistake to avoid.

## Accuracy (most important)
- Platform features, names and settings change. Use WebSearch to confirm anything current before stating it, such as campaign types, objective names, match types, Advantage+ naming, Consent Mode, Conversions API, Enhanced Conversions, or minimum budgets. Avoid exact click paths ("click the blue button at top right"). Describe where things live in general terms.
- Do NOT invent statistics, benchmarks, studies, client stories, testimonials or quotes. If you use an industry number, it must come from a source you found, and you say it's a rough range (e.g., "benchmarks vary widely by industry"). Rules of thumb framed as Evan's practice are fine ("A rule of thumb we use: …").
- Don't state The Marketing School prices. The only offer facts you may use are the ones in this brief.
- No HTML outside the body (the template handles head, nav and footer). No `<h1>` in the body. No inline styles. No images.

When you're done, reply with the slugs you wrote and a one-line summary each, plus anything you weren't sure was accurate.
