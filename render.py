#!/usr/bin/env python
import sys
import cv2
from tqdm import tqdm, trange
from waveshare import epd2in9
from PIL import Image

SIZE = (296, 128)


def render(video_path, frame_number):
    cap = cv2.VideoCapture(video_path)
    print('video fetched!')
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if frame_number > frame_count:
        print("This video only has {0} frames".format(frame_count))
        exit(1)

    if frame_number >= 0:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number - 1)
        ret, cv_frame = cap.read()
        if not ret:
            print("Could not read frame {0} from video".format(frame_number))
            exit(1)

        image = Image.fromarray(cv_frame)
        image.thumbnail(SIZE, Image.ANTIALIAS)

        padded_image = Image.new('RGB', SIZE)
        x_offset = int((SIZE[0] - image.size[0]) / 2)
        y_offset = int((SIZE[1] - image.size[1]) / 2)
        padded_image.paste(image, (x_offset, y_offset))

        epd = epd2in9.EPD()
        epd.init(epd.lut_full_update)
        epd.display(epd.getbuffer(padded_image))
        epd.sleep()

    else:
        epd = epd2in9.EPD()
        print("init and clear")
        epd.init(epd.lut_full_update)
        epd.Clear(0xFF)
        epd.init(epd.lut_partial_update)

        for i in trange(frame_count):
            tqdm.set_description("displaying frame %d/%d" % (i, frame_count))
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, cv_frame = cap.read()
            if not ret:
                print("Could not read frame {0} from video".format(frame_number))
                exit(1)

            image = Image.fromarray(cv_frame)
            image.thumbnail(SIZE, Image.ANTIALIAS)

            padded_image = Image.new('RGB', SIZE)
            x_offset = int((SIZE[0] - image.size[0]) / 2)
            y_offset = int((SIZE[1] - image.size[1]) / 2)
            padded_image.paste(image, (x_offset, y_offset))

            epd.display(epd.getbuffer(padded_image))

        epd.sleep()


if __name__ == "__main__":
    video_path = sys.argv[1]
    if len(sys.argv) > 2: # only display one specified frame
        frame_number = int(sys.argv[2])
    else: # play entire video
        frame_number = -1
    try:
        render(video_path, frame_number)
    except KeyboardInterrupt:    
        print("ctrl + c:")
        epd.init(epd.lut_full_update)
        epd.Clear(0xFF)    
        print("Goto Sleep...")
        epd.sleep()
        exit()
