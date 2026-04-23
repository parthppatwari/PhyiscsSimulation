import numpy as np
import matplotlib.pyplot as plt

def present(binary_array):

    image = (binary_array * 255).astype(np.uint8)

    rows, cols = binary_array.shape

    plt.imshow(image, cmap='gray', vmin=0, vmax=255)

    # Add coordinates on each pixel
    for i in range(rows):
        for j in range(cols):
            plt.text(j, i, f'({i},{j})',
                     ha='center', va='center',
                     color='red', fontsize=8)

    plt.title("Binary Image with Coordinates")
    plt.axis('off')
    plt.show()

def random_binary_array(rows, cols):
    return np.random.randint(0, 2, size=(rows, cols))



height, width = 10 , 15
#bin_array = np.ones([height,width],dtype=int)
bin_array = random_binary_array(10,15)
bin_array[2][2] = 0

present(bin_array)