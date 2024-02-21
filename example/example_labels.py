import sys

sys.path.append("../")

from eggsortlabels import EggSortLabels

filename = "example_data.csv"

# standardní načtení csv a vytvoření listu
with open(filename, "r") as file:
    next(file)
    data = [(int(p1), int(p2)) for p1, p2 in (line.strip().split(",") for line in file)]


# vytvoření objektu
pdf_file = EggSortLabels(
    filename="example_labels.pdf",
    landscape=True,
)

# načtení a vykreslení dat
pdf_file.generate_labels_from_data(data)

# uložení
pdf_file.save()
