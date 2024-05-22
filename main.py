import os
import sys
from typing import NoReturn, Optional, Union

try:
  import PIL.Image
except ImportError:
  print("PIL is required to run the script, install it using: `pip install pillow`")
  sys.exit(1)


# types
Image = PIL.Image.Image
Color = Union[tuple[int, int, int], tuple[int, int, int, int]]
Args = tuple[str, Optional[str]]


# remove colors from an image
def remove_colors_from_image(
  image: Image, 
  colors: list[Color],
) -> Image:
  # get image pixels
  pixels = image.load()
  assert pixels is not None, "Failed to load image pixels"

  # get image size
  (width, height) = image.size
  print(f"Image size: {width}x{height}")

  # count number of pixels removed
  num_removed = 0

  # iterate over all pixels
  for y in range(height):
    for x in range(width):
      pixel = pixels[x, y]

      # check if pixel color is in the list of colors to remove
      if pixel[:3] in colors:
        # set as transparent
        pixels[x, y] = (0, 0, 0, 0)
        num_removed += 1

  if num_removed == 0:
    print("No pixels removed from image, something might be wrong, check your input image")
  else:
    print(f"Removed {num_removed:,d} pixels from image")

  return image


# print usage
def usage(msg: Optional[str] = None) -> NoReturn:
  print(msg or f"Usage: python {sys.argv[0]} <input_path> [output_path]")
  sys.exit(1)


# parse arguments
def parse_args() -> Args:
  if len(sys.argv) < 2:
    usage()

  # get input image path
  input_path = sys.argv[1]

  # get output image path
  if len(sys.argv) > 2:
    output_path = sys.argv[2]
    if not output_path.endswith(".png"):
      usage("Output path must be a PNG file.")
  else:
    output_path = None

  return (input_path, output_path)


# main
def main() -> None:
  # parse arguments
  (input_path, output_path) = parse_args()

  # load input image
  input_image = PIL.Image.open(input_path).convert("RGBA")

  # remove white pixels from image
  output_image = remove_colors_from_image(
    input_image,
    [ (255, 255, 255) ],
  )

  # save output image
  if output_path is None:
    output_path = os.path.dirname(input_path) + "/transparent_" + os.path.basename(input_path)
    output_path = output_path.rsplit(".", 1)[0] + ".png"
  output_image.save(output_path)
  
  print("Modified image saved to:", output_path)


if __name__ == "__main__":
  main()
