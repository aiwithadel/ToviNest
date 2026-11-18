# B2B email flyers: classrooms and pediatric clinics

| File | Use |
|---|---|
| `tovinest-*-flyer-email.jpg` (1200×1600, ~220 KB) | **Inline in the email body.** Insert it at 600 px wide so it stays sharp on retina screens. |
| `tovinest-*-banner-email.jpg` (1200×780, ~110 KB) | A short header at the top of the email body, with the text written underneath. |
| `tovinest-*@2x.png` (2400 px) | **Attachment** or print master. |

Alt text for inline use: "Tovi Nest Moon Walkers playmat in RainBoho and Ash Starlight for classrooms / waiting rooms. Free visit and room measuring in Sterling, VA."

To rebuild, run `cd _src && python3 flyers.py && node render.js && python3 post.py`.

Rules followed:
- No prices.
- No carton photos.
- Only official Dino and Dima images and real flat-lays.
- No safety guarantees; the footer says "Always supervise children during play."

## Flyer for parent and community groups

| File | Use |
|---|---|
| `tovinest-community-feed-share.jpg` (4:5) | Facebook and WhatsApp groups, and posts. |
| `tovinest-community-story-share.jpg` (9:16) | Status and stories. |
| `tovinest-community-*@2x.png` | Print master. |

Ordering is online only, at tovinest.com. The QR code leads to https://tovinest.com.

To rebuild, run `cd _src && python3 community.py && node render.js && python3 post.py`. This needs `pip install segno`.

## Gift-a-Mat program: outreach to practices

| File | Use |
|---|---|
| `tovinest-gift-program-flyer-email.jpg` (1200×1600) | Inline in an outreach email to pediatricians, dentists, OB/GYN, therapy and childcare. |
| `tovinest-gift-program-banner-email.jpg` (1200×780) | Short header for the email. |
| `tovinest-gift-card-front@2x.png` / `-back@2x.png` (7×5 in at about 400 dpi) | Printable gift card, front and back. |

Before printing:
- Replace "Your Practice Name" in `_src/gift.py` (`card_front_inner(..., practice=...)`).
- Replace `XXXX-XXXX-XXXX-XXXX` with a real Shopify gift-card code.

Volume pricing is "ask us": no numbers are invented.

## B2B outreach (41 contacts): 5 audience flyers, 1500×975

| # | File | Audience |
|---|---|---|
| 1 | `tovinest-b2b-1-hospitals-email.jpg` | Hospitals & maternity units |
| 2 | `tovinest-b2b-2-foundations-email.jpg` | Hospital foundations, ladies boards, auxiliaries |
| 3 | `tovinest-b2b-3-dentists-email.jpg` | Pediatric dentists |
| 4 | `tovinest-b2b-4-kids-gyms-email.jpg` | Kids gyms & play spaces |
| 5 | `tovinest-b2b-5-music-classes-email.jpg` | Kids music classes |

Every flyer has the same footer: "Moon Walkers Premium EVA Playmat · CPC/CPSIA tested · tovinest.com/catalog". That link currently redirects to the wholesale catalog PDF.

There is an @2x PNG (3000×1950) of each for attachments.

To rebuild, run `cd _src && python3 b2b41.py && node render.js && python3 post.py`.

## Facebook groups and Marketplace (square 1080×1080, English and Arabic)

`tovinest-social-{en,ar}-{1-hero,2-rainboho,3-ash-starlight,4-how-to-order}-share.jpg`

To rebuild, run `cd _src && python3 social.py && node render.js && python3 post.py`. The Arabic version uses the Cairo font (`fonts/Cairo-*.woff2`, OFL).
