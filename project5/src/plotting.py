import matplotlib.pyplot as plt

def show_2d(v):
    plt.imshow(v, cmap=plt.cm.gray, vmin=0, vmax=1, interpolation='none')
    plt.show()
