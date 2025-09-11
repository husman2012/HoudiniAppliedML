
from PIL import Image
import matplotlib.pyplot as plt
import torch
from torchvision import transforms
from transformers import AutoModelForImageSegmentation

# Load the pre-trained image segmentation model from Hugging Face
model = AutoModelForImageSegmentation.from_pretrained("briaai/RMBG-2.0", trust_remote_code=True)

# Set the precision for matrix multiplication to high for better performance
torch.set_float32_matmul_precision(['high', 'highest'][0])

# Move the model to GPU for faster computation
model.to('cuda')

# Set the model to evaluation mode (disables training-specific layers like dropout)
model.eval()

# Data settings
# Define the target image size and transformation pipeline
image_size = (1024, 1024)
transform_image = transforms.Compose([
    transforms.Resize(image_size),  # Resize the image to the target size
    transforms.ToTensor(),  # Convert the image to a PyTorch tensor
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])  # Normalize the image
])

# Load the input image
input_image_path = "input_img.jpg"
image = Image.open(input_image_path)

# Apply the transformations and add a batch dimension, then move to GPU
input_images = transform_image(image).unsqueeze(0).to('cuda')

# Prediction
with torch.no_grad():  # Disable gradient computation for inference
    preds = model(input_images)[-1].sigmoid().cpu()  # Get the model's predictions and apply sigmoid activation

# Extract the first prediction and remove the batch dimension
pred = preds[0].squeeze()

# Convert the prediction tensor to a PIL image
pred_pil = transforms.ToPILImage()(pred)

# Resize the mask to match the original image size
mask = pred_pil.resize(image.size)

# Add the mask as an alpha channel to the original image
image.putalpha(mask)

# Save the resulting image with the background removed
image.save("no_bg_image.png")