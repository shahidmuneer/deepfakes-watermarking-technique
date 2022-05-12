from rivagan import RivaGAN
import os

model = RivaGAN()
data = tuple([40] * 32)
print(data)
# model = RivaGAN.load("/kaggle/input/rivariva/data/model.pt")
model = RivaGAN.load("data/model.pt")

# model.encode("superman.mp4", data, "supermantrained.mp4")
directory="testdataset"
# directory="/kaggle/input/rivariva/testdataset"
# directory="/kaggle/input/tiktok-trending-december-2020/videos/"
for filename in os.listdir(directory):
    if filename.endswith(".mp4") or filename.endswith(".avi"): 
        model.encode(os.path.join(directory, filename), data, "encodedvideos/"+filename+"trained.mp4")
    else:
        continue