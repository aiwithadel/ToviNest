# Tovi Nest Shopify theme

An Online Store 2.0 theme built on **Dawn 16.1.1** (Shopify, Nov 2026), branded for Tovi Nest: sage / sky / coral /
mustard / blush on cream, self-hosted Fredoka (headings) and Nunito (body), rounded shapes, mobile first.

**Upload:** Online Store → Themes → Add theme → Upload zip file → `tovinest-theme.zip` (theme root at the top of the zip).

## What's in it
| Area | Details |
|---|---|
| Homepage (`templates/index.json`) | Announcement bar → Hero (`tovi-hero`) → Featured product (`premium-eva-playmat`, button swatches) → 2-for-$89.99 offer (`tovi-offer`) → Why parents love it (`tovi-features`) → RainBoho vs Ash Starlight (`tovi-compare`) → Holiday gift banner (`tovi-gift-banner`) → FAQ → "Notes from the nest" signup |
| Product page (`templates/product.json`) | Button variant picker, specs / care / shipping & returns tabs, bundle link, "Always supervise…", icon cards, **mobile sticky add-to-cart** (`tovi-sticky-atc`) |
| Cart drawer | Cart type set to Drawer, plus `snippets/tovi-cart-upsell.liquid`: free-shipping progress bar (when a threshold is set) and "Add a second mat: 2 for $89.99" when one single mat is in the cart |
| Header / footer | Wordmark fallback until you upload a logo; footer with hello@tovinest.com, Shop + Help menus, payment icons, "© 2026 Tovi Nest" |
| Placeholders | Every image setting is an `image_picker`. Until you upload, sections use built-in brand art in `assets/tovi-*.webp` (Dino + box, mat renders, Dino) |
| Theme settings → **Tovi Nest** | Single + 2-pack product pickers, free-shipping threshold (0 = off), upsell and shipping-note text |

Custom files are all prefixed `tovi-`. Dawn files changed: `layout/theme.liquid` (renders the brand styles),
`sections/header.liquid` (wordmark fallback), `sections/footer.liquid` (copyright), `snippets/cart-drawer.liquid` (upsell),
`config/*`, `templates/index.json`, `templates/product.json`, `sections/header-group.json`, `sections/footer-group.json`.

## Store setup checklist
1. **Products** (the handles must match):
   - `premium-eva-playmat`: $49.99, option **Design** = `RainBoho`, `Ash Starlight`. For colour swatches, connect the option to a
     category metafield / add swatches in the product's option settings; otherwise buttons are shown.
   - `playmat-2-pack`: $89.99, option **Design** = `Two RainBoho`, `Two Ash Starlight`, `Mix`.
2. **Menus:** `main-menu` (header + footer "Shop") and `footer` (footer "Help": FAQ, Shipping, Returns, Contact).
3. **Images:** upload in the theme editor: hero (Dino with the RainBoho box), compare images, gift banner (Dino, plus
   optionally his friend), logo (Theme settings → Logo).
4. **Policies:** add a 30-day return policy (unused items) in Settings → Policies; the footer links to it.
5. **Free shipping (optional):** set the threshold in Theme settings → Tovi Nest *and* create the matching free-shipping
   rate in Settings → Shipping.
6. **Holiday banner:** it switches to the "after" text automatically after the cutoff date (2026-12-17).

## Validate
```bash
shopify theme check --path shopify-theme
```
0 errors. The 9 remaining warnings are the same 9 that stock Dawn 16.1.1 reports (UndefinedObject `scheme_classes` /
`continue`, VariableName, UnusedAssign, LiquidComplexity in `main-product`, OrphanedSnippet `quick-order-product-row`).
They're left as-is so Dawn updates merge cleanly.

## Rebuild the zip
```bash
cd shopify-theme && rm -f tovinest-theme.zip && zip -qr tovinest-theme.zip assets config layout locales sections snippets templates
```
