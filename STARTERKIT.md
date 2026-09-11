# STARTERKIT — Routes Des Vins website

> **Lees dit volledig voor je ook maar één regel aanpast.** Dit document bundelt alles wat uit
> eerdere sessies, fouten en feedback geleerd is. Het doel: geen tijd meer verliezen aan dingen
> die we al weten, en geen fouten meer herhalen die we al eens gemaakt hebben.
>
> _Laatst bijgewerkt: 9 september 2026_

---

## 0. TL;DR — de 10 belangrijkste regels

1. **De git-getrackte bestanden in de projectroot zijn de waarheid.** De map `website/` is een verwarrende kopie — negeer ze, bewerk ze niet.
2. **`briefing.md`, `contentplan.md` en delen van `CLAUDE.md` zijn VEROUDERD** (ze beschrijven het oude 5-landen-model, oude prijzen €30/45/55, capaciteit 30, en een `frontend-design` skill die hier niet bestaat). Gebruik ze niet als bron voor content of prijzen.
3. **`node` bestaat niet op deze machine.** `serve.mjs` en `screenshot.mjs` werken NIET. Serveren = `python3 -m http.server 3000`. Screenshotten = Python + Playwright.
4. **Alle tekst loopt via `translations.js`** (NL + FR, ~190 sleutels). Elke tekstwijziging = daar, in BEIDE talen.
5. **Anti-FOUC regel:** de hardgecodeerde tekst in de HTML van een `data-i18n`-element moet exact de NL-vertaling zijn. Wijzig je de NL-sleutel, wijzig dan mee de fallback-tekst in élke HTML-pagina waar die sleutel voorkomt.
6. **NL/FR-pariteit is heilig.** Elke nieuwe sleutel bestaat in `nl:` én `fr:`. Geen enkele mag ontbreken.
7. **Nav + footer staan hardgecodeerd in elke pagina** (geen includes). Wijzig je er één, wijzig ze overal (11 pagina's).
8. **Mobiel overflow is de #1 terugkerende bug.** Test elke wijziging op 390px breed. Geen horizontale scroll, niets buiten de kaart.
9. **Nieuwe afbeeldingen → in `fotos/` (kleine letter) én committen.** Anders breken ze op deploy (is al eens gebeurd).
10. **Kleuren: enkel de tokens uit `styles.css`.** Nooit standaard Tailwind-kleuren, nooit bordeaux/goud.

---

## 1. Wat is dit project

| | |
|---|---|
| **Wat** | Statische, tweetalige (NL/FR) website voor **Routes Des Vins** — een wijnbelevingsevent |
| **Event** | 20 november 2026, Gent |
| **Concept (huidig)** | Een reis langs **3 "wijnhandelaars/wijnhuizen"**, elk gekoppeld aan één tijdslot/formule. Bezoeker kiest een tijdslot, krijgt een boarding pass + wijnpaspoort, en een sommelier gidst door de wijnen. Reismetafoor ("zonder vliegticket, wel een boarding pass"). |
| **Concept (oud, VERLATEN)** | 5 wijnlanden wereldwijd + formules Classic/Sunset/Grand Cru gekoppeld aan doelgroepen (student/prof/expert). Dit staat nog in `briefing.md`/`contentplan.md` — **niet gebruiken.** |
| **Organisatie** | Emiel Maes, Arnaud Roegiers, Louis Roosens, Matteo Van Gulik — studenten Artevelde Hogeschool Gent |
| **Tickets** | Extern via Stamhoofd: `https://shop.stamhoofd.be/routes-des-vins` (één link voor alle tijdsloten) |
| **Contact** | emiel@routesdesvins.com · Instagram @routes.des.vins |
| **Tech** | Handgeschreven HTML/CSS/JS. Geen build, geen framework, geen dependencies. Google Fonts via CDN. |

### Huidige feiten (live waarden — check altijd `translations.js` als bron)

| Formule | i18n-prefix | Naam nu | Prijs | Tijdslot |
|---|---|---|---|---|
| 1 | `classic_*` | Handelaar 1 | €39 | 16u30–19u00 |
| 2 | `sunset_*` | Handelaar 2 → **Wijndomein Waes** (bevestigd, nog te verwerken) | €45 | 18u30–21u00 |
| 3 | `grandcru_*` | Handelaar 3 | €29 | 20u30–23u00 |

- Max. **45** personen per tijdslot (was ooit 30 — oude waarde dook nog op in `tickets.html`, is gefixt).
- Countdown mikt op `2026-11-20T15:30:00` (in `translations.js`, onderaan).
- Regio's van Handelaar 1 en 3 zijn nog **niet** bekend. Handelaar 2 = Wijndomein Waes (zie `voorstel-wijndomein-waes.md`).

---

## 2. ⚠️ Verouderde / misleidende bronnen — NIET op vertrouwen

| Bestand | Probleem |
|---|---|
| `briefing.md` (root + `website/`) | Beschrijft het oude 5-landen-model, "5 wijnregio's", doelgroep-gekoppelde formules. Alleen de secties **Huisstijl** (kleuren/fonts) en **Tone of Voice** zijn nog bruikbaar. |
| `website/contentplan.md` | Volledig oud model: 5 landen (Frankrijk/Italië/VS/Chili/Libanon), prijzen €30/45/55, capaciteit 30, doelgroepen student/prof/expert, 10% korting Grand Cru. **Alles achterhaald.** |
| `CLAUDE.md` (root + `website/`) | Zie sectie 4. De regels over `frontend-design` skill, `node serve.mjs`, `node screenshot.mjs` en Windows-Puppeteer-paden (`C:/Users/nateh/...`) kloppen niet voor deze machine. De **Anti-Generic Guardrails** en **Brand Assets**-secties zijn wél geldig. |
| `Partnerovereenkomst Routes Des Vins.pdf` | Juridisch, niet voor de site. |
| `Begroting/`, `Pitch/` | Interne docs, niet voor de site. |

**Vuistregel:** feiten haal je uit `translations.js` en de live HTML, niet uit de markdown-docs.

---

## 3. Repo- en bestandsstructuur

### 3.1 Wat live gaat (git-getrackt, in projectroot)

```
index.html          Home: hero, countdown, USP's, route-teaser, mini-formulekaarten, sponsor
event.html          Het Event: concept, stappenplan (6 stappen), boarding pass + wijnpaspoort mockup
route.html          De Route: route-map + 3 handelaarkaarten (nu grotendeels placeholder)
formules.html       Formules: 3 formulekaarten + vergelijkingstabel
tickets.html        Tickets: Stamhoofd-CTA, prijskaarten, stats
faq.html            FAQ: accordion, 4 categorieën
over-ons.html       Over Ons: verhaal, team (4 leden, klikbare bio's), kernwaarden
steun-ons.html      Steun ons: gepersonaliseerde kurkentrekker, sponsor-oproep
privacybeleid.html  Legal
voorwaarden.html    Legal (incl. terugbetaling)
cookiebeleid.html   Legal
styles.css          Volledig design system (tokens + componentklassen)
translations.js     i18n-data (nl/fr) + alle client-side JS (taal, scroll-reveal, nav, countdown, FAQ)
flyer.html          STANDALONE promo/flyer met QR-code — niet in de nav, andere structuur, laden apart
fotos/              Alle beeld dat de site gebruikt (kleine letter!)
```

Andere getrackte bestanden: `pw_test.py` (Playwright visuele test), `serve.mjs` + `screenshot.mjs` (Node — **werken hier niet**, zie sectie 5).

### 3.2 Wat je NIET aanraakt

- **`website/`** — een volledige kopie van de site (momenteel identiek aan root voor de kernbestanden) die **niet in git zit**. Bron van verwarring. Aanbeveling: aan Emiel vragen of die weg mag. Tot dan: alles in de **root** bewerken, nooit in `website/`.
- **`Foto's/`** (hoofdletter + apostrof) — ruwe/onbewerkte assets. De site laadt uit `fotos/`. Nieuw beeld: verwerk het, zet het in `fotos/`, commit het.
- `temporary screenshots/`, `pw_screenshots/`, `node_modules/` — gitignored.

### 3.3 Git & deploy

- Remote: `github.com/emielmaes1104-hub/Routes-Des-Vins`, branch `main`.
- ⚠️ **Security:** `.git/config` bevat momenteel een GitHub Personal Access Token in platte tekst in de remote-URL. Aanraden aan Emiel: die token roteren en een credential helper gebruiken. **Nooit die token in output, commits of docs plakken.**
- **Deploymechanisme is niet bevestigd** (geen `vercel.json`/`netlify.toml` in de repo). Vraag Emiel hoe de site live komt vóór je aannames doet over build/deploy-paden.
- Commit-conventie: zoals in de history — beknopte imperatieve titel, bullet-body met wat & waarom. Eindig met:
  `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`
- Werk op een aparte branch als je niet expliciet toestemming hebt om op `main` te committen. Commit/push enkel als Emiel het vraagt.

---

## 4. `CLAUDE.md` — wat klopt en wat niet

`CLAUDE.md` (root) zegt "Invoke the `frontend-design` skill before writing any frontend code". **Die skill bestaat niet in deze omgeving.** Beschikbare relevante skills: zie sectie 6.

| CLAUDE.md-regel | Status |
|---|---|
| `frontend-design` skill eerst | ❌ Bestaat niet. Volg in plaats daarvan de Anti-Generic Guardrails hieronder + `artifact-design` skill-principes indien nodig. |
| `node serve.mjs` op :3000 | ❌ Geen node. Gebruik `python3 -m http.server 3000`. |
| `node screenshot.mjs` | ❌ Geen node/puppeteer. Gebruik Python Playwright. |
| Puppeteer op `C:/Users/nateh/...` | ❌ Windows-pad, verkeerde machine. |
| Altijd op localhost screenshotten, nooit `file://` | ✅ Geldig. |
| 2+ vergelijkingsrondes, wees specifiek over pixels | ✅ Geldig. |
| Brand Assets-map checken vóór design | ✅ Geldig (`website/RDV brandkit.pdf`, `Foto's/`). |
| Anti-Generic Guardrails (kleuren/schaduw/typografie/animatie/focus states) | ✅ Volledig geldig — zie sectie 7.4. |
| Geen `transition-all`, geen standaard Tailwind-blauw/indigo | ✅ Geldig (site gebruikt sowieso geen Tailwind). |

---

## 5. Lokale workflow die ECHT werkt

### 5.1 Serveren

```bash
# Vanuit de projectroot:
python3 -m http.server 3000
```

- Draait er al één op :3000? Check met `lsof -ti:3000`. Start geen tweede.
- De site is puur statisch — geen server-side logica nodig. Elk `.html`-bestand is direct bereikbaar (`http://localhost:3000/route.html`).
- **Nooit** een `file:///`-URL screenshotten (fonts/CSS/paden breken).

### 5.2 Screenshotten (Python Playwright — `pw_test.py` werkt, node niet)

- `python3 pw_test.py` draait een volledige visuele test over 7 pagina's × 3 viewports (desktop 1440×900, tablet 768×1024, mobiel 390×844), forceert alle `.reveal`-elementen zichtbaar, schrijft naar `pw_screenshots/` + `report.json`, en print gevonden layout-problemen (nav-hoogte, hamburger-zichtbaarheid, horizontale overflow, knoppen/kaarten buiten viewport, ontbrekende footer/countdown).
- Voor een snelle losse screenshot: schrijf een klein Playwright-scriptje naar de scratchpad (viewport zetten, `goto`, kort scrollen voor de IntersectionObserver, `.reveal`→`visible` forceren, `screenshot`). Model op `pw_test.py`.
- **`pw_test.py` test nog de oude 7-pagina-lijst** — steun-ons en de legal-pagina's zitten er niet in. Breid uit als je die pagina's raakt.
- Lees de PNG's daarna met de Read-tool en vergelijk concreet ("titel is 32px, referentie ~24px").

### 5.3 Wat je NIET moet proberen

- `node`, `npm`, `npx` installeren of aanroepen — niet aanwezig, niet nodig.
- `serve.mjs` / `screenshot.mjs` draaien.
- De site "builden" — er is niks te builden.

---

## 6. Skills

Beschikbaar en relevant:

| Skill | Wanneer |
|---|---|
| `artifact-design` | Vóór je visuele/design-keuzes maakt — fundamentele design-principes. Nuttig als naslag ook al bouwen we geen Artifact. |
| `design` | Enkel als Emiel een los mockup/canvas wil om visueel te tweaken. Niet voor de echte site-bestanden. |
| `code-review` / `simplify` | Na een grotere wijziging, om de diff na te kijken. |
| `security-review` | Bij twijfel over de changes op de branch. |
| `dataviz` | Alleen als er ooit een grafiek/visualisatie bijkomt (nu niet). |

**Niet** beschikbaar: `frontend-design` (ondanks wat `CLAUDE.md` zegt).

---

## 7. Architectuur van de site

### 7.1 i18n-systeem (`translations.js`)

- `window.RDV.translations = { nl: {...}, fr: {...} }` — ~190 sleutels per taal.
- Een "language engine" (IIFE onderaan `translations.js`) doet op `DOMContentLoaded`:
  - `document.querySelectorAll('[data-i18n]')` → zet `el.innerHTML = t(key)` (of `.placeholder` voor inputs).
  - `[data-i18n-href]` → zet het `href`-attribuut.
  - onthoudt de taal in `localStorage` onder `rdv-lang` (default `nl`).
  - `.lang-btn`-knoppen (in nav + mobiele nav) togglen de taal.
- `t(key)` valt terug op NL, dan op de sleutelnaam zelf.
- **`innerHTML`, niet `textContent`** → vertaalwaarden mogen HTML bevatten (bv. `home_route_h2: '3 wijnhuizen,<br>3 werelden'`). Hou HTML in vertaalwaarden minimaal en identiek qua structuur tussen NL/FR.
- **`data-i18n` overschrijft de VOLLEDIGE inhoud van het element.** Moet een deel van een zin/kaart vertaald worden en een deel niet (bv. een badge naast de naam), zet `data-i18n` dan op een **binnenste span** die enkel die tekst bevat. Voorbeeld: `tickets.html` prijskaart — `data-i18n="sunset_name"` staat op een inner `<span>`, niet op de `.pc-name` die ook de "POPULAIR"-badge bevat.

### 7.2 Anti-FOUC regel (belangrijk, is al eens misgelopen)

`translations.js` laadt onderaan de `<body>` **zonder `defer`** en draait pas op `DOMContentLoaded`. Tot dan toont de browser de **hardgecodeerde** tekst in de HTML. Daarom:

> **De letterlijke tekst tussen de tags van een `data-i18n`-element moet exact gelijk zijn aan de `nl:`-waarde van die sleutel.**

Wijzig je een NL-vertaling, dan pas je in **élke** HTML-pagina waar die sleutel voorkomt ook de fallback-tekst aan. Anders zie je bij het laden even de oude tekst → flikkering, of erger, verkeerde tekst als JS faalt.

Handig om te checken welke pagina's een sleutel gebruiken:
```bash
grep -rn 'data-i18n="SLEUTELNAAM"' *.html
```

### 7.3 CSS design system (`styles.css`)

**Design tokens (`:root`) — gebruik uitsluitend deze:**

```
--c-forest:  #516F5A   primaire kleur, CTA's, accenten
--c-sage:    #8CA180   secundair, focus-outlines
--c-muted:   #95AA9F   gedempt (footer tagline)
--c-light:   #C6D4B9   subtiele achtergrond, badges, highlight-marker
--c-offwhite:#E0DED3   randen, dividers, neutrale vlakken
--c-cream:   #F1F4EC   hoofd-paginablauw… -achtergrond
--c-dark:    #1C2A21   donkere secties, footer, page-headers
--c-dark-mid:#2D3F32   hover op donkere knoppen, gradients
--c-text:    #2A3828   bodytekst
--c-text-light:#526356 gedempte tekst (WCAG-veilig — was ooit te licht, is gefixt)

--font-display: 'Chau Philomene One'   titels (h1-h4), prijzen, cijfers
--font-body:    'DM Sans'              alles lopend
--font-accent:  'Playfair Display' italic  slogans, taglines, handgeschreven gevoel

--nav-h: 72px
--ease-spring / --ease-out / --ease-in-out   gebruik deze, geen ad-hoc cubic-beziers
--shadow-sm / -md / -lg / -xl   groen-getinte gelaagde schaduwen — gebruik deze, geen platte shadow
```

**Belangrijke componentklassen (bestaan al — hergebruik, niet heruitvinden):**
`.nav` `.nav-links` `.nav-lang` `.nav-cta` `.nav-hamburger` `.nav-mobile` ·
`.btn-primary` `.btn-secondary` `.btn-ghost` ·
`.section` `.section-sm` `.container` `.container-sm` `.section-eyebrow` ·
`.card` `.card-sage` `.country-card` `.formula-card` (`.featured`) `.formula-badge` `.usp-card` `.usp-grid` `.team-card` ·
`.countdown-*` `.step-item` `.step-number` `.faq-item` `.faq-trigger` `.faq-body` ·
`.footer` `.footer-top` `.footer-links` `.footer-label` `.footer-bottom` ·
`.boarding-pass` (`-main` / `-stub`) `.passport-cover` ·
`.data-table` `.price-display` (`.on-dark`) `.tag` `.highlight` `.divider` `.urgency-banner` ·
`.reveal` `.reveal-left` `.reveal-scale` + `.delay-1..6` ·
`.grid-2/3/4` `.text-center` `.text-muted` `.text-forest` `.mt-*` `.mb-*`

**Responsive breakpoints in gebruik:** 480px (fijne mobiel-fixes), 600px, 768px (hoofd-mobiel: grids → 1 kolom, footer → 1 kolom), 900px (nav → hamburger), 1024px.

Page-specifieke CSS staat in een `<style>`-blok in de `<head>` van díe pagina. Generieke dingen horen in `styles.css`.

### 7.4 Anti-Generic Guardrails (uit CLAUDE.md — blijven gelden)

- **Kleuren:** enkel de tokens hierboven. Nooit standaard Tailwind (`indigo-500` etc.). Nooit bordeaux of goud (bewuste keuze — organische, natuurlijke stijl i.p.v. klassieke wijnbranding).
- **Schaduwen:** `var(--shadow-*)`, nooit een platte `box-shadow`.
- **Typografie:** display-font ≠ body-font (is al zo). Strakke tracking op grote titels (`-0.02` tot `-0.03em`), royale line-height (1.7) op body.
- **Animaties:** enkel `transform` en `opacity`. **Nooit `transition-all`.** Spring-easing via de tokens.
- **Interactieve elementen:** elke klikbare heeft hover, `:focus-visible` (outline `--c-sage`) én `:active`. Geen uitzonderingen — is al eens vergeten op de bio-toggle en moest achteraf gefixt.
- **Beeld:** gradient-overlay op foto's (`linear-gradient(to bottom, transparent, rgba(20,35,24,.45))`) voor leesbaarheid en consistentie.

### 7.5 JavaScript (allemaal in `translations.js`, als losse IIFE's)

Language engine · scroll-reveal (IntersectionObserver, `threshold 0.1`, unobserve na eerste keer) · nav-scroll (`.scrolled` na 20px) · mobiele nav (hamburger toggelt `.open` + `body overflow hidden`) · countdown (elke seconde) · FAQ-accordion (één tegelijk open, `aria-expanded` + `.open` op `.faq-body`).

`over-ons.html` heeft één eigen inline `<script>` (`toggleBio`) — de enige pagina-specifieke JS.

Nieuwe interactie? Voeg een nieuwe IIFE toe in `translations.js` in dezelfde stijl (wrap in `DOMContentLoaded`, guard met `if (!el) return;`).

---

## 8. Terugkerende fouten — checklist "niet nog eens"

Uit de git-history en eerdere sessies:

| # | Fout | Preventie |
|---|---|---|
| 1 | **Mobiele overflow op prijskaarten** (naam+badge naast prijs+CTA → prijs/knop buiten de kaart, `b5bf647`). Ook algemener: kaarten/knoppen die op 390px buiten de viewport vallen. | Test elke wijziging op 390px. Laat rijen wrappen of stapelen `< 480px`. Draai `pw_test.py` — die vangt horizontale overflow. |
| 2 | **Stale cijfers blijven staan** — capaciteit toonde 30 i.p.v. 45 op één plek na een globale wijziging (`9a7ad05`). Zelfde risico met prijzen/tijdsloten. | Na een cijferwijziging: `grep -rn` op de oude én nieuwe waarde over álle `.html` + `translations.js` (NL én FR). |
| 3 | **FOUC / desync** tussen hardgecodeerde HTML-tekst en de `nl:`-vertaalwaarde (`2e7cd41` moest dit expliciet syncen). | Zie sectie 7.2. HTML-fallback == NL-waarde, in elke pagina. |
| 4 | **NL/FR uit sync** — dode sleutels, ontbrekende FR-sleutels (`2e7cd41` ruimde 260→ sleutels op). | Elke nieuwe/gewijzigde sleutel: NL + FR samen. Check: `nl:` en `fr:` moeten dezelfde sleutelset hebben. |
| 5 | **Gebroken afbeeldingen op deploy** — `fotos/` ontbrak op het deploypad; alle beelden stuk (`2e7cd41`). | Nieuw beeld → in `fotos/` (kleine letter), relatief pad (`fotos/naam.jpg`), en **committen** (geen los untracked bestand). |
| 6 | **Nav/footer maar op één pagina aangepast.** Ze staan hardgecodeerd in alle 11 pagina's. | Wijzig nav of footer? Doe het in élke pagina. `grep -l 'nav-links' *.html` om de lijst te krijgen. Verifieer met screenshots van 2-3 pagina's. |
| 7 | **Em-dashes / typografische rommel** in copy (`5090319` verwijderde em-dash uit `hero_body` NL+FR). | Gebruik gewone leestekens, consistente spatiëring. Geen `—` in vertaalwaarden tenzij bewust. |
| 8 | **WCAG-contrast** — `c-text-light` was te licht, lage-opacity witte tekst op donker faalde (`88eb8ef`). | Gebruik de gefixte tokens. Nieuwe kleurcombo's op donker: mik op contrast ≥ 4.5:1 voor tekst. |
| 9 | **Ontkoppelde velden weer koppelen** — `route.html` "Sfeer" was gekoppeld aan "live muziek"-copy; moest losgekoppeld toen formules herschikt werden (`88eb8ef`). | Als een tekst op 2 plaatsen semantisch verschilt, geef ze aparte sleutels (niet hergebruiken "omdat het toevallig hetzelfde is"). |
| 10 | **Werken in `website/`** i.p.v. root. | Root only. |
| 11 | **Node-tooling proberen draaien.** | Python-workflow (sectie 5). |

---

## 9. Vaste checklist vóór je zegt "klaar"

- [ ] Wijziging in **NL én FR** in `translations.js`.
- [ ] HTML-fallbacktekst == NL-vertaalwaarde, in **elke** pagina die de sleutel gebruikt.
- [ ] `grep -rn` op oude waarden (namen/prijzen/tijden/capaciteit) — niks blijft staan.
- [ ] Nav + footer: als aangeraakt, in **alle 11 pagina's** consistent.
- [ ] Nieuwe afbeeldingen in `fotos/`, gecommit, correct relatief pad.
- [ ] `python3 -m http.server 3000` draait; gescreenshot op **1440, 768 én 390**.
- [ ] Geen horizontale scroll op 390px; geen element buiten zijn kaart/viewport.
- [ ] Hover + `:focus-visible` + `:active` op elke nieuwe klikbare.
- [ ] Enkel design-tokens gebruikt; geen `transition-all`; geen platte schaduw.
- [ ] `python3 pw_test.py` draait zonder nieuwe ⚠️'s (breid de pagina-lijst uit indien nodig).
- [ ] Minstens 2 vergelijkingsrondes screenshot ↔ bedoeling.
- [ ] Diff nagekeken (`git diff`) — geen debug-rommel, geen wijziging in `website/`.

---

## 10. Openstaande punten / bekende gaten in de site

- **SEO ontbreekt volledig:** geen `meta description`, geen Open Graph, geen `favicon`, geen `robots.txt`/`sitemap.xml`, geen JSON-LD. (Het MIELUS-project heeft dit wel — kan als voorbeeld dienen als Emiel dit wil.)
- **Locatie/adres** van het event nog niet publiek ("wordt na aankoop gecommuniceerd").
- **Socials:** enkel Instagram. Facebook wordt genoemd in oude docs maar staat niet op de site.
- **Regio's Handelaar 1 & 3** onbekend. **Handelaar 2 = Wijndomein Waes** — te verwerken (zie `voorstel-wijndomein-waes.md`).
- **`pw_test.py`** dekt de legal-pagina's + `steun-ons` niet.
- **`website/`-map** opruimen (na akkoord Emiel).
- **GitHub-token** in `.git/config` roteren.
- **Deploymethode** documenteren.

---

## 11. De huidige taak: Wijndomein Waes verwerken

Volledig uitgewerkt voorstel staat in **`voorstel-wijndomein-waes.md`**. Kern:

- Wijndomein Waes = **formule 2** (`sunset_*`-sleutels), €45, 18u30–21u00.
- Aanbevolen framing: Waes = de halte **"België · Vlaamse Landwijn"**; "wijnhandelaar" in de copy verbreden naar "wijnhuis" / FR "maison".
- Raakt: `translations.js` (sunset_* + concept-teksten "welke landen volgen nog"), `route.html` (partnerkaart + route-map label), `index.html` (mini-kaart + teaser), `formules.html` (auto via i18n + CTA-tekst), `event.html` (boarding pass "FORMULE"), `faq.html` (a1/a2/a9), evt. SEO-meta.
- **Wacht op Emiel:** concept-keuze (A+C?), exacte wijnselectie, of Waes op locatie of op domein schenkt, live-muziek/hapjes-bevestiging, beeldmateriaal, tekst-akkoord van Lodewijk Waes.
- Nieuwe beelden van Waes → `fotos/waes-*.jpg`, committen.
