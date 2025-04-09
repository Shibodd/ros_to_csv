Example command:

python3 ros_to_csv/bag_to_csv.py \
  -t ros_to_csv/topicfile.yaml \
  -b mille_lat1_record/ \
  -o exported_mille_lat1 \
  -m /workspace/src/odometry_debug_msgs/msg/FilterState.msg \
     /workspace/src/odometry_debug_msgs/msg/ImuBias.msg \
     /workspace/src/vesc_msgs/msg/VescImu.msg \
     /workspace/src/vesc_msgs/msg/VescImuStamped.msg \
     /workspace/src/vesc_msgs/msg/VescState.msg \
     /workspace/src/vesc_msgs/msg/VescStateStamped.msg \
     /opt/ros/foxy/share/ackermann_msgs/msg/AckermannDriveStamped.msg \
     /opt/ros/foxy/share/ackermann_msgs/msg/AckermannDrive.msg