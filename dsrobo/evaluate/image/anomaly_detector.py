from pathlib import Path
from typing import Optional, Type
from collections import OrderedDict

import cv2
import numpy


class AnomalyModel:
    def fit(self, images: dict[str, numpy.ndarray]):
        raise NotImplementedError()

    def evaluate(self, image: numpy.ndarray):
        raise NotImplementedError()


class AbsSumAnomalyModel(AnomalyModel):
    def __init__(self):
        self.model = None

    def fit(self, images: dict[str, numpy.ndarray]):
        mean_img = numpy.mean(list(images.values()), axis=0, dtype='float32')
        self.model = mean_img

    def evaluate(self, image: numpy.ndarray):
        assert image.shape == self.model.shape
        abs_diff = numpy.abs(image - self.model)
        abs_diff_sum = abs_diff.sum(axis=0).sum()
        return abs_diff_sum


class EvaluateAnomalyDetector(object):
    def __init__(self, model_cls: Type[AnomalyModel] = AbsSumAnomalyModel):
        self.model = model_cls()

    def sample_img(self,
                   images: dict[str, numpy.ndarray],
                   dump_to: Optional[Path] = None):
        key = list(images.keys())[0]
        if dump_to is not None:
            cv2.imwrite(str(dump_to), images[key])
        return images[key]

    def fit_model(self, images: dict[str, numpy.ndarray]):
        self.model.fit(images)

    def evaluate(self, images: dict[str, numpy.ndarray]):
        results = {key: self.model.evaluate(image) for key, image in images.items()}
        sorted_results = sorted(results.items(), key=lambda v: v[1], reverse=True)
        od = OrderedDict()
        for key, value in sorted_results:
            od[key] = value
        return od
