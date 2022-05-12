import os
from glob import glob
from random import randint
import numpy as np
import cv2
import torch
from torch.utils.data import DataLoader, Dataset


class VideoDataset(Dataset):
    """
    Given a folder of *.avi video files organized as shown below, this dataset
    selects randomly crops the video to `crop_size` and returns a random
    continuous sequence of `seq_len` frames of shape.

        /root_dir
            1.avi
            2.avi

    The output has shape (3, seq_len, crop_size[0], crop_size[1]).
    """

    def __init__(self, root_dir, crop_size, seq_len, max_crop_size=(360, 480)):
        self.seq_len = seq_len
        self.crop_size = crop_size
        self.max_crop_size = max_crop_size

        self.videos = []
        for ext in ["avi", "mp4"]:
            for path in glob(os.path.join(root_dir, "**/*.%s" % ext), recursive=True):
                cap = cv2.VideoCapture(path)
                nb_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                self.videos.append((path, nb_frames))

    def __len__(self):
        return len(self.videos)

    def __getitem__(self, idx):
        # Select time index
      
        path, nb_frames = self.videos[idx]
        start_idx = randint(0, nb_frames - self.seq_len - 1)

        # Select space index
        cap = cv2.VideoCapture(path)
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_idx - 1)
        ok, frame = cap.read()
        try:
            H, W, D = frame.shape
            x, dx, y, dy = 0, W, 0, H
            if self.crop_size:
                dy, dx = self.crop_size
                x = randint(0, W - dx - 1)
                y = randint(0, H - dy - 1)
            if self.max_crop_size[0] < dy:
                dy, dx = self.max_crop_size
                y = randint(0, H - dy - 1)
            if self.max_crop_size[1] < dx:
                dy, dx = self.max_crop_size
                x = randint(0, W - dx - 1)
        except:
            pass
        # Read frames and normalize to [-1.0, 1.0]

        frames = []
        for _ in range(self.seq_len):
            try:
                ok, frame = cap.read()
                frame = frame[y:y + dy, x:x + dx]
                frames.append(frame / 127.5 - 1.0)
            except:
                pass
#A9A9A9
        # np.set_printoptions(threshold=np.inf)
        # print(frames)   
        # print("next frame")
        # exit()

        try:
            x = torch.FloatTensor(frames)
            x = x.permute(3, 0, 1, 2)
        except:
        #    ../input/ucfclipped/UCF-101/UCF/ApplyEyeMakeup/v_ApplyEyeMakeup_g22_c03.avi
            path, nb_frames = self.videos[1]
            start_idx = randint(0, nb_frames - self.seq_len - 1)

            # Select space index
            cap = cv2.VideoCapture(path)
            cap.set(cv2.CAP_PROP_POS_FRAMES, start_idx - 1)
            ok, frame = cap.read()
            try:
                H, W, D = frame.shape
                x, dx, y, dy = 0, W, 0, H
                if self.crop_size:
                    dy, dx = self.crop_size
                    x = randint(0, W - dx - 1)
                    y = randint(0, H - dy - 1)
                if self.max_crop_size[0] < dy:
                    dy, dx = self.max_crop_size
                    y = randint(0, H - dy - 1)
                if self.max_crop_size[1] < dx:
                    dy, dx = self.max_crop_size
                    x = randint(0, W - dx - 1)
            except:
                pass
            # Read frames and normalize to [-1.0, 1.0]

            frames = []
            for _ in range(self.seq_len):
                try:
                    ok, frame = cap.read()
                    frame = frame[y:y + dy, x:x + dx]
                    frames.append(frame / 127.5 - 1.0)
                except:
                    pass
            x = torch.FloatTensor(frames)
            x = x.permute(3, 0, 1, 2)
           


        
    
        
        return x


def load_train_val(seq_len, batch_size, dataset="hollywood2"):
    """
    This returns two dataloaders correponding to the train and validation sets. Each
    iterator yields tensors of shape (N, 3, L, H, W) where N is the batch size, L is
    the sequence length, and H and W are the height and width of the frame.

    The batch size is always 1 in the validation set. The frames are always cropped
    to (128, 128) windows in the training set. The frames in the validation set are
    not cropped if they are smaller than 360x480; otherwise, they are cropped so the
    maximum returned size is 360x480.
    """
    print("%s/train" % dataset)
    train = DataLoader(VideoDataset(
        "%s/UCF" % dataset,
        # "%s/train" % dataset,
        crop_size=(90, 90),
        seq_len=seq_len,
    ), shuffle=False, num_workers=20, batch_size=batch_size, pin_memory=True)

    # val = DataLoader(VideoDataset(
        # "%s/ApplyEyeMakeup" % dataset,
    #     # "/kaggle/input/deepfake-detection-challenge/test_videos/",
    #     # "/kaggle/input/faceforensics/manipulated_sequences/Face2Face/c23/videos/",
    #     #  "/kaggle/input/faceforensics/original_sequences/youtube/c23/videos/",
    #     crop_size=False,
    #     seq_len=seq_len,
    # ), shuffle=False, batch_size=1, pin_memory=True)
# /kaggle/input/ucf101/UCF101/UCF-101/
    val = DataLoader(VideoDataset(
        # "%s/val" % dataset,
        # "/kaggle/input/faceforensics/manipulated_sequences/Face2Face/c23/videos",
        "/kaggle/input/hollywood/val",
        #  "/kaggle/input/faceforensics/original_sequences/youtube/c23/videos/",
        crop_size=(90 , 90),
        seq_len=seq_len,
    ), shuffle=True, batch_size=batch_size, pin_memory=True)

    return train, val
