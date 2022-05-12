import matplotlib.pyplot as plt 
from rivagan import RivaGAN

model = RivaGAN()

# history = RivaGAN.load("data/model.pt")
import csv

tsv_file = open("data/metrics.tsv")
read_tsv = csv.reader(tsv_file, delimiter="\t")
train_acc=[]
val_acc=[]
for i,row in enumerate(read_tsv):
    if(i==0):continue
    # train_acc.append(row[2])
    # val_acc.append(row[8])
    train_acc.append(row[0])
    val_acc.append(row[3])
#

tsv_file. close()

# loss_train = history.history['acc']
# loss_val = history.history['val_acc']
epochs = range(1,126)
print(train_acc)
print(val_acc)
print(epochs)
plt.plot(epochs, train_acc, 'g', label='Training accuracy')
# plt.plot(epochs, val_acc, 'b', label='validation accuracy')
plt.title('Training and Validation accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.show()