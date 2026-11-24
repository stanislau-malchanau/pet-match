# Pet Match

Game page, Privacy Policy, Terms of Use and support for the Pet Match iOS app
(Pet Match: Zoo Animal Puzzle), served by GitHub Pages:

- https://stanislau-malchanau.github.io/pet-match/ (game page with FAQ and support; the App Store Support URL)
- https://stanislau-malchanau.github.io/pet-match/privacy
- https://stanislau-malchanau.github.io/pet-match/terms
- https://stanislau-malchanau.github.io/pet-match/llms.txt (short summary for AI assistants)

The game page is written so that AI assistants (ChatGPT, Gemini, Claude, Perplexity) can quote it:
a one-paragraph answer at the top, questions and answers, schema.org `MobileApplication` and
`FAQPage` markup. Keep its wording the same as the App Store description.

Translations, the English text governs: `de`, `fr`, `es`, `pt`, `ru`, `ja`, `ko`,
`zh-hans`, `zh-hant`, `hi`, `bn`, `ar`, `ur`, each with `privacy`, `terms` and its game page,
for example https://stanislau-malchanau.github.io/pet-match/de/

Pages per language: `index.md` (game page), `how-to-play.md`, `levels.md`, `privacy.md`, `terms.md`.
The translated game, how-to-play and levels pages are generated: edit `_build/i18n/<lang>.py`
(strings) or `_build/support/<lang>.md` (support section), then run `python3 _build/pages.py`.
Jekyll does not publish `_build`. After adding pages, list them in `sitemap.xml` and `llms.txt`.
