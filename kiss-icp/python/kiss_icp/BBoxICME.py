import numpy as np
import torch
from scipy.spatial.transform import Rotation as R

class BBoxICME():
    def __init__(self, bounding_box):
        
        if isinstance(bounding_box, torch.Tensor):
            self.center  = bounding_box[0:3].cpu().detach().numpy()
            self.l, self.w, self.h = bounding_box[3:6].cpu().detach().numpy()
            self.heading = np.array([0, 0, bounding_box[6].cpu().detach().numpy() + 1e-10])
            self.R = R.from_rotvec( self.heading )
            self.R_mtx = self.R.as_matrix()
            self.R_mtx_homo = np.vstack(( np.hstack((self.R_mtx, np.array([[0], [0], [0]]) )), np.array([0, 0, 0, 1])))

        elif isinstance(bounding_box, np.ndarray):
            self.center  = bounding_box[0:3]
            self.l, self.w, self.h = bounding_box[3:6]
            self.heading = np.array([0, 0, bounding_box[6] + 1e-10])
            self.R = R.from_rotvec( self.heading )
            self.R_mtx = self.R.as_matrix()
            self.R_mtx_homo = np.vstack(( np.hstack((self.R_mtx, np.array([[0], [0], [0]]) )), np.array([0, 0, 0, 1])))

    def get_points_in_bbox(self, pts_frame) -> np.array:
        # compared to c++ performance
        centered_pts = pts_frame - self.center

        x_axis = self.R_mtx[:, 0].T
        y_axis = self.R_mtx[:, 1].T
        z_axis = self.R_mtx[:, 2].T
        point_in_x_idx  = np.abs(np.dot(centered_pts, x_axis )) <= self.l / 2
        point_in_y_idx  = np.abs(np.dot(centered_pts, y_axis )) <= self.w / 2
        point_in_z_idx  = np.abs(np.dot(centered_pts, z_axis )) <= self.h / 2
        all = np.logical_and(point_in_x_idx, point_in_y_idx, point_in_z_idx)
        pts_in_bbox = centered_pts[all]

        return pts_in_bbox + self.center
    
    def get_vertices_nodes(self):
        """
              7 -------- 4
             /|         /|
            6 -------- 5 .
            | |        | |
            . 3 -------- 0
            |/         |/
            2 -------- 1
        Args:
            boxes3d:  (N, 7) [x, y, z, dx, dy, dz, heading], (x, y, z) is the box center

        Returns:
        """
        dx = self.l / 2
        dy = self.w / 2
        dz = self.h / 2

        min_x = - dx
        max_x = + dx
        min_y = - dy
        max_y = + dy
        min_z = - dz
        max_z = + dz

        node_0 = [max_x, max_y, min_z]
        node_1 = [max_x, min_y, min_z] 
        node_2 = [min_x, min_y, min_z]
        node_3 = [min_x, max_y, min_z]
        node_4 = [max_x, max_y, max_z]
        node_5 = [max_x, min_y, max_z]
        node_6 = [min_x, min_y, max_z]
        node_7 = [min_x, max_y, max_z]

        self.nodes = np.array([node_0, node_1, node_2, node_3,
                          node_4, node_5, node_6, node_7])

        self.edges = np.array([[0, 1], [0, 3], [0, 4], 
                          [1, 2], [1, 5], [2, 3], [2, 6],
                          [3, 7], 
                          [4, 5], [4, 7], [5, 6], [6, 7]])

        self.nodes = (
              self.R_mtx_homo @ 
              np.hstack((self.nodes, np.ones((self.nodes.shape[0],1)) )).T
        ).T[:, 0:3] + np.array([self.center])

        return self.nodes, self.edges