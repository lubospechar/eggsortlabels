import io
from reportlab.lib.pagesizes import A4, A3, landscape as set_landscape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import toColor


class EggSortLabels:
    """
    Tato třída slouží k vytváření PDF sady štítků pro třídění kmenových vajec.
    Umožňuje uživatelům specifikovat vzhled dokumentu, včetně rozměrů štítků,
    orientace stránky, a rozestupy mezi štítky. Lze ji použít pro ukládání dokumentu
    do souboru nebo přímé odeslání do paměti, což je vhodné pro webové aplikace.
    """

    def __init__(
        self,
        filename,
        pagesize="A3",
        margin_left=1,  # Levý okraj stránky
        margin_right=1,  # Pravý okraj stránky
        margin_top=2,  # Horní okraj stránky
        margin_bottom=2,  # Spodní okraj stránky
        label_size=(4.75, 2),  # Rozměry štítku
        landscape=False,  # Nastavení orientace stránky
        font_size=26,  # Velikost písma textu na štítku
        horizontal_spacing=0,  # Mezera mezi štítky ve vodorovném směru
        vertical_spacing=0,  # Mezera mezi štítky ve svislém směru
        save_to_memory=False,  # Uložení výsledku do paměti
        labels_per_odd_row=8,  # Počet štítků na lichém řádku
        labels_per_even_row=7,  # Počet štítků na sudém řádku
    ):
        """
        Konstruktor třídy, který inicializuje všechny potřebné atributy
        pro generování PDF dokumentu podle uživatelských specifikací.
        """
        self.filename = filename
        # Převod hodnot okrajů a velikosti štítku z cm na body
        self.margin_left = self.cm_to_points(margin_left)
        self.margin_right = self.cm_to_points(margin_right)
        self.margin_top = self.cm_to_points(margin_top)
        self.margin_bottom = self.cm_to_points(margin_bottom)
        self.label_size = (
            self.cm_to_points(label_size[0]),
            self.cm_to_points(label_size[1]),
        )
        self.font_size = font_size
        self.horizontal_spacing = self.cm_to_points(horizontal_spacing)
        self.vertical_spacing = self.cm_to_points(vertical_spacing)

        self.labels_per_odd_row = labels_per_odd_row
        self.labels_per_even_row = labels_per_even_row

        # Nastavení velikosti stránky a orientace
        if pagesize.upper() == "A4":
            base_pagesize = A4
        elif pagesize.upper() == "A3":
            base_pagesize = A3
        else:
            base_pagesize = A4
        self.pagesize = set_landscape(base_pagesize) if landscape else base_pagesize
        self.width, self.height = self.pagesize  # Uložení rozměrů stránky

        # Rozhodnutí o ukládání do paměti nebo do souboru
        if save_to_memory:
            self.buffer = io.BytesIO()  # Pro ukládání do paměti
            self.c = canvas.Canvas(self.buffer, pagesize=self.pagesize)
        else:
            if filename is None:
                raise ValueError("Musí být zadáno jméno souboru.")
            self.c = canvas.Canvas(
                filename, pagesize=self.pagesize
            )  # Pro ukládání do souboru

    @staticmethod
    def cm_to_points(cm):
        """Převádí centimetry na body pro použití v ReportLab."""
        return cm * 28.35

    def generate_labels_from_data(
        self, data, top_color="#FF0000", bottom_color="#000000"
    ):
        """
        Generuje a umisťuje štítky na PDF stránku na základě poskytnutých dat.
        Tato metoda umožňuje alternovat počet štítků na lichých a sudých řádcích.
        Vstupní data jsou očekávána ve formátu seznamu dvojic (tuplů), kde každá dvojice obsahuje
        horní a dolní hodnotu pro štítek. Barvy a tučnost textu lze také přizpůsobit.
        """
        x = self.margin_left
        y = (
            self.height - self.margin_top - self.label_size[1]
        )  # Začátek umístění prvního štítku
        last_top_number = None  # Uložení poslední horní hodnoty pro porovnání
        row_counter = 1  # Čítač řádků pro alternování počtu štítků
        labels_in_current_row = 0  # Počítadlo štítků v aktuálním řádku

        for index, label_data in enumerate(data):
            # Zjištění, zda je čas přejít na nový řádek
            if (
                row_counter % 2 == 1
                and labels_in_current_row >= self.labels_per_odd_row
            ) or (
                row_counter % 2 == 0
                and labels_in_current_row >= self.labels_per_even_row
            ):
                x = self.margin_left  # Reset x na začátek nového řádku
                y -= self.label_size[1] + self.vertical_spacing  # Posun na nový řádek
                labels_in_current_row = 0  # Reset počítadla štítků pro nový řádek
                row_counter += 1  # Inkrementace čítače řádků

            # Kontrola, jestli je potřeba začít novou stránku
            if y < self.margin_bottom:
                self.c.showPage()  # Vytvoření nové stránky
                x = self.margin_left
                y = (
                    self.height - self.margin_top - self.label_size[1]
                )  # Reset y na začátek pro novou stránku
                row_counter = 1  # Reset čítače řádků pro novou stránku
                labels_in_current_row = 0

            # Vykreslení obdélníku štítku
            self.c.setStrokeColor(toColor("#000000"))  # Nastavení barvy okraje
            self.c.rect(x, y, self.label_size[0], self.label_size[1], stroke=1, fill=0)

            # Tisk horního čísla, pokud se liší od posledního vytisknutého
            if label_data[0] != last_top_number:
                self.c.setFillColor(toColor(top_color))
                self.c.setFont("Helvetica-Bold", self.font_size)
                self.c.drawString(
                    x + 5, y + self.label_size[1] - 25, str(label_data[0])
                )
                last_top_number = label_data[0]  # Aktualizace poslední horní hodnoty

            # Tisk dolního čísla
            if len(label_data) > 1:
                self.c.setFillColor(toColor(bottom_color))
                text_width = self.c.stringWidth(
                    str(label_data[1]), "Helvetica-Bold", self.font_size
                )
                self.c.setFont("Helvetica-Bold", self.font_size)
                self.c.drawString(
                    x + self.label_size[0] - text_width - 5, y + 5, str(label_data[1])
                )

            x += (
                self.label_size[0] + self.horizontal_spacing
            )  # Posunutí pro další štítek v řadě
            labels_in_current_row += (
                1  # Inkrementace počítadla štítků v aktuálním řádku
            )

    def save(self):
        """
        Ukládá vygenerované PDF. Pokud je dokument ukládán do paměti,
        vrací jeho binární obsah. V opačném případě je dokument uložen do souboru.
        """
        self.c.save()
        if hasattr(self, "buffer"):
            return self.buffer.getvalue()
