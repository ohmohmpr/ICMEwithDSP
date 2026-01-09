import numpy as np
from bbox import  BBox3D, BBox2D
from bbox.metrics import iou_3d, iou_2d
from pyquaternion import Quaternion
import warnings


class Instance():
    def __init__(self, bbox: BBox2D, id: int):
        self._id = id
        self._color = np.random.rand(1, 3)
        self.bbox = bbox

class Tracker():
    def __init__(self):
        self._instances_in_frame = {}
        self._instances = []
        self.id = 0 # diry fix, fix with design pattern.
        pass

    def add(self, instances):

        # if (len(self._instances) > 0):
        #     prev_dist = np.sort(np.linalg.norm(self._instances[:, :3].cpu(), axis=1))
        #     print("previous", prev_dist)
        # current_dist = np.sort(np.linalg.norm(instances[:, :3].cpu(), axis=1))
        # print("current", current_dist)
        instances = instances.tolist()

        warnings.simplefilter(action='ignore', category=DeprecationWarning) # ICMEwithDSP modified, dirty fix
        if (len(self._instances) == 0):
            for current_car in instances:
                self._instances.append(Instance(BBox2D([*current_car[:2], *current_car[3:5]]), self.id))
                self.id = self.id + 1
                print("INIT", self.id)

        elif (len(self._instances) > 0):
            i_prev = 0
            for prev_car in self._instances:
                i_curr = 0
                current_iou_max = 0
                is_found = False
                for current_car in instances:

                    # Slow
                    # prev_car_bbox = BBox3D(*prev_car[:6], q= Quaternion( axis=[0.0, 0.0, 1.0], radians=prev_car[6])    )
                    # current_car_bbox = BBox3D(*current_car[:6], q= Quaternion( axis=[0.0, 0.0, 1.0], radians=current_car[6]) )
                    # iou = iou_3d(prev_car_bbox, current_car_bbox)

                    # print(*prev_car[:2], *prev_car[3:5], *current_car[:2], *current_car[3:5])
                    # Not that slow
                    prev_car_bbox = prev_car.bbox
                    current_car_bbox = BBox2D([*current_car[:2], *current_car[3:5]])
                    iou = iou_2d(prev_car_bbox, current_car_bbox)


                    # print("test")
                    if iou > 0.3:
                      is_found = True
                      current_iou_max = iou
                      idx_current_iou_max = i_curr
                      current_car_bbox_max = current_car_bbox
                      # print("MATCH", prev_car_bbox, current_car_bbox, iou, i_curr)
                      # print("\n")
                    i_curr = i_curr + 1
                
                if is_found:
                  # UPDATE
                  prev_car.bbox = current_car_bbox
                  instances.pop(idx_current_iou_max)
                  # print("MAX", prev_car_bbox, current_car_bbox_max, current_iou_max, idx_current_iou_max)
                  pass

            for current_car in instances:
                # CREATION
                self._instances.append(Instance(BBox2D([*current_car[:2], *current_car[3:5]]), self.id))
                self.id = self.id + 1
                print("CREATION", self.id)

                #

        print("\n")

    def get(self):
        pass