import time
import edgeiq
import os
import json
from posture import CheckPosture


def main():

    posture = CheckPosture()

    pose_estimator = edgeiq.PoseEstimation("alwaysai/human-pose")
    pose_estimator.load(engine=edgeiq.Engine.DNN)

    print("Loaded model:\n{}\n".format(pose_estimator.model_id))
    print("Engine: {}".format(pose_estimator.engine))
    print("Accelerator: {}\n".format(pose_estimator.accelerator))

    fps = edgeiq.FPS()

    try:
        with edgeiq.WebcamVideoStream(cam=0) as video_stream, \
                edgeiq.Streamer() as streamer:
            # Allow Webcam to warm up
            time.sleep(2.0)
            fps.start()

            # loop detection
            while True:
                frame = video_stream.read()
                results = pose_estimator.estimate(frame)
                # Generate text to display on streamer
                text = ["Model: {}".format(pose_estimator.model_id)]
                text.append(
                    "Inference time: {:1.3f} s".format(results.duration))
                for ind, pose in enumerate(results.poses):
                    text.append("Person {}".format(ind))
                    text.append('-'*10)

                    # update the instance key_points to check the posture
                    posture.set_key_points(pose.key_points)
                    # play a reminder if you are not sitting up straight
                    correct_posture = posture.correct_posture()
                    if not correct_posture:
                        text.append(posture.build_message())
                    # make a sound to alert the user to improper posture
                    print("\a")
                streamer.send_data(results.draw_poses(frame), text)

                fps.update()

                if streamer.check_exit():
                    break

                streamer.send_data(results.draw_poses(frame), text)

                fps.update()
                if streamer.check_exit():
                    break
    finally:
        fps.stop()
        print("elapsed time: {:.2f}".format(fps.get_elapsed_seconds()))
        print("approx. FPS: {:.2f}".format(fps.compute_fps()))

        print("Program Ending")


if __name__ == "__main__":
    main()
