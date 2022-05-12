from rivagan import RivaGAN

model = RivaGAN.load("data/model.pt")
# print(model)
recovered_data = model.decode("deepfake.avi")
print(next(recovered_data))