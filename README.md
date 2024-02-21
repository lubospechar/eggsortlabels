# EggSortLabels

Třída `EggSortLabels` slouží k vytváření PDF sady štítků pro třídění kmenových vajec. Umožňuje uživatelům flexibilně specifikovat vzhled dokumentu, včetně rozměrů štítků, orientace stránky a rozestupů mezi štítky. Dokument lze ukládat buď do souboru nebo přímo do paměti, což je ideální pro webové aplikace.

## Funkce

- Nastavení velikosti štítku, okrajů, orientace stránky a velikosti písma.
- Možnost ukládat vygenerované PDF do souboru nebo do paměti.
- Specifikace počtu štítků na lichých a sudých řádcích pro optimalizované rozmístění.
- Nastavení barvy a tučnosti písma pro horní a dolní hodnoty na štítcích.

## Instalace

Třída `EggSortLabels` vyžaduje [Python](https://python.org) a knihovnu [ReportLab](https://www.reportlab.com/dev/docs/).

Instalaci knihovny ReportLab můžete provést pomocí pip:
pip install reportlab


## Použití

Pro generování PDF sady štítků s využitím třídy `EggSortLabels`, postupujte podle následujícího příkladu:

```python
from eggsortlabels import EggSortLabels

# Vytvoření instance třídy s požadovanou konfigurací
labels = EggSortLabels(
    filename="output_labels.pdf",  # Název výstupního souboru
    pagesize="A4",  # Velikost stránky
    margin_left=1,  # Levý okraj
    margin_right=1,  # Pravý okraj
    margin_top=2,  # Horní okraj
    margin_bottom=2,  # Spodní okraj
    label_size=(4.75, 2),  # Velikost štítku (šířka, výška) v centimetrech
    landscape=False,  # Orientace stránky
    font_size=26,  # Velikost písma
    horizontal_spacing=0.5,  # Horizontální mezera mezi štítky
    vertical_spacing=1,  # Vertikální mezera mezi štítky
    save_to_memory=False,  # Uložit do paměti nebo do souboru
    labels_per_odd_row=8,  # Počet štítků na lichý řádek
    labels_per_even_row=7  # Počet štítků na sudý řádek
)

# Data pro generování štítků
data = [
    (1, "5"),
    (1, "18"),
    (2, "22"),
    (2, "28")
    # další data...
]

# Generování štítků z dat
labels.generate_labels_from_data(data, top_color="#FF0000", bottom_color="#000000")

# Uložení výsledného PDF
labels.save()
```


Tento příklad demonstruje základní použití třídy pro vytvoření a uložení sady štítků do PDF souboru. Můžete upravit konfiguraci třídy podle svých potřeb, včetně rozměrů štítků, okrajů, orientace stránky a mezery mezi štítky. Flexibilita třídy umožňuje jednoduše přizpůsobit výstup různým požadavkům a využití scénářům.

## Konfigurace

Třída `EggSortLabels` nabízí následující konfigurační možnosti:

- `filename`: Cesta a název výstupního PDF souboru. Pokud je `save_to_memory=True`, tento parametr se ignoruje.
- `pagesize`: Velikost stránky, podporované hodnoty jsou `"A4"` a `"A3"`.
- `margin_left`, `margin_right`, `margin_top`, `margin_bottom`: Okraje stránky v centimetrech.
- `label_size`: Dvojice hodnot určující šířku a výšku štítku v centimetrech.
- `landscape`: Boolean hodnota určující, zda má být stránka v orientaci na šířku.
- `font_size`: Velikost písma textu na štítku.
- `horizontal_spacing`, `vertical_spacing`: Mezery mezi štítky v centimetrech.
- `save_to_memory`: Pokud `True`, výsledek se uloží do paměti místo do souboru.
- `labels_per_odd_row`, `labels_per_even_row`: Určuje počet štítků na lichém a sudém řádku.

Použití těchto konfiguračních možností umožňuje detailní přizpůsobení vzhledu výsledného PDF dokumentu, což činí třídu `EggSortLabels` velmi univerzálním nástrojem pro generování štítků.
