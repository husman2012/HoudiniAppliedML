import hou
import numpy as np
import math

from PIL import Image
import torch
import torchvision.transforms as transforms

IMAGE_SIZE = 28
CLASS_NAMES = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

def convert_grid_to_array(prims):
    """
    Converts a grid of Houdini primitives to a 2D array of grayscale values.

    Arguments:
        prims (list[hou.Prim]): List of Houdini primitive objects.

    Returns:
        grid_matrix (list[list[float]]): 2D array representing grayscale values of the grid.
    """
    num_rows = num_cols = int(math.sqrt(len(prims)))
    grid_matrix = []
    geo = prims[0].geometry() if prims else None
    if not geo:
        return grid_matrix
    for row in range(num_rows):
        new_row = []
        for col in range(num_cols):
            idx = row * num_cols + col
            prim = geo.prim(idx)
            # Extract the first channel of the color attribute (assumed grayscale)
            color = prim.attribValue("Cd")[0]
            new_row.append(color)
        grid_matrix.append(new_row)
    return grid_matrix

def matrix_to_tensor(matrix):
    """
    Converts a 2D matrix of grayscale values to a PyTorch tensor suitable for model input.

    Arguments:
        matrix (list[list[float]]): 2D array of grayscale values.

    Returns:
        tensor (torch.Tensor): Tensor of shape (1, IMAGE_SIZE, IMAGE_SIZE).
    """
    # Convert matrix to uint8 and scale to 0-255
    array = np.array(matrix, dtype=np.uint8) * 255
    img = Image.fromarray(array, 'L').resize((IMAGE_SIZE, IMAGE_SIZE))
    transform = transforms.Compose(
        [
            transforms.ToTensor()
        ]
    )
    tensor = transform(img)
    return tensor

def run_model(input_tensor, model_path=None):
    """
    Loads a TorchScript model and runs inference on the input tensor.

    Arguments:
        input_tensor (torch.Tensor): Input tensor for the model.
        model_path (str, optional): Path to the TorchScript model file.

    Returns:
        predicted (str or None): Predicted class name, or None if model path is not specified.
    """
    if model_path is None:
        hou.ui.displayMessage("Model path not specified.")
        return None
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    input_tensor = input_tensor.to(device).float()
    model = torch.jit.load(model_path)
    model.eval()

    with torch.no_grad():
        pred = model(input_tensor)
        # Get the predicted class name
        predicted = CLASS_NAMES[pred[0].argmax(0).item()]
        return predicted

def get_pred():
    """
    Houdini callback function to run the FashionMNIST model on the current node's geometry.

    Arguments:
        None

    Returns:
        None
    """
    # Get the current Houdini node and its geometry
    node = hou.pwd()
    geo = node.geometry()
    prims = geo.prims()
    model_path = node.parm("model_path").eval()

    if not prims:
        hou.ui.displayMessage("No geometry found. Please provide a geometry with a mask.")
        return

    # Convert geometry to input tensor and run model
    grid_matrix = convert_grid_to_array(prims)
    input_tensor = matrix_to_tensor(grid_matrix)
    prediction = run_model(input_tensor, model_path)
    print("Predicted Class:", prediction)