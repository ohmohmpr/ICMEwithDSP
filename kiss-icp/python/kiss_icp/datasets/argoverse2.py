# MIT License
#
# Copyright (c) 2022 Panyawat Rattana.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import importlib
import os
import sys

from av2.datasets.sensor.sensor_dataloader import SensorDataloader, Sweep
from av2.structures.cuboid import CuboidList
from av2.utils.io import TimestampedCitySE3EgoPoses, read_city_SE3_ego, read_feather

from pathlib import Path

class Argoverse2Dataset:
    def __init__(self, data_dir: Path, log_id: str, *_, **__):
        try:
            importlib.import_module("av2")
        except ModuleNotFoundError:
            print("av2 is not installed on your system")
            print('run "pip install av2"')
            sys.exit(1)

        self.scans_dir = Path.absolute(data_dir)
        self.dataset_dir = Path.absolute(data_dir)
        self.sequence_id = self.scans_dir.parts[-1]
        self.log_id = log_id
        self.split = "train"
        self.file_extension = "feather"

        self._dataset = SensorDataloader(
            self.scans_dir,
            with_annotations=True,
            with_cache=True,
        )

        logs_id = list(self._dataset.sensor_cache.index.unique("log_id"))

        if int(log_id) < len(logs_id) and int(log_id) >= 0:
            print(f"\nFound {len(logs_id)} keys\n")
            self.log_id = logs_id[int(log_id)]
        elif log_id == None or log_id not in logs_id:
            print("\nPlease find log_ig from this list\n")
            print(logs_id)
            print("\nUse first Key\n")
            self.log_id = logs_id[0]
        
        self._load_gt_poses_and_annotations()


    def __len__(self):
        return len(self._dataset.sensor_cache.xs((self.split, self.log_id, "lidar")).index)
    
    def __getitem__(self, idx):
        log_lidar_records = self._dataset.sensor_cache.xs((self.split, self.log_id, "lidar")).index
        timestamp_ns = log_lidar_records[idx]

        log_dir = self.dataset_dir / self.split / self.log_id
        sensor_dir = log_dir / "sensors"
        lidar_feather_path = sensor_dir / "lidar" / f"{timestamp_ns}.feather"
        sweep = Sweep.from_feather(lidar_feather_path=lidar_feather_path)
        # timestamp_city_SE3_ego_dict = read_city_SE3_ego(log_dir=log_dir)

        self.intensity = sweep.intensity/255
        return sweep.xyz, sweep.offset_ns

    def _load_annotations_with_spefic_category(self, split: str, log_id: str, sweep_timestamp_ns: int, category: str) -> CuboidList:
        """
        adapted from av2 lib
        Load the sweep annotations at the provided timestamp.

        Args:
            split: Split name.
            log_id: Log unique id.
            sweep_timestamp_ns: Nanosecond timestamp.

        Returns:
            Cuboid list of annotations.
        """
        annotations_feather_path = self.dataset_dir / self.split / self.log_id / "annotations.feather"

        # Load annotations from disk.
        # NOTE: This contains annotations for the ENTIRE sequence.
        # The sweep annotations are selected below.
        cuboid_list = CuboidList.from_feather(annotations_feather_path)
        cuboids = list(filter(lambda x: x.timestamp_ns == sweep_timestamp_ns and x.category == category , cuboid_list.cuboids))
        return CuboidList(cuboids=cuboids)
    
    def _load_gt_poses_and_annotations(self):
        print("Load Ground truth")
        timestamp_ns_list = list(self._dataset.sensor_cache.xs((self.split, self.log_id, "lidar")).index)
        self.gt_poses = []
        for timestamp_ns in timestamp_ns_list:
            self.gt_poses.append(self._load_annotations_with_spefic_category(
                self.split, self.log_id, timestamp_ns, "REGULAR_VEHICLE"))
        

