from collections import OrderedDict
from pathlib import Path
from typing import Optional

import cv2
import numpy


def assert_find(directory: Path, pattern: str):
    found = list(directory.glob(pattern))
    assert len(found) == 1
    return found[0]


def load_image(path: Path, interest_region: Optional[tuple[int, int, int, int]] = None) -> numpy.ndarray:
    img = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if interest_region is not None:
        x, y, w, h = interest_region
        crop = img[y:y + h, x:x + w]
        return crop
    return img


def load_images(job_dir: Path, iteration_job_no: int, image_job_no: int, image_name: str,
                interest_region: Optional[tuple[int, int, int, int]] = None) -> dict[str, numpy.ndarray]:
    iteration_job_dir = assert_find(job_dir, f"{iteration_job_no}_*")
    image_files = {iter_dir.stem: assert_find(iter_dir, f"{image_job_no}_*/{image_name}")
                   for iter_dir in iteration_job_dir.glob("*") if iter_dir.is_dir()}
    return {iter_no: load_image(iter_path, interest_region)
            for iter_no, iter_path in image_files.items()}


def dump_result(dest_root: Path, images: dict[str, numpy.ndarray], scores: OrderedDict) -> None:
    n_imgs = len(images)
    n_digits = len(str(n_imgs))
    dest_root.mkdir(exist_ok=True, parents=True)
    for i, (key, score) in enumerate(scores.items()):
        dest_name = f"{str(i).zfill(n_digits)}-{key}-{score}.png"
        dest_path = dest_root / dest_name
        cv2.imwrite(str(dest_path), images[key])
