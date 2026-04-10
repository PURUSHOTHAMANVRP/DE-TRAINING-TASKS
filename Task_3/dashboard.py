"""
Stage 2 — Books Data Dashboard
Reads books_transformed.csv and saves a 4-panel dashboard.png
"""

import os
import logging
from pathlib import Path
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

matplotlib.use("Agg")   # headless — no window needed

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)

INPUT_CSV   = Path("new_data/transformed/books/books_transformed.csv")
OUTPUT_FILE = Path("dashboard.png")

PALETTE = {
    "blue": "#2563EB", "purple": "#7C3AED", "green": "#059669",
    "amber": "#D97706", "red": "#DC2626", "gray": "#6B7280",
    "bg": "#F9FAFB", "panel": "#FFFFFF", "text": "#111827",
    "subtext": "#6B7280",
}
STAR_COLORS = {1: "#EF4444", 2: "#F97316", 3: "#EAB308",
               4: "#22C55E", 5: "#3B82F6"}


def style(ax, title):
    ax.set_facecolor(PALETTE["panel"])
    ax.set_title(title, fontsize=13, fontweight="bold",
                 color=PALETTE["text"], pad=12)
    ax.tick_params(colors=PALETTE["subtext"], labelsize=9)
    for spine in ax.spines.values():
        spine.set_edgecolor("#E5E7EB")
        spine.set_linewidth(0.8)
    ax.yaxis.grid(True, linestyle="--", linewidth=0.5, alpha=0.6, color="#D1D5DB")
    ax.set_axisbelow(True)


def panel_price(ax, df):
    prices = df["price"].dropna()
    ax.hist(prices, bins=30, color=PALETTE["blue"], alpha=0.75,
            edgecolor="white", linewidth=0.5)
    try:
        from scipy.stats import gaussian_kde
        xs = np.linspace(prices.min(), prices.max(), 300)
        kde = gaussian_kde(prices)
        ax2 = ax.twinx()
        ax2.plot(xs, kde(xs), color=PALETTE["purple"], linewidth=2)
        ax2.set_ylabel("Density", fontsize=9, color=PALETTE["subtext"])
        ax2.tick_params(colors=PALETTE["subtext"], labelsize=8)
        for spine in ax2.spines.values():
            spine.set_edgecolor("#E5E7EB")
    except ImportError:
        pass
    ax.axvline(prices.median(), color=PALETTE["amber"], linestyle="--",
               linewidth=1.5, label=f"Median £{prices.median():.2f}")
    ax.legend(fontsize=8)
    ax.set_xlabel("Price (£)", fontsize=9, color=PALETTE["subtext"])
    ax.set_ylabel("Number of books", fontsize=9, color=PALETTE["subtext"])
    style(ax, "Price distribution")


def panel_ratings(ax, df):
    ratings = df["rating"].dropna().astype(int)
    counts  = ratings.value_counts().sort_index()
    colors  = [STAR_COLORS.get(s, PALETTE["gray"]) for s in counts.index]
    bars    = ax.bar(counts.index, counts.values, color=colors,
                     edgecolor="white", linewidth=0.5, width=0.6)
    for bar, val in zip(bars, counts.values):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + counts.values.max() * 0.01,
                str(val), ha="center", va="bottom", fontsize=9,
                fontweight="bold", color=PALETTE["text"])
    ax.set_xlabel("Star rating", fontsize=9, color=PALETTE["subtext"])
    ax.set_ylabel("Number of books", fontsize=9, color=PALETTE["subtext"])
    ax.set_xticks(range(1, 6))
    ax.set_xticklabels(["1 ★", "2 ★", "3 ★", "4 ★", "5 ★"], fontsize=9)
    style(ax, "Rating distribution")


def panel_availability(ax, df):
    avail = df["availability"].dropna()
    in_s  = int((avail == 1).sum())
    out_s = int((avail == 0).sum())
    data  = [(l, s, c) for l, s, c in
             [("In stock", in_s, PALETTE["green"]),
              ("Out of stock", out_s, PALETTE["red"])] if s > 0]
    labels, sizes, colors = zip(*data)
    _, texts, autotexts = ax.pie(
        sizes, labels=labels, autopct="%1.1f%%", colors=colors,
        startangle=90, pctdistance=0.75,
        wedgeprops={"edgecolor": "white", "linewidth": 1.5},
    )
    for at in autotexts:
        at.set_fontsize(10); at.set_fontweight("bold"); at.set_color("white")
    ax.set_title("Stock availability", fontsize=13, fontweight="bold",
                 color=PALETTE["text"], pad=12)


def panel_top_books(ax, df):
    top = df[["title", "price"]].dropna().nlargest(15, "price").reset_index(drop=True)
    top["label"] = top["title"].apply(
        lambda t: (t[:40] + "…") if len(str(t)) > 40 else t)
    colors = plt.cm.RdYlGn_r(np.linspace(0.1, 0.9, len(top)))
    ax.barh(top["label"][::-1], top["price"][::-1],
            color=colors[::-1], edgecolor="white", linewidth=0.5)
    for i, (_, row) in enumerate(top[::-1].iterrows()):
        ax.text(row["price"] + top["price"].max() * 0.005, i,
                f"£{row['price']:.2f}", va="center", fontsize=8,
                color=PALETTE["text"])
    ax.set_xlabel("Price (£)", fontsize=9, color=PALETTE["subtext"])
    ax.tick_params(axis="y", labelsize=8)
    ax.xaxis.grid(True, linestyle="--", linewidth=0.5, alpha=0.6, color="#D1D5DB")
    ax.yaxis.grid(False)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_edgecolor("#E5E7EB"); spine.set_linewidth(0.8)
    ax.set_facecolor(PALETTE["panel"])
    ax.set_title("Top 15 most expensive books", fontsize=13,
                 fontweight="bold", color=PALETTE["text"], pad=12)


def main():
    log.info("=== Stage 2: Dashboard ===")
    if not INPUT_CSV.exists():
        raise FileNotFoundError(f"Run transform.py first. Not found: {INPUT_CSV}")

    df = pd.read_csv(INPUT_CSV)
    log.info("Loaded %d rows", len(df))

    fig = plt.figure(figsize=(18, 12), facecolor=PALETTE["bg"])
    fig.suptitle("Books Dataset — Analytical Dashboard", fontsize=18,
                 fontweight="bold", color=PALETTE["text"], y=0.98)

    gs = fig.add_gridspec(2, 2, hspace=0.38, wspace=0.32,
                          left=0.07, right=0.97, top=0.92, bottom=0.06)
    panel_price(fig.add_subplot(gs[0, 0]), df)
    panel_ratings(fig.add_subplot(gs[0, 1]), df)
    panel_availability(fig.add_subplot(gs[1, 0]), df)
    panel_top_books(fig.add_subplot(gs[1, 1]), df)

    total = len(df)
    n_avail   = int(df["availability"].sum())
    avg_price = f"£{df['price'].mean():.2f}"
    avg_rating= f"{df['rating'].mean():.2f} ★"
    fig.text(0.5, 0.005,
             f"Total books: {total}  |  In stock: {n_avail}  |  "
             f"Avg price: {avg_price}  |  Avg rating: {avg_rating}",
             ha="center", fontsize=9, color=PALETTE["subtext"])

    fig.savefig(OUTPUT_FILE, dpi=150, bbox_inches="tight",
                facecolor=PALETTE["bg"])
    log.info("Dashboard saved → %s", OUTPUT_FILE)
    plt.close(fig)
    log.info("=== Done ===")


if __name__ == "__main__":
    main()