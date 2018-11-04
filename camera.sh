#!/bin/bash
sudo uv4l -nopreview --auto-video_nr --driver raspicam --encoding mjpeg --rotation 180 --width 320 --height 240 --framerate 20 --vstab yes --server-option '--port=9090' --server-option '--max-queued-connections=30' --server-option '--max-streams=5' --server-option '--max-threads=29'
