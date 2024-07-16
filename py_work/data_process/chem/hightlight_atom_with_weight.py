from typing import List

from IPython.display import SVG
from matplotlib.colors import LinearSegmentedColormap
from numpy.typing import ArrayLike
from rdkit import Chem
from rdkit.Chem import AllChem, Draw
from rdkit.Chem.Draw import SimilarityMaps
from sklearn.preprocessing import MinMaxScaler


def create_custom_colormap(colors: List[str]) -> LinearSegmentedColormap:
    """
    Create a custom LinearSegmentedColormap with evenly spaced colors.
    Args:
        colors (List[str]): A list of color strings.
    Returns:
        LinearSegmentedColormap: The resulting colormap.
    """
    # Ensure the colors list is not empty
    if not colors:
        raise ValueError("The list of colors is empty.")

    # Calculate evenly spaced positions for each color
    n = len(colors)
    positions = np.linspace(0, 1, n)

    # Pair each color with its calculated position
    color_positions = list(zip(positions, colors))

    # Create the custom colormap
    return LinearSegmentedColormap.from_list("custom_colormap", color_positions)


def gaussian_mol_with_weight(mol, weights: ArrayLike, custom_colors, ratio=1.0, figure_size=None):
    if figure_size is None:
        figure_size = [400, 400]

    def _adjust_svg(svg_words):
        """
        """
        svg_words = svg_words.replace(
            'stroke-width:2px', 'stroke-width:1.5px').replace(
            'font-size:17px', 'font-size:15px').replace(
            'stroke-linecap:butt', 'stroke-linecap:square').replace(
            'fill:#FFFFFF', 'fill:none').replace(
            'svg:', '')
        return svg_words

    drawer = Draw.MolDraw2DSVG(*figure_size)
    # drawer = Draw.MolDraw2DCairo(400, 400)
    drawer.drawOptions().clearBackground = True
    drawer.drawOptions().addAtomIndices = True
    drawer.ClearDrawing()

    AllChem.ComputeGasteigerCharges(mol)

    scaler = MinMaxScaler(feature_range=(0, 1))
    weights = scaler.fit_transform(weights.reshape(-1, 1)).flatten()

    indecies = np.argsort(weights)
    n = np.ceil(indecies.shape[0] * (1 - ratio))
    weights[indecies[: int(n)]] = -1

    custom_colormap = create_custom_colormap(custom_colors)
    SimilarityMaps.GetSimilarityMapFromWeights(mol, list(weights), colorMap=custom_colormap, contourLines=0,
                                               draw2d=drawer)
    drawer.FinishDrawing()

    svg = drawer.GetDrawingText()
    return SVG(_adjust_svg(svg))


if __name__ == "__main__":
    import numpy as np

    m = Chem.MolFromSmiles('COc1cccc2cc(C(=O)NCCCCN3CCN(c4cccc5nccnc54)CC3)oc21')
    contribs = np.random.randn(len(m.GetAtoms()))  # fake data
    colors = ["limegreen", "white", "orange"]

    svg_fig = gaussian_mol_with_weight(m, contribs, custom_colors=colors)

    with open('./demo.svg', 'w') as f:
        f.write(svg_fig.data)

    # In jupyter
    # >>> SVG(svg_fig)

    print("DONE")
