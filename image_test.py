from python_imagesearch.imagesearch import imagesearch, imagesearcharea
from pathlib import Path

img = "crayfish.png"
file_to_open = Path(f"./assets/{img}")

pos = imagesearch(str(file_to_open))
# pos = imagesearcharea(str(file_to_open),0,0,800,600)
if pos[0] != -1:
    print("position : ", pos[0] - 1090, pos[1])
else:
    print("image not found")
