import torch
from torch import nn
import numpy as np
from torch.nn import functional
import torchvision.models as models

def multiplicative(x, data):
    """
    This function takes a 5d tensor (with the same shape and dimension order
    as the input to Conv3d) and a 2d data tensor. For each element in the
    batch, the data vector is combined with the first D dimensions of the 5d
    tensor through an elementwise product.

    Input: (N, C_{in}, L, H, W), (N, D)
    Output: (N, C_{in}, L, H, W)
    """
    N, D = data.size()
    N, C, L, H, W = x.size()
    assert D <= C, "data dims must be less than channel dims"
    x = torch.cat([
        x[:, :D, :, :, :] * data.view(N, D, 1, 1, 1).expand(N, D, L, H, W),
        x[:, D:, :, :, :]
    ], dim=1)
    return x


class AttentiveEncoder(nn.Module):
    """
    Input: (N, 3, L, H, W), (N, D, )
    Output: (N, 3, L, H, W)
    """

    def __init__(self, data_dim, tie_rgb=False, linf_max=0.016,
                 kernel_size=(1, 11, 11), padding=(0, 5, 5)):
        super(AttentiveEncoder, self).__init__()

        self.linf_max = linf_max
        self.data_dim = data_dim
        self.kernel_size = kernel_size
        self.padding = padding
        # 
        self.net = models.video.r3d_18(pretrained=True)
        # If you treat GooLeNet as a fixed feature extractor, disable the gradients and save some memory
        for p in self.net.parameters():
            p.requires_grad = False
        # Define which layers you are going to extract
        self._attention = nn.Sequential(*list(self.net.children())[:4])
        # self._attention = nn.Sequential(
        #     nn.Conv3d(3, 32, kernel_size=kernel_size, padding=padding),
        #     nn.Tanh(),
        #     nn.BatchNorm3d(32),
        #     nn.Conv3d(32, data_dim, kernel_size=kernel_size, padding=padding),
        #     nn.Tanh(),
        #     nn.BatchNorm3d(data_dim),
        # )
        self._conv = nn.Sequential(
            nn.Conv3d(4, 32, kernel_size=kernel_size, padding=padding),
            nn.Tanh(),
            nn.BatchNorm3d(32),
            nn.Conv3d(32, 1 if tie_rgb else 3, kernel_size=kernel_size, padding=padding),
            nn.Tanh(),
        )
        # self._conv=nn.Sequential(*list(self.net.children())[:4])

    def forward(self, frames, data):
        data = data * 2.0 - 1.0
        x = functional.softmax(self._attention(frames), dim=1)
        x = torch.sum(multiplicative(x, data), dim=1, keepdim=True)
      
        x.resize_(64, 1, 1,4,4)
        frames.resize_(64, 3,1, 4,4)
        # print(frames.shape,x.shape)
        # exit()
        x = self._conv(torch.cat([frames,x], dim=1))
    #  [batch_size=4, channels=16, height=37, width=37]
        # x = self._conv(x)
        
        # x = x.view(x.size(0), 3*3*3)
        # frames = frames.view(22.3, 3*3*3)
        # frames.resize_(64,3,1,64,27)
        # torch.reshape(x,(32,  3))
        # print(x.shape,frames.shape)
        # exit()
        # x.resize_(32,  3, 1, 3, 3)
        return frames + self.linf_max * x


class AttentiveDecoder(nn.Module):
    """
    Input: (N, 3, L, H, W)
    Output: (N, D)
    """

    def __init__(self, encoder):
        super(AttentiveDecoder, self).__init__()
        self.data_dim = encoder.data_dim
        self._attention = encoder._attention
       
        # self._conv=encoder._conv
        self._conv = nn.Sequential(
            nn.Conv3d(4, 32, kernel_size=encoder.kernel_size, padding=encoder.padding, stride=1),
            nn.Tanh(),
            nn.BatchNorm3d(32),
            nn.Conv3d(32, self.data_dim, kernel_size=encoder.kernel_size,
                      padding=encoder.padding, stride=1),
        )

    def forward(self, frames):
        N, D, L, H, W = frames.size()
        # frames = frames.view(frames.size(0), 4)
        # print(frames.shape)
        # exit()
        attention = functional.softmax(self._attention(frames), dim=3)
        # print(attention.shape)
        # exit()
        # frames= torch.reshape(frames,(16, 3, 27, 64, 4))
        # attention= torch.reshape(attention,(16, 32, 4, 64, 4))
        
        # torch.Size([64, 256, 1, 8, 4]) torch.Size([64, 3, 1, 64, 27])
        # print(attention.shape,frames.shape)
        # exit()
        # torch.reshape(frames,())
        # 3538944
        # x = self._conv(frames) * attention
        return torch.mean(attention.view(N, self.data_dim, -1), dim=2)
