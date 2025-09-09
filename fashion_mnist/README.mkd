1. Copy the following code into OTL Python Module:

    import sys

    sys.path.append(r"path\to\fashion_mnist")
    import hou_fashionMNIST as hfm
    import importlib
    importlib.reload(hfm)

    def execute():
        hfm.get_pred()

2. Copy the following into button callback:
    hou.phm().execute()

3. Point model path to fashion_mnist_model.pth file