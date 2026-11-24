#!/usr/bin/env python3
"""Build the translated game pages (index, how-to-play, levels) for every language folder.

The English pages in the repo root are written by hand and govern. Each language has its
strings in _build/i18n/<lang>.py (a dict T) and its support section in _build/support/<lang>.md.
Run from the repo root: python3 _build/pages.py. Jekyll skips folders that start with "_".
"""
import importlib.util
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://stanislau-malchanau.github.io/pet-match/"
STORE = "https://apps.apple.com/app/id6738354347"
LANGS = ["de", "fr", "es", "pt", "ru", "ja", "ko", "zh-hans", "zh-hant", "hi", "bn", "ar", "ur"]
RTL = {"ar", "ur"}
IMG = {
    "heart": "../img/level-heart.jpg",
    "chicks": "../img/match-three.jpg",
    "wave": "../img/level-wave.jpg",
    "shuffle": "../img/shuffle.jpg",
}


def load(lang):
    spec = importlib.util.spec_from_file_location(lang, os.path.join(ROOT, "_build", "i18n", lang.replace("-", "_") + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.T


def q(s):
    return json.dumps(s, ensure_ascii=False)


def front(title, desc, lang):
    return "---\ntitle: %s\ndescription: %s\nlang: %s\n---\n\n" % (q(title), q(desc), lang)


def wrap(lang, body):
    if lang in RTL:
        return '<div dir="rtl" markdown="1">\n\n' + body + "\n</div>\n"
    return body


def img(key, alt):
    return '<img src="%s" alt="%s" width="270" loading="lazy">' % (IMG[key], alt.replace('"', "&quot;"))


def nav(t, here):
    items = [("./", t["nav_game"]), ("how-to-play", t["nav_howto"]), ("levels", t["nav_levels"]),
             ("privacy", t["nav_privacy"]), ("terms", t["nav_terms"])]
    current = "./" if here == "index" else here
    links = ["[%s](%s)" % (label, href) for href, label in items if href != current]
    eng = {"index": "../", "how-to-play": "../how-to-play", "levels": "../levels"}[here]
    links.append("[English](%s)" % eng)
    return " · ".join(links)


def ld(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=2) + "\n</script>\n"


def index_page(lang, t, support):
    b = []
    b.append("# %s\n" % t["name"])
    b.append("**%s**\n" % t["idx_lead"])
    b.append("[%s](%s)\n" % (t["dl"], STORE))
    b.append("<p>%s\n%s</p>\n" % (img("heart", t["alt_heart"]), img("chicks", t["alt_chicks"])))
    b.append("## %s\n" % t["h_play"])
    b.append("\n".join("%d. %s" % (i + 1, s) for i, s in enumerate(t["play"])) + "\n")
    b.append(t["play_more"].format(howto="how-to-play") + "\n")
    b.append("## %s\n" % t["h_diff"])
    b.append("\n".join("- " + s.format(levels="levels") for s in t["diff"]) + "\n")
    b.append("## %s\n" % t["h_who"])
    b.append(t["who"] + "\n")
    b.append("## %s\n" % t["h_faq"])
    b.append("\n\n".join("**%s** %s" % (qq, a) for qq, a in t["faq"]) + "\n")
    b.append(support)
    b.append(nav(t, "index") + "\n")
    body = "\n".join(b)
    app = {
        "@context": "https://schema.org", "@type": "MobileApplication", "name": t["name"],
        "alternateName": "Pet Match", "description": t["idx_desc"], "inLanguage": lang,
        "url": BASE + lang + "/", "downloadUrl": STORE, "sameAs": [STORE],
        "image": BASE + "img/icon.png",
        "screenshot": [BASE + "img/level-heart.jpg", BASE + "img/match-three.jpg", BASE + "img/level-wave.jpg"],
        "operatingSystem": "iOS, iPadOS", "applicationCategory": "GameApplication",
        "applicationSubCategory": "Puzzle", "isAccessibleForFree": True,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        "author": {"@type": "Person", "name": "Stanislau Malchanau"},
    }
    faq = {
        "@context": "https://schema.org", "@type": "FAQPage", "inLanguage": lang,
        "mainEntity": [{"@type": "Question", "name": qq, "acceptedAnswer": {"@type": "Answer", "text": a}}
                       for qq, a in t["faq"]],
    }
    return front(t["name"], t["idx_desc"], lang) + wrap(lang, body) + "\n" + ld(app) + "\n" + ld(faq)


def howto_page(lang, t):
    b = []
    b.append("# %s\n" % t["ht_h1"])
    b.append("**%s**\n" % t["ht_lead"])
    b.append("[%s](%s)\n" % (t["dl"], STORE))
    b.append("## %s\n" % t["h_rules"])
    b.append("\n".join("%d. %s" % (i + 1, s) for i, s in enumerate(t["rules"])) + "\n")
    b.append("## %s\n" % t["h_boost"])
    b.append("\n".join("- **%s** %s" % (n, s) for n, s in t["boosters"]) + "\n")
    b.append("<p>%s</p>\n" % img("shuffle", t["alt_shuffle"]))
    b.append(t["recharge"] + "\n")
    b.append("## %s\n" % t["h_tips"])
    b.append("\n".join("- " + s for s in t["tips"]) + "\n")
    b.append("## %s\n" % t["h_ads"])
    b.append(t["ads"] + "\n")
    b.append(nav(t, "how-to-play") + "\n")
    howto = {
        "@context": "https://schema.org", "@type": "HowTo", "inLanguage": lang, "name": t["ht_title"],
        "description": t["ht_desc"],
        "step": [{"@type": "HowToStep", "text": s} for s in t["steps"]],
    }
    return front(t["ht_title"], t["ht_desc"], lang) + wrap(lang, "\n".join(b)) + "\n" + ld(howto)


def levels_page(lang, t):
    b = []
    b.append("# %s\n" % t["lv_h1"])
    b.append("**%s**\n" % t["lv_lead"])
    b.append("[%s](%s)\n" % (t["dl"], STORE))
    b.append("## %s\n" % t["h_look"])
    b.append("\n".join("- **%s** %s" % (label, items) for label, items in t["cats"]) + "\n")
    b.append("## %s\n" % t["h_hard"])
    b.append(t["hard"] + "\n")
    b.append("## %s\n" % t["h_animals"])
    b.append(t["animals"] + "\n")
    b.append("<p>%s\n%s</p>\n" % (img("heart", t["alt_heart"]), img("wave", t["alt_wave"])))
    b.append(nav(t, "levels") + "\n")
    return front(t["lv_title"], t["lv_desc"], lang) + wrap(lang, "\n".join(b))


def main():
    for lang in LANGS:
        t = load(lang)
        support = open(os.path.join(ROOT, "_build", "support", lang + ".md"), encoding="utf-8").read().strip() + "\n"
        for name, text in (("index.md", index_page(lang, t, support)),
                           ("how-to-play.md", howto_page(lang, t)),
                           ("levels.md", levels_page(lang, t))):
            with open(os.path.join(ROOT, lang, name), "w", encoding="utf-8") as f:
                f.write(text)
        print("built", lang)


if __name__ == "__main__":
    main()
