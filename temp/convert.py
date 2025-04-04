from PIL import Image


def convert_webp_to_png(input_path: str, output_path: str) -> None:
    # Open the .webp image
    with Image.open(input_path) as img:
        # Convert and save as .png
        img.thumbnail((1000, 1000))
        img.save(output_path, "PNG")


if __name__ == "__main__":
    # Replace these with your actual file paths
    input_file = "uploaded_files/example-receipt.webp"
    output_file = "uploaded_files/example-receipt.png"

    convert_webp_to_png(input_file, output_file)
    print(f"Converted {input_file} to {output_file}")
