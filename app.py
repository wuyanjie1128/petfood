import os
import random
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

import pandas as pd
import numpy as np
import streamlit as st
import altair as alt


# =========================================================
# Nebula Paw Kitchen™ — a premium cooked fresh planner
# English UI • No ingredient photos • Robust breed fallback
# =========================================================

APP_TITLE = "Nebula Paw Kitchen™"
APP_SUBTITLE = "A premium cooked-fresh meal intelligence studio for dogs"

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🐶🍳",
    layout="wide",
    initial_sidebar_state="expanded",
)


# -------------------------
# Creative cosmic-kitchen UI
# -------------------------
CUSTOM_CSS = """
<style>
.stApp {
    background:
        radial-gradient(1200px 800px at 8% 12%, rgba(120, 140, 255, 0.15), transparent 60%),
        radial-gradient(1200px 800px at 90% 15%, rgba(255, 120, 220, 0.12), transparent 60%),
        radial-gradient(900px 700px at 15% 90%, rgba(120, 255, 200, 0.10), transparent 60%),
        linear-gradient(135deg, #060712 0%, #0a0c1b 45%, #070812 100%);
    color: #F5F7FF;
}
h1, h2, h3, h4 { letter-spacing: 0.35px; }

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(255,255,255,0.035), rgba(255,255,255,0.01));
    border-right: 1px solid rgba(255,255,255,0.06);
}

.nebula-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.065), rgba(255,255,255,0.02));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 18px 18px 14px 18px;
    box-shadow: 0 10px 28px rgba(0,0,0,0.28);
}

.nebula-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.12), transparent);
    margin: 14px 0 18px 0;
}

.badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 999px;
    font-size: 11px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.10);
    margin-left: 6px;
}

.small-muted { opacity: 0.8; font-size: 0.92rem; }

.stButton > button {
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.10);
    background: linear-gradient(135deg, rgba(120,140,255,0.22), rgba(255,120,220,0.18));
    color: white;
    font-weight: 650;
}
.stButton > button:hover {
    border: 1px solid rgba(255,255,255,0.26);
    transform: translateY(-1px);
}

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] > div {
    background-color: rgba(255,255,255,0.04) !important;
    border-radius: 10px;
}

thead tr th { background-color: rgba(255,255,255,0.06) !important; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# =========================================================
# 1) Breed Atlas — built-in mega list + safe optional CSV
# =========================================================

def _builtin_breed_rows() -> List[Dict[str, str]]:
    # A large, globally diverse starter atlas.
    # Not literally every variety on earth, but intentionally broad.
    # You can later replace/extend via data/breeds.csv safely.

    def row(b, grp, reg, sz, notes=""):
        return {"Breed": b, "FCI Group": grp, "Region": reg, "Size Class": sz, "Notes": notes}

    G1 = "Group 1 - Sheepdogs and Cattle Dogs"
    G2 = "Group 2 - Pinscher / Schnauzer / Molossoid / Swiss Mountain"
    G3 = "Group 3 - Terriers"
    G4 = "Group 4 - Dachshunds"
    G5 = "Group 5 - Spitz and Primitive types"
    G6 = "Group 6 - Scent hounds and related"
    G7 = "Group 7 - Pointing Dogs"
    G8 = "Group 8 - Retrievers / Flushing Dogs / Water Dogs"
    G9 = "Group 9 - Companion and Toy Dogs"
    G10 = "Group 10 - Sighthounds"
    NA = "N/A"

    rows = [
        row("Mixed Breed / Unknown", NA, "Global", "Unknown", "For rescues or uncertain lineage"),

        # Group 1
        row("German Shepherd Dog", G1, "Europe", "Large"),
        row("Belgian Malinois", G1, "Europe", "Large"),
        row("Belgian Tervuren", G1, "Europe", "Large"),
        row("Belgian Groenendael", G1, "Europe", "Large"),
        row("Belgian Laekenois", G1, "Europe", "Large"),
        row("Border Collie", G1, "Europe", "Medium"),
        row("Rough Collie", G1, "Europe", "Large"),
        row("Smooth Collie", G1, "Europe", "Large"),
        row("Shetland Sheepdog", G1, "Europe", "Small"),
        row("Old English Sheepdog", G1, "Europe", "Large"),
        row("Australian Shepherd", G1, "Oceania", "Medium"),
        row("Miniature American Shepherd", G1, "North America", "Small"),
        row("Australian Cattle Dog", G1, "Oceania", "Medium"),
        row("Pembroke Welsh Corgi", G1, "Europe", "Small"),
        row("Cardigan Welsh Corgi", G1, "Europe", "Small"),
        row("Dutch Shepherd", G1, "Europe", "Large"),
        row("White Swiss Shepherd Dog", G1, "Europe", "Large"),
        row("Bearded Collie", G1, "Europe", "Medium"),
        row("Briard", G1, "Europe", "Large"),
        row("Puli", G1, "Europe", "Medium"),
        row("Pumi", G1, "Europe", "Medium"),
        row("Mudi", G1, "Europe", "Medium"),
        row("Bergamasco Sheepdog", G1, "Europe", "Large"),
        row("Pyrenean Shepherd", G1, "Europe", "Small"),

        # Group 2
        row("Doberman Pinscher", G2, "Europe", "Large"),
        row("Miniature Pinscher", G2, "Europe", "Small"),
        row("German Pinscher", G2, "Europe", "Medium"),
        row("Affenpinscher", G2, "Europe", "Toy"),
        row("Schnauzer - Giant", G2, "Europe", "Large"),
        row("Schnauzer - Standard", G2, "Europe", "Medium"),
        row("Schnauzer - Miniature", G2, "Europe", "Small"),
        row("Rottweiler", G2, "Europe", "Large"),
        row("Boxer", G2, "Europe", "Large"),
        row("Great Dane", G2, "Europe", "Giant"),
        row("Bullmastiff", G2, "Europe", "Giant"),
        row("Mastiff - English", G2, "Europe", "Giant"),
        row("Neapolitan Mastiff", G2, "Europe", "Giant"),
        row("Cane Corso", G2, "Europe", "Large"),
        row("Dogue de Bordeaux", G2, "Europe", "Giant"),
        row("Bernese Mountain Dog", G2, "Europe", "Giant"),
        row("Greater Swiss Mountain Dog", G2, "Europe", "Giant"),
        row("Saint Bernard", G2, "Europe", "Giant"),
        row("Newfoundland", G2, "Europe", "Giant"),
        row("Leonberger", G2, "Europe", "Giant"),
        row("Tibetan Mastiff", G2, "Asia", "Giant"),
        row("Boerboel", G2, "Africa", "Giant"),
        row("Akbash", G2, "Middle East", "Giant", "Livestock guardian type"),
        row("Kangal Shepherd Dog", G2, "Middle East", "Giant", "Livestock guardian type"),

        # Group 3
        row("Airedale Terrier", G3, "Europe", "Large"),
        row("Bull Terrier", G3, "Europe", "Medium"),
        row("Staffordshire Bull Terrier", G3, "Europe", "Medium"),
        row("American Staffordshire Terrier", G3, "North America", "Large"),
        row("West Highland White Terrier", G3, "Europe", "Small"),
        row("Cairn Terrier", G3, "Europe", "Small"),
        row("Scottish Terrier", G3, "Europe", "Small"),
        row("Norfolk Terrier", G3, "Europe", "Small"),
        row("Norwich Terrier", G3, "Europe", "Small"),
        row("Border Terrier", G3, "Europe", "Small"),
        row("Jack Russell Terrier", G3, "Europe", "Small"),
        row("Parson Russell Terrier", G3, "Europe", "Small"),
        row("Wire Fox Terrier", G3, "Europe", "Small"),
        row("Smooth Fox Terrier", G3, "Europe", "Small"),
        row("Kerry Blue Terrier", G3, "Europe", "Medium"),
        row("Irish Terrier", G3, "Europe", "Medium"),
        row("Soft Coated Wheaten Terrier", G3, "Europe", "Medium"),
        row("Australian Terrier", G3, "Oceania", "Small"),
        row("Yorkshire Terrier", G3, "Europe", "Toy"),

        # Group 4
        row("Dachshund - Standard", G4, "Europe", "Small"),
        row("Dachshund - Miniature", G4, "Europe", "Toy"),
        row("Dachshund - Wirehaired", G4, "Europe", "Small"),

        # Group 5
        row("Siberian Husky", G5, "Europe", "Large"),
        row("Alaskan Malamute", G5, "North America", "Giant"),
        row("Samoyed", G5, "Europe", "Large"),
        row("Akita", G5, "Asia", "Large"),
        row("American Akita", G5, "North America", "Large"),
        row("Shiba Inu", G5, "Asia", "Medium"),
        row("Korean Jindo", G5, "Asia", "Medium"),
        row("Chow Chow", G5, "Asia", "Large"),
        row("Keeshond", G5, "Europe", "Medium"),
        row("Pomeranian", G5, "Europe", "Toy"),
        row("Finnish Spitz", G5, "Europe", "Medium"),
        row("Norwegian Elkhound", G5, "Europe", "Medium"),
        row("Icelandic Sheepdog", G5, "Europe", "Medium"),
        row("Basenji", G5, "Africa", "Medium"),
        row("Thai Ridgeback", G5, "Asia", "Large"),
        row("Pharaoh Hound", G5, "Europe", "Large"),
        row("Xoloitzcuintli", G5, "North America", "Small/Medium", "Primitive heritage"),
        row("Peruvian Inca Orchid", G5, "South America", "Medium", "Primitive heritage"),
        row("Kishu Ken", G5, "Asia", "Medium"),
        row("Kai Ken", G5, "Asia", "Medium"),
        row("Shikoku", G5, "Asia", "Medium"),
        row("Hokkaido", G5, "Asia", "Medium"),
        row("Borzoi (Spitz line)", G5, "Europe", "Large", "Classification varies by registry"),

        # Group 6
        row("Beagle", G6, "Europe", "Medium"),
        row("Basset Hound", G6, "Europe", "Medium"),
        row("Bloodhound", G6, "Europe", "Large"),
        row("Rhodesian Ridgeback", G6, "Africa", "Large"),
        row("Coonhound - Black and Tan", G6, "North America", "Large"),
        row("Coonhound - Redbone", G6, "North America", "Large"),
        row("Coonhound - Treeing Walker", G6, "North America", "Large"),
        row("Harrier", G6, "Europe", "Medium"),
        row("Drever", G6, "Europe", "Medium"),
        row("Finnish Hound", G6, "Europe", "Medium"),

        # Group 7
        row("German Shorthaired Pointer", G7, "Europe", "Large"),
        row("German Wirehaired Pointer", G7, "Europe", "Large"),
        row("English Pointer", G7, "Europe", "Large"),
        row("Vizsla", G7, "Europe", "Medium"),
        row("Weimaraner", G7, "Europe", "Large"),
        row("Brittany", G7, "Europe", "Medium"),
        row("English Setter", G7, "Europe", "Large"),
        row("Gordon Setter", G7, "Europe", "Large"),
        row("Irish Setter", G7, "Europe", "Large"),

        # Group 8
        row("Labrador Retriever", G8, "Europe", "Large"),
        row("Golden Retriever", G8, "Europe", "Large"),
        row("Flat-Coated Retriever", G8, "Europe", "Large"),
        row("Curly-Coated Retriever", G8, "Europe", "Large"),
        row("Chesapeake Bay Retriever", G8, "North America", "Large"),
        row("Nova Scotia Duck Tolling Retriever", G8, "North America", "Medium"),
        row("English Springer Spaniel", G8, "Europe", "Medium"),
        row("English Cocker Spaniel", G8, "Europe", "Small"),
        row("American Cocker Spaniel", G8, "North America", "Small"),
        row("Portuguese Water Dog", G8, "Europe", "Large"),
        row("Spanish Water Dog", G8, "Europe", "Medium"),
        row("Lagotto Romagnolo", G8, "Europe", "Medium"),

        # Group 9
        row("Pug", G9, "Asia", "Small"),
        row("French Bulldog", G9, "Europe", "Small"),
        row("Bulldog - English", G9, "Europe", "Medium"),
        row("Boston Terrier", G9, "North America", "Small"),
        row("Cavalier King Charles Spaniel", G9, "Europe", "Small"),
        row("King Charles Spaniel", G9, "Europe", "Toy"),
        row("Maltese", G9, "Europe", "Toy"),
        row("Bichon Frise", G9, "Europe", "Small"),
        row("Havanese", G9, "North America", "Small"),
        row("Shih Tzu", G9, "Asia", "Toy"),
        row("Lhasa Apso", G9, "Asia", "Small"),
        row("Pekingese", G9, "Asia", "Toy"),
        row("Japanese Chin", G9, "Asia", "Toy"),
        row("Papillon", G9, "Europe", "Toy"),
        row("Chihuahua", G9, "North America", "Toy"),
        row("Chinese Crested", G9, "Asia", "Toy"),
        row("Coton de Tulear", G9, "Africa", "Small"),
        row("Brussels Griffon", G9, "Europe", "Toy"),
        row("Affenpinscher (Companion)", G9, "Europe", "Toy"),
        row("Poodle - Toy", G9, "Europe", "Toy"),
        row("Poodle - Miniature", G9, "Europe", "Small"),
        row("Poodle - Standard", G9, "Europe", "Large"),
        row("Italian Greyhound", G9, "Europe", "Toy"),
        row("Yorkshire Terrier (Companion line)", G9, "Europe", "Toy"),
        row("Russian Toy", G9, "Europe", "Toy"),
        row("Bolognese", G9, "Europe", "Small"),
        row("Lowchen", G9, "Europe", "Small"),

        # Group 10
        row("Greyhound", G10, "Europe", "Large"),
        row("Whippet", G10, "Europe", "Medium"),
        row("Saluki", G10, "Middle East", "Large"),
        row("Afghan Hound", G10, "Asia", "Large"),
        row("Irish Wolfhound", G10, "Europe", "Giant"),
        row("Scottish Deerhound", G10, "Europe", "Giant"),
        row("Italian Greyhound (Sighthound)", G10, "Europe", "Toy"),

        # Widely recognized non-FCI or registry-variant lines
        row("American Eskimo Dog", NA, "North America", "Small/Medium", "Spitz-type classification varies"),
        row("Great Pyrenees", NA, "Europe", "Giant", "Livestock guardian type"),
        row("Anatolian Shepherd Dog", NA, "Middle East", "Giant", "Livestock guardian type"),
        row("Caucasian Shepherd Dog", NA, "Europe/Asia", "Giant", "Also called Caucasian Ovcharka"),
        row("Central Asian Shepherd Dog", NA, "Europe/Asia", "Giant", "Also called Alabai"),
        row("Maremma Sheepdog", NA, "Europe", "Large", "Livestock guardian type"),
        row("Kuvasz", NA, "Europe", "Large", "Livestock guardian type"),
        row("Komondor", NA, "Europe", "Large", "Livestock guardian type"),
        row("Korean Sapsaree", NA, "Asia", "Large", "National heritage breed"),
        row("Tosa", NA, "Asia", "Large", "Japanese mastiff-type"),
        row("Catahoula Leopard Dog", NA, "North America", "Large", "Working heritage"),

        # Popular global breeds not yet listed above
        row("Rough-haired German Shepherd Mix", NA, "Global", "Large", "Common informal mix label"),
        row("Schnauzer Mix", NA, "Global", "Small/Medium", "Common companion mix"),
        row("Shiba Mix", NA, "Global", "Small/Medium", "Common companion mix"),

        # Designer / modern mixes (educational only)
        row("Cockapoo", NA, "Global", "Small", "Designer mix"),
        row("Labradoodle", NA, "Global", "Medium/Large", "Designer mix"),
        row("Goldendoodle", NA, "Global", "Medium/Large", "Designer mix"),
        row("Cavapoo", NA, "Global", "Small", "Designer mix"),
        row("Maltipoo", NA, "Global", "Toy", "Designer mix"),
        row("Shihpoo", NA, "Global", "Small", "Designer mix"),
        row("Pomsky", NA, "Global", "Small/Medium", "Designer mix"),
    ]

    # Expand with a broad plain-name list (no special metadata)
    # to simulate a larger atlas without risking CSV parsing issues.
    extra_names = [
        "Basset Fauve de Bretagne", "Black Russian Terrier", "Bohemian Shepherd",
        "Bolognese (Registry)", "Boykin Spaniel", "Bracco Italiano",
        "Briquet Griffon Vendeen", "Canaan Dog", "Catalan Sheepdog",
        "Chinese Shar-Pei", "Clumber Spaniel", "Dandie Dinmont Terrier",
        "English Toy Terrier", "Eurasier", "Field Spaniel",
        "Finnish Lapphund", "Glen of Imaal Terrier", "Ibizan Hound",
        "Irish Water Spaniel", "Japanese Spitz", "Keeshond (Registry)",
        "Kerry Beagle", "Koolie", "Laika (Regional types)",
        "Manchester Terrier", "Miniature Bull Terrier",
        "Norwegian Buhund", "Norwegian Lundehund",
        "Otterhound", "Pyrenean Mastiff", "Schipperke",
        "Sloughi", "Spanish Mastiff", "Swedish Vallhund",
        "Thai Bangkaew Dog", "Tibetan Spaniel", "Tibetan Terrier",
        "Treeing Tennessee Brindle", "Volpino Italiano",
        "Welsh Springer Spaniel", "Wirehaired Pointing Griffon",
        "Xiasi Dog (China)", "Yakutian Laika",
    ]
    for n in extra_names:
        rows.append(row(n, NA, "Global", "Unknown", "Broad atlas placeholder"))

    return rows


def build_builtin_breed_df() -> pd.DataFrame:
    df = pd.DataFrame(_builtin_breed_rows())
    # normalize
    for c in ["Breed", "FCI Group", "Region", "Size Class", "Notes"]:
        if c not in df.columns:
            df[c] = ""
        df[c] = df[c].astype(str).str.strip()
    df = df.drop_duplicates(subset=["Breed"]).sort_values("Breed").reset_index(drop=True)
    return df


@st.cache_data
def load_breeds() -> pd.DataFrame:
    """
    Safe loader:
    - Uses data/breeds.csv if present.
    - Any read/parse issue -> fallback to built-in atlas.
    This prevents pandas.errors.ParserError from breaking the app.
    """
    builtin = build_builtin_breed_df()
    path = os.path.join("data", "breeds.csv")

    if not os.path.exists(path):
        return builtin

    try:
        df = pd.read_csv(
            path,
            dtype=str,
            keep_default_na=False,
            engine="python",
        )
        # ensure columns
        required = ["Breed", "FCI Group", "Region", "Size Class", "Notes"]
        for col in required:
            if col not in df.columns:
                df[col] = ""
            df[col] = df[col].astype(str).str.strip()

        if not (df["Breed"] == "Mixed Breed / Unknown").any():
            df = pd.concat([pd.DataFrame([{
                "Breed": "Mixed Breed / Unknown",
                "FCI Group": "N/A",
                "Region": "Global",
                "Size Class": "Unknown",
                "Notes": ""
            }]), df], ignore_index=True)

        df = df.drop_duplicates(subset=["Breed"]).sort_values("Breed").reset_index(drop=True)
        # If someone accidentally provided an empty or weird file, fallback
        if df.empty or "Breed" not in df.columns:
            return builtin
        return df

    except Exception:
        return builtin


BREED_DF = load_breeds()
BREED_META = BREED_DF.set_index("Breed").to_dict(orient="index")


def filter_breed_options(search: str, fci_groups: List[str], regions: List[str], sizes: List[str]) -> List[str]:
    df = BREED_DF.copy()
    if fci_groups:
        df = df[df["FCI Group"].isin(fci_groups)]
    if regions:
        df = df[df["Region"].isin(regions)]
    if sizes:
        df = df[df["Size Class"].isin(sizes)]
    if search.strip():
        s = search.strip().lower()
        mask = (
            df["Breed"].str.lower().str.contains(s, na=False) |
            df["Notes"].astype(str).str.lower().str.contains(s, na=False)
        )
        df = df[mask]
    opts = df["Breed"].tolist()
    return opts if opts else ["Mixed Breed / Unknown"]


# =========================================================
# 2) Ingredient knowledge base (cooked-focus)
# =========================================================

@dataclass(frozen=True)
class Ingredient:
    name: str
    category: str  # Meat, Veg, Carb, Oil, Treat
    kcal_per_100g: float
    protein_g: float
    fat_g: float
    carbs_g: float
    micronote: str
    benefits: List[str]
    cautions: List[str]


def build_ingredients() -> Dict[str, Ingredient]:
    items = [
        # --- MEATS / PROTEINS ---
        Ingredient("Chicken (lean, cooked)", "Meat", 165, 31, 3.6, 0,
                   "B vitamins / selenium.",
                   ["High-quality protein", "Great base protein for rotation", "Widely available"],
                   ["Avoid if allergy suspected", "Remove skin for lower-fat plans"]),
        Ingredient("Turkey (lean, cooked)", "Meat", 150, 29, 2.0, 0,
                   "Niacin / selenium.",
                   ["Lean option for weight-aware plans", "Mild flavor", "Good GI-friendly anchor"],
                   ["Avoid processed turkey"]),
        Ingredient("Beef (lean, cooked)", "Meat", 200, 26, 10, 0,
                   "Iron / zinc / B12.",
                   ["Strong palatability", "Useful for active adults", "Supports red-blood-cell nutrition"],
                   ["Fat varies by cut"]),
        Ingredient("Lamb (lean, cooked)", "Meat", 206, 25, 12, 0,
                   "Zinc / carnitine.",
                   ["Alternative protein", "Rich taste to combat boredom", "Rotation diversity"],
                   ["Richer profile—use caution for fat-sensitive dogs"]),
        Ingredient("Pork (lean, cooked)", "Meat", 195, 27, 9, 0,
                   "Thiamine-rich protein.",
                   ["Good rotation variety", "Often highly palatable"],
                   ["Avoid processed pork"]),
        Ingredient("Duck (lean, cooked)", "Meat", 190, 24, 11, 0,
                   "Flavor-forward protein.",
                   ["Excellent for picky eaters", "Rotation variety"],
                   ["Moderate fat"]),
        Ingredient("Venison (lean, cooked)", "Meat", 158, 30, 3.2, 0,
                   "Often considered a novel protein.",
                   ["Lean alternative", "Rotation diversity"],
                   ["Novel protein strategies should be vet-guided"]),
        Ingredient("Rabbit (cooked)", "Meat", 173, 33, 3.5, 0,
                   "Very lean / light protein.",
                   ["Great for rotation", "Weight-aware option"],
                   ["Ensure safe sourcing"]),
        Ingredient("Egg (cooked)", "Meat", 155, 13, 11, 1.1,
                   "Complete amino-acid profile.",
                   ["High biological value", "Palatability booster"],
                   ["Introduce gradually"]),
        Ingredient("Salmon (cooked)", "Meat", 208, 20, 13, 0,
                   "Omega-3 / vitamin D.",
                   ["Skin and coat support", "Senior-friendly rotation"],
                   ["Higher fat—portion carefully"]),
        Ingredient("White Fish (cod, cooked)", "Meat", 105, 23, 0.9, 0,
                   "Very lean protein.",
                   ["Excellent for low-fat plans", "Gentle for sensitive stomachs"],
                   ["Keep unseasoned"]),
        Ingredient("Sardines (cooked, deboned)", "Meat", 208, 25, 11, 0,
                   "Omega-3 rich mini-fish.",
                   ["Great topper", "Highly palatable"],
                   ["Watch sodium if canned"]),

        # --- VEGETABLES ---
        Ingredient("Pumpkin (cooked)", "Veg", 26, 1, 0.1, 6.5,
                   "Soluble fiber / beta-carotene.",
                   ["Supports stool quality", "Gentle gut helper", "Excellent transition vegetable"],
                   ["Too much may dilute calories"]),
        Ingredient("Carrot (cooked)", "Veg", 35, 0.8, 0.2, 8,
                   "Beta-carotene.",
                   ["Colorful antioxidant support", "Low-cal micronutrient boost"],
                   ["Cook/soften for tiny breeds"]),
        Ingredient("Zucchini (cooked)", "Veg", 17, 1.2, 0.3, 3.1,
                   "Hydration-friendly veggie.",
                   ["Great for volumizing meals", "Mild flavor"],
                   ["Avoid seasoning"]),
        Ingredient("Green Beans (cooked)", "Veg", 31, 1.8, 0.1, 7,
                   "Low-cal bulk.",
                   ["Helpful for weight management", "Gentle fiber"],
                   []),
        Ingredient("Broccoli (cooked)", "Veg", 34, 2.8, 0.4, 7,
                   "Vitamin C / K.",
                   ["Rotation-friendly antioxidants"],
                   ["Large amounts can cause gas"]),
        Ingredient("Cauliflower (cooked)", "Veg", 25, 1.9, 0.3, 5,
                   "Low-cal crucifer.",
                   ["Adds volume and variety"],
                   ["May cause gas"]),
        Ingredient("Bell Pepper (red, cooked)", "Veg", 31, 1, 0.3, 6,
                   "Color-rich vitamin profile.",
                   ["Adds antioxidant diversity"],
                   ["Avoid spicy/seasoned"]),
        Ingredient("Spinach (cooked, small portions)", "Veg", 23, 2.9, 0.4, 3.6,
                   "Folate / magnesium.",
                   ["Micronutrient accent"],
                   ["Use small portions"]),
        Ingredient("Kale (cooked, small portions)", "Veg", 35, 2.9, 1.5, 4.4,
                   "Dense micronutrients.",
                   ["Small-dose antioxidant boost"],
                   ["Use small portions"]),
        Ingredient("Cabbage (cooked, small portions)", "Veg", 23, 1.3, 0.1, 5.5,
                   "Budget-friendly fiber.",
                   ["Adds variety"],
                   ["May cause gas"]),

        # --- CARBS ---
        Ingredient("Sweet Potato (cooked)", "Carb", 86, 1.6, 0.1, 20,
                   "Beta-carotene / potassium.",
                   ["Palatable controlled carb", "Great rotation energy base"],
                   ["Portion for weight control"]),
        Ingredient("Brown Rice (cooked)", "Carb", 123, 2.7, 1.0, 25.6,
                   "Gentle starch base.",
                   ["Neutral and easy-to-digest"],
                   ["Lower for weight-loss plans"]),
        Ingredient("White Rice (cooked)", "Carb", 130, 2.4, 0.3, 28.2,
                   "Very gentle GI carb.",
                   ["Useful during sensitive-stomach phases"],
                   ["Lower micronutrients vs brown rice"]),
        Ingredient("Oats (cooked)", "Carb", 71, 2.5, 1.4, 12,
                   "Soluble fiber.",
                   ["Satiety support", "Gut-friendly option"],
                   ["Introduce gradually"]),
        Ingredient("Quinoa (cooked)", "Carb", 120, 4.4, 1.9, 21.3,
                   "Higher-protein pseudo-grain.",
                   ["Adds amino-acid diversity"],
                   ["Rinse well before cooking"]),
        Ingredient("Barley (cooked)", "Carb", 123, 2.3, 0.4, 28,
                   "Fiber-friendly grain.",
                   ["Satiety-supporting carb"],
                   ["Introduce gradually"]),
        Ingredient("Potato (cooked, plain)", "Carb", 87, 2, 0.1, 20,
                   "Simple starch.",
                   ["Limited-ingredient carb option"],
                   ["Never raw / no green parts"]),

        # --- OILS ---
        Ingredient("Fish Oil (supplemental)", "Oil", 900, 0, 100, 0,
                   "EPA/DHA omega-3s.",
                   ["Skin/coat support", "Joint and inflammatory balance"],
                   ["Dose carefully"]),
        Ingredient("Olive Oil (small amounts)", "Oil", 884, 0, 100, 0,
                   "Monounsaturated fats.",
                   ["Palatability booster"],
                   ["Too much may cause GI upset"]),
        Ingredient("Flaxseed Oil (small amounts)", "Oil", 884, 0, 100, 0,
                   "ALA omega-3 (plant-based).",
                   ["Rotation fat option"],
                   ["ALA conversion is limited"]),

        # --- TREATS / FRUIT TOPPERS ---
        Ingredient("Blueberries (small portions)", "Treat", 57, 0.7, 0.3, 14.5,
                   "Antioxidant fruit topper.",
                   ["Light enrichment", "Palette diversity"],
                   ["Use small portions"]),
        Ingredient("Apple (peeled, no seeds)", "Treat", 52, 0.3, 0.2, 14,
                   "Hydrating sweet crunch.",
                   ["Low-cal treat topper"],
                   ["Remove seeds/core"]),
        Ingredient("Strawberries (small portions)", "Treat", 32, 0.7, 0.3, 7.7,
                   "Vitamin C and flavor variety.",
                   ["Light fruity enrichment"],
                   ["Use small portions"]),
    ]
    return {i.name: i for i in items}


INGREDIENTS = build_ingredients()


def ingredient_df() -> pd.DataFrame:
    rows = []
    for ing in INGREDIENTS.values():
        rows.append({
            "Ingredient": ing.name,
            "Category": ing.category,
            "kcal/100g": ing.kcal_per_100g,
            "Protein(g)": ing.protein_g,
            "Fat(g)": ing.fat_g,
            "Carbs(g)": ing.carbs_g,
            "Micro-note": ing.micronote,
            "Benefits": " • ".join(ing.benefits),
            "Cautions": " • ".join(ing.cautions) if ing.cautions else "",
        })
    return pd.DataFrame(rows).sort_values(["Category", "Ingredient"]).reset_index(drop=True)


def filter_ingredients_by_category(cat: str) -> List[str]:
    return [i.name for i in INGREDIENTS.values() if i.category == cat]


# =========================================================
# 3) Energy + life-stage logic (educational)
# =========================================================

def age_to_life_stage(age_years: float) -> str:
    if age_years < 1:
        return "Puppy"
    if age_years < 7:
        return "Adult"
    return "Senior"


def calc_rer(weight_kg: float) -> float:
    return 70 * (weight_kg ** 0.75)


def mer_factor(life_stage: str, activity: str, neutered: bool) -> float:
    base = 1.6 if neutered else 1.8
    if life_stage == "Puppy":
        base = 2.2 if neutered else 2.4
    elif life_stage == "Senior":
        base = 1.3 if neutered else 1.4

    activity_boost = {
        "Low": 0.9,
        "Normal": 1.0,
        "High": 1.2,
        "Athletic/Working": 1.35,
    }.get(activity, 1.0)

    return base * activity_boost


def compute_daily_energy(
    weight_kg: float,
    age_years: float,
    activity: str,
    neutered: bool,
    special_flags: List[str]
) -> Tuple[float, float, float, str]:
    stage = age_to_life_stage(age_years)
    rer = calc_rer(weight_kg)
    mer = rer * mer_factor(stage, activity, neutered)

    adj = 1.0
    rationale = []

    if "Overweight / Weight loss goal" in special_flags:
        adj *= 0.85
        rationale.append("Weight-loss adjusted target.")
    if "Pancreatitis risk / Needs lower fat" in special_flags:
        adj *= 0.95
        rationale.append("Fat-sensitive conservative target.")
    if "Kidney concern (vet-managed)" in special_flags:
        adj *= 0.95
        rationale.append("Energy conservative; protein strategy must be vet-guided.")
    if "Very picky eater" in special_flags:
        rationale.append("Rotation and palatability tactics emphasized.")

    mer_adj = mer * adj
    explanation = stage + (" | " + " ".join(rationale) if rationale else "")

    return rer, mer, mer_adj, explanation


# =========================================================
# 4) Ratio presets
# =========================================================

@dataclass(frozen=True)
class RatioPreset:
    key: str
    label: str
    meat_pct: int
    veg_pct: int
    carb_pct: int
    note: str


RATIO_PRESETS = [
    RatioPreset("balanced", "Balanced Cooked Fresh (default)", 50, 35, 15,
                "A practical cooked-fresh ratio emphasizing lean protein and diverse vegetables."),
    RatioPreset("weight", "Weight-Aware & Satiety", 45, 45, 10,
                "Higher vegetable volume and lower energy density."),
    RatioPreset("active", "Active Adult Energy", 55, 25, 20,
                "More energy support for high activity while keeping vegetables present."),
    RatioPreset("senior", "Senior Gentle Balance", 48, 40, 12,
                "Fiber and micronutrient focus, moderate carbs."),
    RatioPreset("puppy", "Puppy Growth (cooked baseline)", 55, 30, 15,
                "Growth needs are complex; long-term cooked plans require calcium/micronutrient balancing."),
    RatioPreset("gentle_gi", "Gentle GI Rotation", 50, 40, 10,
                "A calmer profile leaning on easy proteins and soothing fiber veggies."),
]


def ensure_ratio_sum(meat_pct: int, veg_pct: int, carb_pct: int) -> Tuple[int, int, int]:
    total = meat_pct + veg_pct + carb_pct
    if total == 100:
        return meat_pct, veg_pct, carb_pct
    meat = round(meat_pct / total * 100)
    veg = round(veg_pct / total * 100)
    carb = 100 - meat - veg
    carb = max(0, carb)
    if meat + veg + carb != 100:
        diff = 100 - (meat + veg + carb)
        meat = max(0, meat + diff)
    return meat, veg, carb


def estimate_food_grams_from_energy(daily_kcal: float, assumed_kcal_per_g: float) -> float:
    return daily_kcal / assumed_kcal_per_g


def grams_for_day(total_grams: float, meat_pct: int, veg_pct: int, carb_pct: int) -> Tuple[float, float, float]:
    return (
        total_grams * meat_pct / 100,
        total_grams * veg_pct / 100,
        total_grams * carb_pct / 100
    )


def day_nutrition_estimate(meat: str, veg: str, carb: str,
                           meat_g: float, veg_g: float, carb_g: float) -> Dict[str, float]:
    def calc(name: str, grams: float) -> Dict[str, float]:
        ing = INGREDIENTS[name]
        f = grams / 100.0
        return {
            "kcal": ing.kcal_per_100g * f,
            "protein": ing.protein_g * f,
            "fat": ing.fat_g * f,
            "carbs": ing.carbs_g * f,
        }
    a, b, c = calc(meat, meat_g), calc(veg, veg_g), calc(carb, carb_g)
    return {
        "kcal": a["kcal"] + b["kcal"] + c["kcal"],
        "protein": a["protein"] + b["protein"] + c["protein"],
        "fat": a["fat"] + b["fat"] + c["fat"],
        "carbs": a["carbs"] + b["carbs"] + c["carbs"],
    }


# =========================================================
# 5) Conservative supplement guide (expanded)
# =========================================================

SUPPLEMENTS = [
    {"name": "Omega-3 (Fish Oil)",
     "why": "Supports skin/coat, joint comfort, and inflammatory balance.",
     "best_for": ["Dry/itchy skin", "Senior dogs", "Joint-support plans"],
     "cautions": "Dose carefully; may loosen stool. Check with vet if on clotting-related meds.",
     "pairing": "Pairs well with lean proteins and colorful vegetables."},

    {"name": "Probiotics",
     "why": "May improve gut resilience and stool stability.",
     "best_for": ["Sensitive stomach", "Diet transitions", "Stress-related GI changes"],
     "cautions": "Choose canine-specific options.",
     "pairing": "Works nicely with pumpkin and gentle proteins."},

    {"name": "Prebiotic Fiber (e.g., inulin / MOS)",
     "why": "Supports beneficial gut bacteria.",
     "best_for": ["Soft stools", "Gut resilience goals"],
     "cautions": "Too much can cause gas.",
     "pairing": "Often paired with probiotics."},

    {"name": "Calcium Support (home-cooked essential)",
     "why": "Long-term home cooking commonly needs calcium balancing.",
     "best_for": ["Puppies", "Long-term cooked routines"],
     "cautions": "Over/under supplementation can be risky—vet nutritionist advised.",
     "pairing": "A backbone supplement for balanced home cooking."},

    {"name": "Canine Multivitamin",
     "why": "Helps cover micronutrient gaps in simplified routines.",
     "best_for": ["Limited ingredient variety", "Busy weekly batch cooking"],
     "cautions": "Avoid human multivitamins unless approved.",
     "pairing": "Best with rotation-based weeks."},

    {"name": "Joint Support (Glucosamine / Chondroitin / UC-II)",
     "why": "May support mobility and cartilage comfort.",
     "best_for": ["Large breeds", "Senior dogs", "Highly active dogs"],
     "cautions": "Effects vary and take time.",
     "pairing": "Combine with weight control and omega-3."},

    {"name": "Vitamin E (as guided)",
     "why": "Antioxidant support often used alongside omega-3.",
     "best_for": ["Dogs on long-term fish oil"],
     "cautions": "Avoid excessive dosing.",
     "pairing": "Consider with fatty-acid protocols."},

    {"name": "Dental Additives (vet-approved)",
     "why": "Supports plaque control when brushing is difficult.",
     "best_for": ["Small breeds", "Dental-prone dogs"],
     "cautions": "Not a substitute for brushing.",
     "pairing": "Pair with safe chewing strategies."},

    {"name": "L-Carnitine (vet-guided)",
     "why": "May assist some weight or cardiac strategies.",
     "best_for": ["Vet-supervised weight plans"],
     "cautions": "Use under professional advice.",
     "pairing": "Best with lean protein + veggie-forward ratios."},
]


# =========================================================
# 6) Personalized ingredient recommendations
# =========================================================

def recommend_ingredients(stage: str, special_flags: List[str]) -> Dict[str, List[str]]:
    meats, vegs, carbs, treats = [], [], [], []

    base_meats = [
        "Turkey (lean, cooked)", "White Fish (cod, cooked)",
        "Chicken (lean, cooked)", "Egg (cooked)", "Beef (lean, cooked)"
    ]
    base_vegs = [
        "Pumpkin (cooked)", "Zucchini (cooked)", "Green Beans (cooked)",
        "Carrot (cooked)", "Bell Pepper (red, cooked)"
    ]
    base_carbs = [
        "Sweet Potato (cooked)", "Brown Rice (cooked)", "Oats (cooked)", "Quinoa (cooked)"
    ]
    base_treats = [
        "Blueberries (small portions)", "Apple (peeled, no seeds)", "Strawberries (small portions)"
    ]

    meats.extend(base_meats)
    vegs.extend(base_vegs)
    carbs.extend(base_carbs)
    treats.extend(base_treats)

    if stage == "Puppy":
        meats.extend(["Chicken (lean, cooked)", "Beef (lean, cooked)"])
        carbs.extend(["White Rice (cooked)"])
    if stage == "Senior":
        meats.extend(["White Fish (cod, cooked)", "Salmon (cooked)"])
        vegs.extend(["Pumpkin (cooked)"])

    if "Sensitive stomach" in special_flags:
        meats.extend(["Turkey (lean, cooked)", "White Fish (cod, cooked)"])
        vegs.extend(["Pumpkin (cooked)"])
        carbs.extend(["White Rice (cooked)", "Oats (cooked)"])

    if "Skin/coat concern" in special_flags:
        meats.extend(["Salmon (cooked)", "Sardines (cooked, deboned)"])
        treats.extend(["Blueberries (small portions)"])

    if "Overweight / Weight loss goal" in special_flags:
        meats.extend(["Turkey (lean, cooked)", "White Fish (cod, cooked)", "Rabbit (cooked)"])
        vegs.extend(["Green Beans (cooked)", "Zucchini (cooked)", "Cauliflower (cooked)"])

    if "Pancreatitis risk / Needs lower fat" in special_flags:
        meats = [m for m in meats if m not in ["Salmon (cooked)", "Duck (lean, cooked)", "Sardines (cooked, deboned)"]]
        meats.extend(["Turkey (lean, cooked)", "White Fish (cod, cooked)"])

    def dedupe(lst):
        seen, out = set(), []
        for x in lst:
            if x in INGREDIENTS and x not in seen:
                out.append(x)
                seen.add(x)
        return out

    return {"Meat": dedupe(meats), "Veg": dedupe(vegs), "Carb": dedupe(carbs), "Treat": dedupe(treats)}


# =========================================================
# 7) Taste learning (single-dog session friendly)
# =========================================================

def pref_score_from_label(p: str) -> int:
    return {"Dislike": 0, "Neutral": 1, "Like": 2, "Love": 3}.get(p, 1)


def get_preference_maps() -> Tuple[Dict[str, float], Dict[str, float]]:
    entries = st.session_state.get("taste_log", [])
    if not entries:
        return {}, {}
    df = pd.DataFrame(entries)
    if df.empty:
        return {}, {}
    df["score"] = df["Preference"].map(pref_score_from_label)

    protein_map, veg_map = {}, {}
    sub = df.dropna(subset=["Protein"])
    if not sub.empty:
        protein_map = sub.groupby("Protein")["score"].mean().to_dict()
    sub = df.dropna(subset=["Veg"])
    if not sub.empty:
        veg_map = sub.groupby("Veg")["score"].mean().to_dict()
    return protein_map, veg_map


def weighted_choice(rng: random.Random, items: List[str], weights: List[float]) -> str:
    if not items:
        raise ValueError("weighted_choice received empty items")
    if len(items) != len(weights):
        raise ValueError("weighted_choice items/weights mismatch")
    total = sum(max(0.0, w) for w in weights)
    if total <= 0:
        return rng.choice(items)
    r = rng.random() * total
    acc = 0.0
    for item, w in zip(items, weights):
        w = max(0.0, w)
        acc += w
        if r <= acc:
            return item
    return items[-1]


def pick_rotation_smart(
    pantry_meats: List[str],
    pantry_vegs: List[str],
    pantry_carbs: List[str],
    allow_new: bool,
    recommendations: Dict[str, List[str]],
    taste_meat_map: Dict[str, float],
    taste_veg_map: Dict[str, float],
    use_taste_weights: bool,
    days: int = 7,
    seed: int = 42
) -> List[Dict[str, str]]:
    rng = random.Random(seed)

    all_meats = filter_ingredients_by_category("Meat")
    all_vegs = filter_ingredients_by_category("Veg")
    all_carbs = filter_ingredients_by_category("Carb")

    if allow_new:
        meat_pool = list(dict.fromkeys(pantry_meats + recommendations.get("Meat", []) + all_meats))
        veg_pool = list(dict.fromkeys(pantry_vegs + recommendations.get("Veg", []) + all_vegs))
        carb_pool = list(dict.fromkeys(pantry_carbs + recommendations.get("Carb", []) + all_carbs))
    else:
        meat_pool = pantry_meats if pantry_meats else all_meats
        veg_pool = pantry_vegs if pantry_vegs else all_vegs
        carb_pool = pantry_carbs if pantry_carbs else all_carbs

    def taste_weight(name: str, m: Dict[str, float]) -> float:
        if not use_taste_weights:
            return 1.0
        s = m.get(name)
        if s is None:
            return 1.0
        return max(0.25, 0.25 + float(s))  # 0..3 -> 0.25..3.25

    def choose(pool: List[str], last: Optional[str], last2: Optional[str], taste_map: Dict[str, float]) -> str:
        candidates = pool[:]
        # prevent boredom: avoid repeating the same ingredient too many days in a row
        if last and last2 and last == last2:
            filtered = [x for x in candidates if x != last]
            if filtered:
                candidates = filtered
        if last and len(candidates) > 1:
            filtered = [x for x in candidates if x != last]
            if filtered:
                candidates = filtered
        weights = [taste_weight(x, taste_map) for x in candidates]
        return weighted_choice(rng, candidates, weights)

    plan = []
    last_meat = last_meat2 = None
    last_veg = last_veg2 = None

    for _ in range(days):
        meat = choose(meat_pool, last_meat, last_meat2, taste_meat_map)
        veg = choose(veg_pool, last_veg, last_veg2, taste_veg_map)
        carb = rng.choice(carb_pool) if carb_pool else rng.choice(all_carbs)

        plan.append({"Meat": meat, "Veg": veg, "Carb": carb})

        last_meat2, last_meat = last_meat, meat
        last_veg2, last_veg = last_veg, veg

    return plan


def build_weekly_shopping_list(plan_df: pd.DataFrame) -> pd.DataFrame:
    totals = {}

    def add_item(name: str, grams: float):
        if not name or name == "—":
            return
        totals[name] = totals.get(name, 0.0) + float(grams)

    for _, row in plan_df.iterrows():
        add_item(row.get("Meat"), row.get("Daily Meat (g)", 0))
        add_item(row.get("Veg"), row.get("Daily Veg (g)", 0))
        add_item(row.get("Carb"), row.get("Daily Carb (g)", 0))

    rows = []
    for name, g in totals.items():
        cat = INGREDIENTS.get(name).category if name in INGREDIENTS else "Unknown"
        rows.append({
            "Ingredient": name,
            "Category": cat,
            "Total grams (7 days)": int(round(g)),
            "Avg grams/day": round(g / 7.0, 1),
        })

    df = pd.DataFrame(rows)
    if df.empty:
        return df
    return df.sort_values(["Category", "Ingredient"]).reset_index(drop=True)


def build_category_prep_summary(shopping_df: pd.DataFrame) -> pd.DataFrame:
    if shopping_df.empty:
        return shopping_df
    grp = shopping_df.groupby("Category")["Total grams (7 days)"].sum().reset_index()
    grp["Total grams (7 days)"] = grp["Total grams (7 days)"].round().astype(int)
    return grp.sort_values("Total grams (7 days)", ascending=False).reset_index(drop=True)


# =========================================================
# 8) Session state
# =========================================================

if "taste_log" not in st.session_state:
    st.session_state.taste_log = []


# =========================================================
# Sidebar — profile + breed filters + meals/day
# =========================================================

st.sidebar.markdown(f"## 🐶🍳 {APP_TITLE}")
st.sidebar.caption("Cosmic-grade cooked fresh planning")

dog_name = st.sidebar.text_input("Dog name", value="", placeholder="e.g., Mochi / Luna / Atlas")

st.sidebar.markdown("### Breed Atlas filters")
breed_search = st.sidebar.text_input("Search breed", value="")
fci_groups_all = sorted(BREED_DF["FCI Group"].unique().tolist())
regions_all = sorted(BREED_DF["Region"].unique().tolist())
sizes_all = sorted(BREED_DF["Size Class"].unique().tolist())

breed_fci = st.sidebar.multiselect("FCI Group", fci_groups_all, default=[])
breed_region = st.sidebar.multiselect("Region", regions_all, default=[])
breed_size = st.sidebar.multiselect("Size class", sizes_all, default=[])

breed_options = filter_breed_options(breed_search, breed_fci, breed_region, breed_size)

breed = st.sidebar.selectbox("Breed", breed_options, index=0)

colA, colB = st.sidebar.columns(2)
with colA:
    age_years = st.number_input("Age (years)", 0.1, 25.0, 3.0, 0.1)
with colB:
    weight_kg = st.number_input("Weight (kg)", 0.5, 90.0, 10.0, 0.1)

neutered = st.sidebar.toggle("Neutered/Spayed", value=True)
activity = st.sidebar.select_slider("Activity level", ["Low", "Normal", "High", "Athletic/Working"], value="Normal")

special_flags = st.sidebar.multiselect(
    "Special considerations",
    [
        "None",
        "Overweight / Weight loss goal",
        "Sensitive stomach",
        "Pancreatitis risk / Needs lower fat",
        "Skin/coat concern",
        "Very picky eater",
        "Kidney concern (vet-managed)",
        "Food allergy suspected",
        "Joint/mobility support focus",
    ],
    default=["None"]
)
if "None" in special_flags and len(special_flags) > 1:
    special_flags = [f for f in special_flags if f != "None"]

meals_per_day = st.sidebar.select_slider("Meals per day", [1, 2, 3, 4], value=2)

assumed_kcal_per_g = st.sidebar.slider(
    "Assumed energy density (kcal/g of cooked mix)",
    1.0, 1.8, 1.35, 0.05,
    help="A planning assumption. Actual calories vary by ingredients and cooking method."
)

st.sidebar.markdown("---")
st.sidebar.caption("Educational tool; not a substitute for veterinary nutrition advice.")


# =========================================================
# Hero banner
# =========================================================

title_name = dog_name.strip() or "Your dog"

st.markdown(
    f"""
    <div class="nebula-card">
      <h1>🐶🍲 {APP_TITLE}</h1>
      <p style="font-size: 1.05rem; opacity: 0.9;">
        {APP_SUBTITLE}
        <span class="badge">No-photo minimalist science</span>
        <span class="badge">Boredom-resistant rotation</span>
        <span class="badge">Pantry + smart add-ons</span>
      </p>
      <div class="nebula-divider"></div>
      <p style="opacity: 0.92;">
        Welcome, <b>{title_name}</b>. This studio blends an ingredient encyclopedia,
        ratio physics, preference learning, and a weekly menu generator designed to avoid
        “same meat every day” fatigue.
      </p>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# Tabs
# =========================================================

tab_home, tab_ingredients, tab_ratio, tab_planner, tab_supp, tab_taste = st.tabs(
    [
        "🐾 Command Deck",
        "🥩🥦 Ingredient Cosmos",
        "⚖️ Ratio Lab",
        "📅 7-Day Intelligent Plan",
        "💊 Supplement Observatory",
        "😋 Taste & Notes"
    ]
)


# =========================================================
# Home
# =========================================================

with tab_home:
    stage = age_to_life_stage(age_years)
    meta = BREED_META.get(breed, {})
    size_class = meta.get("Size Class", "Unknown")
    region = meta.get("Region", "Unknown")
    fci_group = meta.get("FCI Group", "Unknown")

    rer, mer, mer_adj, explanation = compute_daily_energy(
        weight_kg=weight_kg,
        age_years=age_years,
        activity=activity,
        neutered=neutered,
        special_flags=special_flags
    )

    st.markdown("### Profile Snapshot")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Name", title_name)
    c2.metric("Life stage", stage)
    c3.metric("RER (kcal/day)", f"{rer:.0f}")
    c4.metric("Target MER (adjusted)", f"{mer_adj:.0f}")

    st.caption(f"Breed: {breed} · Size class: {size_class} · Region: {region}")
    st.caption(f"FCI classification: {fci_group}")
    st.caption(f"Meals/day: {meals_per_day}")
    st.caption(f"Context note: {explanation}")

    with st.expander("Breed Atlas (current dataset)"):
        st.dataframe(BREED_DF, use_container_width=True, height=320)

    st.markdown("### Safety-first cooked fresh principles")
    with st.expander("Open safety notes"):
        st.write(
            """
            - This planner targets **cooked fresh inspiration**.
            - Avoid seasoning: salt, onion, garlic, spicy sauces.
            - Fully cook proteins and remove bones.
            - Long-term home-cooked feeding usually needs **calcium + micronutrient balancing**.
            - Puppies and medical cases should use a vet-supervised plan.
            """
        )

    st.markdown("### What makes this app 'premium'")
    colp1, colp2, colp3 = st.columns(3)
    with colp1:
        st.markdown(
            """
            <div class="nebula-card">
              <h4>Rotation Intelligence</h4>
              <p class="small-muted">
                The weekly engine purposely avoids repeating identical proteins/veggies
                too many days in a row to reduce boredom.
              </p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with colp2:
        st.markdown(
            """
            <div class="nebula-card">
              <h4>Pantry + Smart Add-ons</h4>
              <p class="small-muted">
                You can allow the system to recommend and use ingredients you do not currently have,
                producing more realistic, human-friendly meal variety.
              </p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with colp3:
        st.markdown(
            """
            <div class="nebula-card">
              <h4>Taste Learning</h4>
              <p class="small-muted">
                Your dog's preferences bias future suggestions without locking the plan
                into a monotone ingredient loop.
              </p>
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# Ingredient Cosmos (NO PHOTOS)
# =========================================================

with tab_ingredients:
    st.markdown("### Ingredient Encyclopedia (text-first, data-rich)")

    df = ingredient_df()

    col_f1, col_f2, col_f3 = st.columns([1.1, 1.1, 2.2])
    with col_f1:
        cat_filter = st.selectbox("Category filter", ["All", "Meat", "Veg", "Carb", "Oil", "Treat"])
    with col_f2:
        sort_key = st.selectbox("Sort by", ["Category", "Ingredient", "kcal/100g", "Protein(g)", "Fat(g)", "Carbs(g)"])
    with col_f3:
        search_text = st.text_input("Search ingredient name or notes", value="")

    df_view = df.copy()
    if cat_filter != "All":
        df_view = df_view[df_view["Category"] == cat_filter]

    if search_text.strip():
        mask = (
            df_view["Ingredient"].str.contains(search_text, case=False, na=False) |
            df_view["Micro-note"].str.contains(search_text, case=False, na=False) |
            df_view["Benefits"].str.contains(search_text, case=False, na=False) |
            df_view["Cautions"].str.contains(search_text, case=False, na=False)
        )
        df_view = df_view[mask]

    df_view = df_view.sort_values(sort_key).reset_index(drop=True)
    st.dataframe(df_view, use_container_width=True, height=360)

    st.markdown("### Deep-dive card (strictly no photos)")

    selected_ing = st.selectbox("Pick an ingredient to explore", df["Ingredient"].tolist())
    ing_obj = INGREDIENTS[selected_ing]

    st.markdown(
        f"""
        <div class="nebula-card">
          <h3>{ing_obj.name}</h3>
          <p><b>Category:</b> {ing_obj.category}</p>
          <p><b>Approx cooked nutrition per 100g:</b>
             {ing_obj.kcal_per_100g:.0f} kcal ·
             P {ing_obj.protein_g:.1f}g ·
             F {ing_obj.fat_g:.1f}g ·
             C {ing_obj.carbs_g:.1f}g
          </p>
          <p><b>Micro-note:</b> {ing_obj.micronote}</p>
          <div class="nebula-divider"></div>
          <p><b>Benefits</b></p>
          <ul>
            {''.join([f'<li>{b}</li>' for b in ing_obj.benefits])}
          </ul>
          <p><b>Cautions</b></p>
          <ul>
            {''.join([f'<li>{c}</li>' for c in ing_obj.cautions]) if ing_obj.cautions else '<li>No major general cautions listed for standard cooked use.</li>'}
          </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.expander("Ingredient science mini-lessons"):
        st.write(
            """
            **Protein rotation** can reduce boredom and may help some sensitive dogs
            identify triggers (under vet guidance).  
            **Vegetable diversity** is typically about fiber, micronutrients, and texture,
            not high calorie delivery.  
            **Carb choice** is often about digestibility, convenience, and controlled energy.
            """
        )


# =========================================================
# Ratio Lab
# =========================================================

with tab_ratio:
    st.markdown("### Ratio Presets & Custom Tuning")

    preset_labels = {p.label: p.key for p in RATIO_PRESETS}
    preset_choice_label = st.selectbox("Choose a ratio preset", list(preset_labels.keys()), index=0)
    preset_key = preset_labels[preset_choice_label]
    preset_obj = next(p for p in RATIO_PRESETS if p.key == preset_key)

    st.info(preset_obj.note)

    use_custom = st.toggle("Override with custom ratios", value=False)

    if not use_custom:
        meat_pct, veg_pct, carb_pct = preset_obj.meat_pct, preset_obj.veg_pct, preset_obj.carb_pct
    else:
        c1, c2, c3 = st.columns(3)
        with c1:
            meat_pct = st.slider("Meat %", 30, 70, preset_obj.meat_pct)
        with c2:
            veg_pct = st.slider("Veg %", 15, 55, preset_obj.veg_pct)
        with c3:
            carb_pct = st.slider("Carb %", 0, 30, preset_obj.carb_pct)
        meat_pct, veg_pct, carb_pct = ensure_ratio_sum(meat_pct, veg_pct, carb_pct)
        st.caption(f"Normalized ratio: Meat {meat_pct}% · Veg {veg_pct}% · Carb {carb_pct}%")

    rer, mer, mer_adj, explanation = compute_daily_energy(
        weight_kg=weight_kg, age_years=age_years,
        activity=activity, neutered=neutered,
        special_flags=special_flags
    )

    daily_grams = estimate_food_grams_from_energy(mer_adj, assumed_kcal_per_g)
    meat_g, veg_g, carb_g = grams_for_day(daily_grams, meat_pct, veg_pct, carb_pct)

    st.markdown("### Daily gram targets (assumption-based)")
    g1, g2, g3, g4 = st.columns(4)
    g1.metric("Total cooked mix (g/day)", f"{daily_grams:.0f}")
    g2.metric("Meat target (g)", f"{meat_g:.0f}")
    g3.metric("Veg target (g)", f"{veg_g:.0f}")
    g4.metric("Carb target (g)", f"{carb_g:.0f}")

    st.caption(f"Meals/day: {meals_per_day} → per-meal split approx {daily_grams/meals_per_day:.0f}g")

    # Conceptual macro lens (category averages)
    df_ing = ingredient_df()
    cat_means = df_ing.groupby("Category")[["kcal/100g"]].mean()

    def est_cat_kcal(cat: str, grams: float) -> float:
        if cat not in cat_means.index:
            return 0.0
        return float(cat_means.loc[cat, "kcal/100g"]) * grams / 100.0

    ratio_kcal_df = pd.DataFrame([
        {"Component": "Meat (avg)", "kcal": est_cat_kcal("Meat", meat_g)},
        {"Component": "Veg (avg)", "kcal": est_cat_kcal("Veg", veg_g)},
        {"Component": "Carb (avg)", "kcal": est_cat_kcal("Carb", carb_g)},
    ])

    chart = (
        alt.Chart(ratio_kcal_df)
        .mark_arc(innerRadius=55)
        .encode(
            theta="kcal:Q",
            color="Component:N",
            tooltip=["Component", alt.Tooltip("kcal:Q", format=".0f")]
        )
        .properties(height=280)
    )
    st.altair_chart(chart, use_container_width=True)


# =========================================================
# 7-Day Intelligent Plan
# =========================================================

with tab_planner:
    st.markdown("### Pantry-driven weekly generation (with boredom-resistant intelligence)")

    all_meats = filter_ingredients_by_category("Meat")
    all_vegs = filter_ingredients_by_category("Veg")
    all_carbs = filter_ingredients_by_category("Carb")

    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        pantry_meats = st.multiselect("Meats you have", all_meats, default=[])
    with col_p2:
        pantry_vegs = st.multiselect("Vegetables you have", all_vegs, default=[])
    with col_p3:
        pantry_carbs = st.multiselect("Carbs you have", all_carbs, default=[])

    st.markdown("### Planning style")

    col_mode1, col_mode2, col_mode3, col_mode4 = st.columns([1.0, 1.0, 1.2, 1.4])
    with col_mode1:
        pantry_only = st.toggle(
            "Pantry-only mode",
            value=False,
            help="If ON, the plan will not introduce new ingredients beyond your selections."
        )
    with col_mode2:
        taste_mode = st.toggle(
            "Taste-informed rotation",
            value=True,
            help="Biases choices toward what your dog likes."
        )
    with col_mode3:
        include_fruit = st.toggle(
            "Allow fruit toppers (small)",
            value=True,
            help="Adds optional small fruit suggestions for variety."
        )
    with col_mode4:
        allow_new = st.toggle(
            "Human-friendly variety mode",
            value=True,
            help="If ON, the engine may recommend and use ingredients you don't currently have."
        )

    stage = age_to_life_stage(age_years)
    recs = recommend_ingredients(stage, special_flags)

    st.markdown("### Personalized add-on suggestions (what could make this week better)")
    rr1, rr2, rr3, rr4 = st.columns(4)
    with rr1:
        st.write("**Proteins**")
        st.write("\n".join([f"• {x}" for x in recs["Meat"][:10]]) if recs["Meat"] else "—")
    with rr2:
        st.write("**Vegetables**")
        st.write("\n".join([f"• {x}" for x in recs["Veg"][:10]]) if recs["Veg"] else "—")
    with rr3:
        st.write("**Carbs**")
        st.write("\n".join([f"• {x}" for x in recs["Carb"][:10]]) if recs["Carb"] else "—")
    with rr4:
        st.write("**Fruits (optional)**")
        if include_fruit and recs["Treat"]:
            st.write("\n".join([f"• {x}" for x in recs["Treat"][:8]]))
        else:
            st.write("—")

    st.markdown("### Ratio configuration for weekly planner")
    preset_labels = {p.label: p.key for p in RATIO_PRESETS}
    planner_preset_label = st.selectbox("Planner ratio preset", list(preset_labels.keys()), index=0)
    planner_preset_obj = next(p for p in RATIO_PRESETS if p.key == preset_labels[planner_preset_label])

    planner_custom = st.toggle("Fine-tune planner ratio", value=False)
    if not planner_custom:
        meat_pct, veg_pct, carb_pct = planner_preset_obj.meat_pct, planner_preset_obj.veg_pct, planner_preset_obj.carb_pct
    else:
        cc1, cc2, cc3 = st.columns(3)
        with cc1:
            meat_pct = st.slider("Planner Meat %", 30, 70, planner_preset_obj.meat_pct, key="planner_meat")
        with cc2:
            veg_pct = st.slider("Planner Veg %", 15, 55, planner_preset_obj.veg_pct, key="planner_veg")
        with cc3:
            carb_pct = st.slider("Planner Carb %", 0, 30, planner_preset_obj.carb_pct, key="planner_carb")
        meat_pct, veg_pct, carb_pct = ensure_ratio_sum(meat_pct, veg_pct, carb_pct)

    rer, mer, mer_adj, explanation = compute_daily_energy(
        weight_kg=weight_kg, age_years=age_years,
        activity=activity, neutered=neutered,
        special_flags=special_flags
    )

    daily_grams = estimate_food_grams_from_energy(mer_adj, assumed_kcal_per_g)
    meat_g, veg_g, carb_g = grams_for_day(daily_grams, meat_pct, veg_pct, carb_pct)

    st.caption(
        f"Daily targets (assumption-based): "
        f"{daily_grams:.0f}g total → Meat {meat_g:.0f}g · Veg {veg_g:.0f}g · Carb {carb_g:.0f}g"
    )
    st.caption(f"Meals/day: {meals_per_day} → per-meal split will be shown in the plan.")

    seed = st.slider("Rotation randomness seed", 1, 999, 42)
    generate = st.button("✨ Generate 7-Day Nebula Plan")

    taste_meat_map, taste_veg_map = get_preference_maps()

    if generate:
        effective_allow_new = (allow_new and not pantry_only)

        rotation = pick_rotation_smart(
            pantry_meats=pantry_meats,
            pantry_vegs=pantry_vegs,
            pantry_carbs=pantry_carbs,
            allow_new=effective_allow_new,
            recommendations=recs,
            taste_meat_map=taste_meat_map,
            taste_veg_map=taste_veg_map,
            use_taste_weights=taste_mode,
            days=7,
            seed=seed
        )

        fruit_rotation = []
        if include_fruit and recs["Treat"]:
            rng = random.Random(seed + 7)
            for _ in range(7):
                fruit_rotation.append(rng.choice(recs["Treat"]))
        else:
            fruit_rotation = [None] * 7

        per_meal_total = daily_grams / meals_per_day
        per_meal_meat = meat_g / meals_per_day
        per_meal_veg = veg_g / meals_per_day
        per_meal_carb = carb_g / meals_per_day

        rows = []
        for i, combo in enumerate(rotation, start=1):
            mg, vg, cg = grams_for_day(daily_grams, meat_pct, veg_pct, carb_pct)

            # protect against missing dict keys (shouldn't happen)
            meat_name = combo.get("Meat", all_meats[0])
            veg_name = combo.get("Veg", all_vegs[0])
            carb_name = combo.get("Carb", all_carbs[0])

            nut = day_nutrition_estimate(meat_name, veg_name, carb_name, mg, vg, cg)

            rows.append({
                "Day": f"Day {i}",
                "Meat": meat_name,
                "Veg": veg_name,
                "Carb": carb_name,
                "Optional Fruit Topper": fruit_rotation[i-1] or "—",
                "Daily Meat (g)": round(mg),
                "Daily Veg (g)": round(vg),
                "Daily Carb (g)": round(cg),
                "Meals/day": meals_per_day,
                "Per-Meal Total (g)": round(per_meal_total),
                "Per-Meal Meat (g)": round(per_meal_meat),
                "Per-Meal Veg (g)": round(per_meal_veg),
                "Per-Meal Carb (g)": round(per_meal_carb),
                "Est kcal": round(nut["kcal"]),
                "Protein (g)": round(nut["protein"], 1),
                "Fat (g)": round(nut["fat"], 1),
                "Carbs (g)": round(nut["carbs"], 1),
                "Variety Mode": "Pantry-only" if pantry_only else ("Smart + add-ons" if effective_allow_new else "Pantry-preferred"),
            })

        plan_df = pd.DataFrame(rows)

        st.markdown(f"### {title_name}'s weekly plan")
        st.dataframe(plan_df, use_container_width=True, height=360)

        st.markdown("### Weekly nutrient trend (approx)")
        melt = plan_df.melt(
            id_vars=["Day"],
            value_vars=["Est kcal", "Protein (g)", "Fat (g)", "Carbs (g)"],
            var_name="Metric",
            value_name="Value"
        )
        line = (
            alt.Chart(melt)
            .mark_line(point=True)
            .encode(
                x="Day:N",
                y="Value:Q",
                color="Metric:N",
                tooltip=["Day", "Metric", "Value"]
            )
            .properties(height=260)
        )
        st.altair_chart(line, use_container_width=True)

        st.markdown("### 🧾 Weekly shopping list & batch-prep calculator")
        shopping_df = build_weekly_shopping_list(plan_df)
        if shopping_df.empty:
            st.info("Shopping list is empty. Try regenerating.")
        else:
            cat_summary = build_category_prep_summary(shopping_df)

            csum1, csum2 = st.columns([1, 2])
            with csum1:
                st.markdown("**Category totals**")
                st.dataframe(cat_summary, use_container_width=True, height=220)
            with csum2:
                st.markdown("**Ingredient totals (7 days)**")
                st.dataframe(shopping_df, use_container_width=True, height=220)

            csv_bytes = shopping_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️ Download shopping list (CSV)",
                data=csv_bytes,
                file_name=f"{title_name.lower().replace(' ', '_')}_shopping_list.csv",
                mime="text/csv"
            )

        with st.expander("Why this planner does NOT force identical daily ingredients"):
            st.write(
                """
                Dogs can get bored when the same protein/vegetable repeats every day.
                The rotation engine applies simple anti-repetition rules and will introduce
                diversity—especially when you enable **Human-friendly variety mode**.
                """
            )


# =========================================================
# Supplement Observatory
# =========================================================

with tab_supp:
    st.markdown("### Conservative supplement pairing guide")

    st.write(
        """
        This is a non-prescriptive educational guide.
        For dosing and long-term protocols—especially for puppies and medical conditions—
        consult a veterinarian or a board-certified veterinary nutritionist.
        """
    )

    supp_df = pd.DataFrame(SUPPLEMENTS)
    st.dataframe(
        supp_df[["name", "why", "cautions", "pairing"]],
        use_container_width=True,
        height=300
    )

    st.markdown("### Personalized supplement lens")
    focus = st.multiselect(
        "Select your priority",
        ["Skin/Coat", "Gut", "Joint/Mobility", "Puppy Growth Support",
         "Senior Vitality", "Weight Management", "Dental Support"],
        default=[]
    )

    def add_if(lst, item):
        if item not in lst:
            lst.append(item)

    suggestions = []
    if "Skin/Coat" in focus:
        add_if(suggestions, "Omega-3 (Fish Oil)")
        add_if(suggestions, "Vitamin E (as guided)")
    if "Gut" in focus:
        add_if(suggestions, "Probiotics")
        add_if(suggestions, "Prebiotic Fiber (e.g., inulin / MOS)")
    if "Joint/Mobility" in focus:
        add_if(suggestions, "Joint Support (Glucosamine / Chondroitin / UC-II)")
        add_if(suggestions, "Omega-3 (Fish Oil)")
    if "Puppy Growth Support" in focus:
        add_if(suggestions, "Calcium Support (home-cooked essential)")
        add_if(suggestions, "Canine Multivitamin")
    if "Senior Vitality" in focus:
        add_if(suggestions, "Omega-3 (Fish Oil)")
        add_if(suggestions, "Joint Support (Glucosamine / Chondroitin / UC-II)")
        add_if(suggestions, "Probiotics")
    if "Weight Management" in focus:
        add_if(suggestions, "Probiotics")
        add_if(suggestions, "L-Carnitine (vet-guided)")
    if "Dental Support" in focus:
        add_if(suggestions, "Dental Additives (vet-approved)")

    if suggestions:
        st.markdown(
            f"""
            <div class="nebula-card">
              <h4>Educational focus list</h4>
              <ul>
                {''.join([f'<li>{s}</li>' for s in suggestions])}
              </ul>
              <div class="nebula-divider"></div>
              <p class="small-muted">
                Consider these as discussion points with your vet,
                not automatic prescriptions.
              </p>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.caption("Select a priority to view conservative suggestions.")


# =========================================================
# Taste & Notes
# =========================================================

with tab_taste:
    st.markdown(f"### Taste tracking capsule for {title_name}")

    st.write(
        """
        Log how your dog reacts to different proteins and vegetables.
        The weekly planner can use these preferences to gently bias future rotations.
        """
    )

    col_t1, col_t2, col_t3 = st.columns(3)
    with col_t1:
        log_meat = st.selectbox("Observed protein", ["(skip)"] + filter_ingredients_by_category("Meat"))
    with col_t2:
        log_veg = st.selectbox("Observed vegetable", ["(skip)"] + filter_ingredients_by_category("Veg"))
    with col_t3:
        love_level = st.select_slider(
            "Preference",
            options=["Dislike", "Neutral", "Like", "Love"],
            value="Like"
        )

    stool = st.selectbox("Stool observation (optional)", ["(skip)", "Normal", "Soft", "Loose", "Constipated"])
    energy = st.selectbox("Energy level (optional)", ["(skip)", "Normal", "High", "Low"])
    itch = st.selectbox("Itching/skin (optional)", ["(skip)", "No change", "Improved", "Worse"])

    notes = st.text_input("Extra notes (optional)")

    if st.button("🧪 Add taste entry"):
        entry = {
            "Dog Name": title_name,
            "Breed": breed,
            "Age (y)": round(age_years, 2),
            "Weight (kg)": round(weight_kg, 2),
            "Protein": None if log_meat == "(skip)" else log_meat,
            "Veg": None if log_veg == "(skip)" else log_veg,
            "Preference": love_level,
            "Stool": None if stool == "(skip)" else stool,
            "Energy": None if energy == "(skip)" else energy,
            "Skin": None if itch == "(skip)" else itch,
            "Notes": notes.strip(),
        }
        st.session_state.taste_log.append(entry)
        st.success("Entry added to this session log.")

    if st.session_state.taste_log:
        log_df = pd.DataFrame(st.session_state.taste_log)

        st.markdown("### Session taste log")
        st.dataframe(log_df, use_container_width=True, height=260)

        st.markdown("### Preference summaries (session)")

        def pref_score(p: str) -> int:
            return {"Dislike": 0, "Neutral": 1, "Like": 2, "Love": 3}.get(p, 1)

        protein_records = log_df.dropna(subset=["Protein"]).copy()
        veg_records = log_df.dropna(subset=["Veg"]).copy()

        col_s1, col_s2 = st.columns(2)
        with col_s1:
            if not protein_records.empty:
                protein_records["Score"] = protein_records["Preference"].map(pref_score)
                rank = protein_records.groupby("Protein")["Score"].mean().sort_values(ascending=False).reset_index()
                rank.columns = ["Protein", "Avg Preference Score"]
                bar = (
                    alt.Chart(rank)
                    .mark_bar()
                    .encode(
                        x=alt.X("Avg Preference Score:Q", scale=alt.Scale(domain=[0, 3])),
                        y=alt.Y("Protein:N", sort="-x"),
                        tooltip=["Protein", alt.Tooltip("Avg Preference Score:Q", format=".2f")]
                    )
                    .properties(height=240, title="Protein preference (session)")
                )
                st.altair_chart(bar, use_container_width=True)
            else:
                st.caption("No protein taste entries yet.")

        with col_s2:
            if not veg_records.empty:
                veg_records["Score"] = veg_records["Preference"].map(pref_score)
                rank = veg_records.groupby("Veg")["Score"].mean().sort_values(ascending=False).reset_index()
                rank.columns = ["Vegetable", "Avg Preference Score"]
                bar = (
                    alt.Chart(rank)
                    .mark_bar()
                    .encode(
                        x=alt.X("Avg Preference Score:Q", scale=alt.Scale(domain=[0, 3])),
                        y=alt.Y("Vegetable:N", sort="-x"),
                        tooltip=["Vegetable", alt.Tooltip("Avg Preference Score:Q", format=".2f")]
                    )
                    .properties(height=240, title="Vegetable preference (session)")
                )
                st.altair_chart(bar, use_container_width=True)
            else:
                st.caption("No vegetable taste entries yet.")
    else:
        st.info("No taste entries yet. Add a few to activate taste-informed rotation.")


# =========================================================
# Footer
# =========================================================

st.markdown("---")
st.caption(
    f"{APP_TITLE} is an educational cooked-fresh planner. "
    "For long-term complete nutrition—especially for puppies or medical cases—"
    "consult a veterinarian or a board-certified veterinary nutritionist."
)
