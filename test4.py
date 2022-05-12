# from rivagan import RivaGAN
# model = RivaGAN()
# model.fit("drive/MyDrive/RivaGAN/data/hollywood",batch_size=32, epochs=50)
# model.save("./data/model.pt")

from rivagan import RivaGAN
model = RivaGAN()
model.fit("/kaggle/input/ucf101/UCF101/UCF-101/",batch_size=32, epochs=75,
                                                        lr=1e-3)
# model.fit("/kaggle/input/ucfclipped/UCF-101/",batch_size=32, epochs=75)
# model.fit("UCF-101",batch_size=32, epochs=129)
# model.fit("/kaggle/input/hmdb51/HMDB51",batch_size=32, epochs=20)
model.save("./model.pt")