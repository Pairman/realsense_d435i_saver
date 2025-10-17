#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
import os
import sys
import time
import cv2
import numpy as np
import pyrealsense2 as rs

# quiet save option
flag_is_quiet = "-q" in sys.argv

# create save path
save_path = os.path.join(
    os.getcwd(), "out",
    datetime.now().strftime("%Y-%m-%d_%H:%M:%S.%f"))
color_save_path = os.path.join(save_path, "color")
depth_save_path = os.path.join(save_path, "depth")
os.makedirs(color_save_path, exist_ok=True)
os.makedirs(depth_save_path, exist_ok=True)

# create config
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

if __name__ == "__main__":
    print(f"output path: {save_path}")
    # frame aligner to color frame
    align = rs.align(rs.stream.color)
    # start pipeline
    pipeline = rs.pipeline()
    profile = pipeline.start(config)
    # get depth scale
    depth_meter = 8
    depth_scale = profile.get_device().first_depth_sensor().get_depth_scale()
    depth_alpha = 255.0 * depth_scale / depth_meter
    print(f"depth scale: {depth_scale}, max distance: {depth_meter}")
    # wait for stabilization
    print("starting...")
    time.sleep(2.5)
    try:
        while frames := align.process(pipeline.wait_for_frames()):
            # get frame
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            if not depth_frame or not color_frame:
                continue
            # get timestamp
            ts = datetime.now().strftime("%Y-%m-%d_%H:%M:%S.%f")
            # save color frame
            cv2.imwrite(
                os.path.join(color_save_path, f"{ts}.png"),
                np.asanyarray(color_frame.get_data()))
            # save depth frame
            np.save(
                os.path.join(depth_save_path, f"{ts}.npy"),
                np.asanyarray(depth_frame.get_data(), dtype="float16"))
            # cv2.imwrite(
            #     os.path.join(depth_save_path, f"{ts}.png"),
            #     cv2.convertScaleAbs(np.asanyarray(depth_frame.get_data()),
            #     alpha=depth_alpha))
            if not flag_is_quiet:
                print(f"saved: {ts}")
    except KeyboardInterrupt:
        print("stopping...")
    finally:
        # stop pipeline
        pipeline.stop()
