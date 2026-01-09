# MIT License
#
# Copyright (c) 2022 Ignacio Vizzo, Tiziano Guadagnino, Benedikt Mersch, Cyrill
# Stachniss.
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
from typing import Optional

from pydantic import BaseModel


class DataConfig(BaseModel):
    max_range: float = 100.0
    min_range: float = 0.0
    deskew: bool = True


class MappingConfig(BaseModel):
    voxel_size: Optional[float] = None  # default: take it from data
    max_points_per_voxel: int = 20


class RegistrationConfig(BaseModel):
    max_num_iterations: Optional[int] = 500
    convergence_criterion: Optional[float] = 0.0001
    max_num_threads: Optional[int] = 0  # 0 means automatic


class AdaptiveThresholdConfig(BaseModel):
    fixed_threshold: Optional[float] = None
    initial_threshold: float = 2.0
    min_motion_th: float = 0.1

class OpenPCDetConfig(BaseModel):
    cfg_file: str = "cfgs/kitti_models/pv_rcnn.yaml"
    ckpt: str = "pv_rcnn_8369.pth"
    data_path: str = "~/data/KITTI/sequences/00/velodyne/"

class DSPSLAMConfig(BaseModel):
    data_type: str = "KITTI"
    # detect_online: bool = False
    # path_label_3d: "data/dsp_slam/kitti/07/labels/pointpillars_labels"
    # path_label_2d: "data/dsp_slam/kitti/07/labels/maskrcnn_labels"
    # Detector3D: 
    #     config_path: "configs/config_pointpillars.py"
    #     weight_path: "weights/pointpillars/model.pth"
    # Detector2D:
    #     config_path: "configs/config_maskrcnn.py"
    #     weight_path: "weights/maskrcnn/model.pth"
    min_bb_area: Optional[float] = 1600
    min_mask_area: Optional[float] = 1000
    downsample_ratio: Optional[float] = 4.0
    num_lidar_max: Optional[float] = 500
    num_lidar_min: Optional[float] = 10
    DeepSDF_DIR: str = "weights/deepsdf/cars_64"
    voxels_dim: Optional[float] = 32
    optimizer: dict = {}
    #     code_len: Optional[float] = 64,
    #     num_depth_samples: Optional[float] = 50,
    #     cut_off_threshold: Optional[float] = 0.01,
    #     joint_optim: list = [
    #         k1: Optional[float] = 1.0
    #         k2: Optional[float] = 100.0
    #         k3: Optional[float] = 0.25
    #         k4: Optional[float] = 1e07
    #         b1: Optional[float] = 0.20
    #         b2: Optional[float] = 0.025
    #     ],
    #     num_iterations: Optional[float] = 10
    #     learning_rate: Optional[float] = 1.0
    #     scale_damping: Optional[float] = 100.0
    #     pose_only_optim: list = [
    #         num_iterations: Optional[float] = 5
    #         learning_rate: Optional[float] = 1.0
    #     ],
    # ]
    # viewer:
    #     "distance": 150.0
    #     "tilt": 45.0
    #     "frame_size": 10.0