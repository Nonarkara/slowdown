#!/usr/bin/env python3
"""
Download all 27 public-domain art plates used in the book to ./img/.

Run this once before deploying the site for fully self-hosted images.
The book also works without it — the page falls back to the Wikimedia
CDN — but local files give the most reliable, fastest first paint.

Usage:
    python3 download.py

Safe to re-run; existing files are skipped.
Requires Python 3.6+ (standard library only).
"""
import os
import sys
import urllib.parse
import urllib.request
import urllib.error

FILES = [
    "Six_persimmons.jpg",
    "The_Sixth_Patriarch_Cutting_Bamboo_by_Liang_Kai.jpg",
    "Sesshu_-_Haboku-Sansui.jpg",
    "Red_Fuji_southern_wind_clear_morning.jpg",
    "Vilhelm_Hammershøi_-_Interior_in_Strandgade,_Sunlight_on_the_Floor_-_Google_Art_Project.jpg",
    "Vermeer_-_Woman_holding_a_balance_(National_Gallery_of_Art).jpg",
    "Jean-Baptiste-Camille_Corot_-_Ville-d'Avray_-_Google_Art_Project.jpg",
    "Caspar_David_Friedrich_-_Wanderer_above_the_Sea_of_Fog.jpeg",
    "Caspar_David_Friedrich_-_Der_Mönch_am_Meer_-_Google_Art_Project.jpg",
    "Joseph_Mallord_William_Turner_-_Rain,_Steam_and_Speed_-_The_Great_Western_Railway_-_WGA23178.jpg",
    "Whistler-Nocturne_in_black_and_gold.jpg",
    "Rembrandt_van_Rijn_-_Self-Portrait_-_Google_Art_Project.jpg",
    "Gustave_Caillebotte_-_The_Floor_Planers_-_Google_Art_Project.jpg",
    "Pieter_Bruegel_de_Oude_-_De_val_van_Icarus.jpg",
    "Hokusai-Mt_Fuji-36-Views-Rainstorm.jpg",
    "Albrecht_Dürer_-_Melencolia_I_(detail)_-_WGA7195.jpg",
    "Hiroshige_Atake_sous_une_averse_soudaine.jpg",
    "Hiroshige_-_Plum_Park_in_Kameido.jpg",
    "Claude_Monet_-_The_Houses_of_Parliament,_Sunset.jpg",
    "Tawaraya_Sotatsu_-_Waves_at_Matsushima_-_Google_Art_Project.jpg",
    "Itoh_Jakuchu_-_Rooster_(Ōkyo_Maruyama).jpg",
    "Albrecht_Dürer_-_Hare,_1502_-_Google_Art_Project.jpg",
    "Paul_Cézanne_-_Mont_Sainte-Victoire_-_Google_Art_Project.jpg",
    "Ogata_Kōrin_-_Red_and_White_Plum_Blossoms_-_Google_Art_Project.jpg",
    "Bada_Shanren_-_Fish.jpg",
    "Two_Cranes_on_a_snow-covered_pine_tree_LACMA_M.71.100.49.jpg",
    "Pine_Trees_(Shōrin-zu_byōbu)_-_left_hand_screen.jpg",
]

WIDTH = 1800  # request a reasonable max width from Wikimedia's thumb service
HERE = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(HERE, "img")


def fetch(filename: str) -> bool:
    out = os.path.join(IMG_DIR, filename)
    if os.path.exists(out) and os.path.getsize(out) > 0:
        print(f"  skip   {filename}")
        return True
    encoded = urllib.parse.quote(filename, safe="")
    url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{encoded}?width={WIDTH}"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "slowdown-book/1.0 (public-domain art download script)"
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
        with open(out, "wb") as f:
            f.write(data)
        print(f"  ok     {filename}  ({len(data)//1024} KB)")
        return True
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
        print(f"  FAIL   {filename}  ({e})")
        return False


def main() -> int:
    os.makedirs(IMG_DIR, exist_ok=True)
    print(f"Downloading {len(FILES)} plates to {IMG_DIR}\n")
    failed = [f for f in FILES if not fetch(f)]
    print()
    if failed:
        print(f"Done with {len(failed)} failure(s):")
        for f in failed:
            print(f"  - {f}")
        return 1
    print("All plates downloaded.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
