from rivagan import RivaGAN
import os

model = RivaGAN()
data = tuple([40] * 32)
print(data)
# model = RivaGAN.load("data/model.pt")
model = RivaGAN.load("/kaggle/input/rivariva/data/model.pt")
directory="./"
directory="/kaggle/input/tiktok-trending-december-2020/videos/"
for filename in os.listdir(directory):
    if filename.endswith(".mp4") or filename.endswith(".avi"): 
        model.encode("test2.avi", data, "train2.avi")
    else:
        continue

# https://syedmujtaba.com.pk/?code=4%2F0AX4XfWjbzeh0q8tfrtjnse0EryJVPHrYunMcwPKl5PsYbZcM6cvJ35C2I62bfuVcSfkZVA&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcalendar