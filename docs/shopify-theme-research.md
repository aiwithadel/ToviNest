# Tovi Nest: Shopify theme review & market research (Nov 14, 2026)

## 1. Review of the current theme (`shopify-theme/`, Dawn 16.1.1 + Tovi Nest brand layer)

| Area | Status | Notes |
|---|---|---|
| Menus / dropdowns / mobile drawer | **Fixed today** | Reported as "transparent, content shows through". `assets/tovi.css` now forces a solid background on the dropdown, mega menu, mobile drawer, search and country picker, with rounded corners, a shadow and a sage hover. Re-upload `tovinest-theme.zip`. If it still shows, send a screenshot plus the preview link. |
| Logo | Weak | Header shows a text wordmark fallback until a logo is uploaded (Theme settings → Logo). |
| Product imagery | Weak | Placeholders are drawn mat renders. Real photos of the assembled mats (RainBoho / Ash Starlight, top-down + lifestyle + baby on the mat) are the single biggest visual upgrade. |
| Product page | OK, generic | Dawn's product page is solid but plain: no bundle picker, no review stars, no "what's in the box" or comparison blocks. |
| Brand look | Good base | Fonts, palette, rounded shapes and custom sections (hero, offer, icon cards, compare, gift banner, FAQ) are in place and pass theme check (0 errors). |
| Conversion features | Partial | Sticky add-to-cart on mobile and cart upsell / free-shipping line are custom-built. Missing: native bundles, reviews, upsell inside the product form. |

**Verdict:** the current theme works and is on-brand, but Dawn is a "starter" theme. To look premium and playful like the category leaders, move to a premium kids-friendly theme and port our brand layer onto it.

## 2. What the play-mat leaders actually use (detected from their live storefronts, Nov 14, 2026)

| Brand | Category | Theme |
|---|---|---|
| Toddlekind | Premium play mats (direct competitor) | **Habitat** 13.0 (Fuel Themes) |
| Totter + Tumble | Premium play mats (direct competitor) | **Broadcast** 5.6 (Presidio) |
| Gathre | Leather / vegan play mats | **Symmetry** 7.1 (Clean Canvas) |
| Little Nomad | Play mats | **Dawn** 15.3 (heavily customized: the same base as ours) |
| Lovevery | Kids play kits | Shopify, custom theme (not detectable) |

## 3. Shortlist (Shopify Theme Store data, Nov 2026)

| Theme | Price | Rating | Why it fits | Watch-outs |
|---|---|---|---|---|
| **Broadcast** (Presidio) | $420 | 94% of 285 | Used by Totter + Tumble; playful presets (Broadcast, Relay, Airwave, Motif, Stellar); quick buy, sticky + slide-out cart, mega menu, swatches, tabs, badges; bundles via free Presidio+ app; v8.1.1 (Apr 2026) | Bundles need the add-on app |
| **Habitat** (Fuel Themes) | $360 | 97% of 64 | Used by Toddlekind; many custom sections and conversion templates; 5 presets; v15.0 (Oct 2026) | Smaller review base; no native bundles / free-shipping bar |
| **Symmetry** (Clean Canvas) | $420 | 94% of 392 | Used by Gathre; 70k+ stores; very stable | More fashion/catalog-oriented; no sticky ATC listed |
| **Be Yours** (RoarTheme) | $380 | 98% of 700 | Highest rated; v10 adds per-section color schemes | Beauty-oriented; no kids preset despite some blog claims |
| **Impact** (Maestrooo) | $400 | 85% of 200 | Bold single-product DTC look; sticky ATC | Lowest rating of the paid options |
| Horizon / Tinker (Shopify, free) | Free | 36% / 35% | New block-based architecture | Poorly reviewed; no bundles or free-shipping bar |
| Current Dawn + brand layer | Free | n/a | Already branded, works, 0 errors | Plain look; we build every feature ourselves |

## 4. Recommendation

1. **Pick: Broadcast ($420).** It's the theme a direct play-mat competitor runs, it's designed for kids and baby brands, it has the mobile conversion features we need (quick buy, sticky cart, slide-out cart, swatches, tabs), and it handles bundles (our 2 for $89.99) through Presidio+. **Runner-up: Habitat ($360)**, Toddlekind's choice, if you prefer its look or the lower price.
2. **Timing:** Black Friday is Nov 27, 13 days away. Don't switch themes the week before. Launch BFCM on the current fixed theme (re-upload the new zip), and in parallel try Broadcast and Habitat for free in the theme editor (Shopify lets you preview paid themes before buying). Migrate in early January, after the Dec 17 Christmas cutoff.
3. **Migration plan (≈ 1–2 days of dev):** port the brand layer (fonts, palette, icons, Dino art), rebuild the homepage sections with Broadcast's built-in sections, set up the 2-pack bundle in Presidio+, add a reviews app (Judge.me or Okendo), and swap in real product photography.
4. **Biggest wins regardless of theme:** real mat photos (top-down + lifestyle + baby on the mat), a reviews app with photo reviews, and a proper logo upload.

## Sources
- Theme Store pages: [Broadcast](https://themes.shopify.com/themes/broadcast), [Habitat](https://themes.shopify.com/themes/habitat), [Symmetry](https://themes.shopify.com/themes/symmetry), [Be Yours](https://themes.shopify.com/themes/be-yours), [Impact](https://themes.shopify.com/themes/impact), [Horizon](https://themes.shopify.com/themes/horizon), [Tinker](https://themes.shopify.com/themes/tinker)
- Roundups: [Meetanshi: best themes for baby & kids](https://meetanshi.com/blog/best-shopify-themes-for-baby-kids-stores/), [GemPages: themes baby stores use](https://gempages.net/blogs/shopify/shopify-themes-baby-store), [CommerceRank: toy store themes](https://www.commercerank.ai/guides/themes/best-toy-themes), [Ecommerce Platforms: Horizon themes guide](https://ecommerce-platforms.com/articles/shopify-horizon-themes)
- Competitor themes: detected from the `Shopify.theme` object on toddlekind.com, totterandtumble.com, gathre.com and littlenomad.com.
