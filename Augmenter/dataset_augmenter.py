from __future__ import annotations

import argparse
from pathlib import Path

import albumentations as A
import cv2


VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def build_augmentation_pipeline(
	bw_prob: float,
	translate_prob: float,
	translate_limit: float,
) -> A.Compose:
	"""Define un pipeline base de aumentacion."""
	return A.Compose(
		[
			A.HorizontalFlip(p=0.5),
			A.Affine(
				translate_percent={"x": (-translate_limit, translate_limit), "y": (-translate_limit, translate_limit)},
				mode=cv2.BORDER_CONSTANT,
				cval=(0, 0, 0),
				p=translate_prob,
			),
			A.ShiftScaleRotate(
				shift_limit=0.0,
				scale_limit=0.2,
				rotate_limit=20,
				border_mode=cv2.BORDER_REFLECT,
				p=0.7,
			),
			A.RandomBrightnessContrast(
				brightness_limit=0.2,
				contrast_limit=0.2,
				p=0.5,
			),
			A.GaussianBlur(blur_limit=(3, 5), p=0.2),
			A.HueSaturationValue(
				hue_shift_limit=10,
				sat_shift_limit=10,
				val_shift_limit=10,
				p=0.3,
			),
			A.ToGray(p=bw_prob),
		]
	)


def is_image_file(path: Path) -> bool:
	return path.suffix.lower() in VALID_EXTENSIONS


def augment_single_image(
	image_path: Path,
	output_class_dir: Path,
	transform: A.Compose,
	num_aug: int,
) -> None:
	"""Genera N imagenes aumentadas desde una sola imagen."""
	image_bgr = cv2.imread(str(image_path))
	if image_bgr is None:
		print(f"[WARN] No se pudo leer: {image_path}")
		return

	image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

	stem = image_path.stem
	suffix = image_path.suffix.lower() if image_path.suffix else ".jpg"

	for i in range(num_aug):
		augmented = transform(image=image_rgb)
		aug_rgb = augmented["image"]
		aug_bgr = cv2.cvtColor(aug_rgb, cv2.COLOR_RGB2BGR)

		output_name = f"{stem}_aug_{i + 1}{suffix}"
		output_path = output_class_dir / output_name
		cv2.imwrite(str(output_path), aug_bgr)


def process_dataset(
	input_dir: Path,
	output_dir: Path,
	num_aug: int,
	bw_prob: float,
	translate_prob: float,
	translate_limit: float,
) -> None:
	"""Recorre carpetas por clase y aplica aumentacion a cada imagen."""
	transform = build_augmentation_pipeline(
		bw_prob=bw_prob,
		translate_prob=translate_prob,
		translate_limit=translate_limit,
	)

	class_dirs = [p for p in input_dir.iterdir() if p.is_dir()]
	if not class_dirs:
		print(f"[INFO] No se encontraron carpetas de clase en: {input_dir}")
		return

	output_dir.mkdir(parents=True, exist_ok=True)

	for class_dir in sorted(class_dirs):
		output_class_dir = output_dir / class_dir.name
		output_class_dir.mkdir(parents=True, exist_ok=True)

		image_files = [p for p in class_dir.iterdir() if p.is_file() and is_image_file(p)]
		if not image_files:
			print(f"[INFO] Sin imagenes validas en: {class_dir}")
			continue

		print(f"[INFO] Clase: {class_dir.name} | Imagenes: {len(image_files)}")

		for image_path in image_files:
			augment_single_image(
				image_path=image_path,
				output_class_dir=output_class_dir,
				transform=transform,
				num_aug=num_aug,
			)


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(
		description="Aumentacion basica de imagenes por carpetas de clase con Albumentations"
	)
	parser.add_argument(
		"--input-dir",
		type=Path,
		required=True,
		help="Carpeta raiz del dataset original (subcarpetas = clases)",
	)
	parser.add_argument(
		"--output-dir",
		type=Path,
		required=True,
		help="Carpeta donde se guardaran las imagenes aumentadas",
	)
	parser.add_argument(
		"--num-aug",
		type=int,
		default=3,
		help="Cuantas imagenes aumentadas generar por imagen original",
	)
	parser.add_argument(
		"--bw-prob",
		type=float,
		default=0.2,
		help="Probabilidad de convertir una imagen aumentada a blanco y negro (0.0 a 1.0)",
	)
	parser.add_argument(
		"--translate-prob",
		type=float,
		default=0.5,
		help="Probabilidad de aplicar traslacion con fondo negro visible (0.0 a 1.0)",
	)
	parser.add_argument(
		"--translate-limit",
		type=float,
		default=0.12,
		help="Maximo de traslacion relativa por eje (0.0 a 0.5)",
	)
	return parser.parse_args()


def main() -> None:
	args = parse_args()

	if not args.input_dir.exists():
		raise FileNotFoundError(f"No existe la carpeta de entrada: {args.input_dir}")

	if args.num_aug < 1:
		raise ValueError("--num-aug debe ser mayor o igual a 1")
	if not (0.0 <= args.bw_prob <= 1.0):
		raise ValueError("--bw-prob debe estar entre 0.0 y 1.0")
	if not (0.0 <= args.translate_prob <= 1.0):
		raise ValueError("--translate-prob debe estar entre 0.0 y 1.0")
	if not (0.0 <= args.translate_limit <= 0.5):
		raise ValueError("--translate-limit debe estar entre 0.0 y 0.5")

	process_dataset(
		input_dir=args.input_dir,
		output_dir=args.output_dir,
		num_aug=args.num_aug,
		bw_prob=args.bw_prob,
		translate_prob=args.translate_prob,
		translate_limit=args.translate_limit,
	)
	print("[DONE] Aumentacion completada")


if __name__ == "__main__":
	main()
