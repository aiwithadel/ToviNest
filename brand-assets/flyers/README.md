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
