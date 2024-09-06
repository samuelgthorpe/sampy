"""Basic tests of the vscode chatgpt extension."""


def filter_files(path: str, tag: str) -> list:
    """Return list of files present at input path with file names matching tag.

    Note: return a list files with filenames which match the tag. In the
          returned list, the filenames are joined with the input path such
          that each list entry contains the full path to the file.

    Args:
        path (str): path containing files
        tag (str): extension or regex pattern which must be present in file
                   name in order to be retirned

    Returns:
        list: kist of files matching tag pattern
    """
    import os
    import re

    files = [os.path.join(path, f) for f in os.listdir(path)
             if re.search(tag, f)]

    return files


def visualize_matrix(M):
    """Given input matrix M, visualize as a heat map using matplotlib.

    Args:
        M (_type_): np.array
    """
    import matplotlib.pyplot as plt
    import numpy as np

    plt.imshow(M, cmap='hot', interpolation='nearest')
    plt.colorbar()
    plt.show()


def plot_spectrum(dfr: pd.DataFrame):
    """Plot power spectrum associates with input time series of measurements.

    Given the input dataframe, first compute power spectrum from timestamps and
    measurements columns using Welch's method. Then visualize the power spectrum
    via an interactive html plot using the plotly library.

    Args:
        dfr (pd.DataFrame): must contain a column with "timestamps" as well
            as a second column with "measurements".
    """
    import pandas as pd
    import plotly.express as px
    from scipy.signal import welch

    frequencies, power_spectrum = welch(
        dfr['measurements'],
        fs=1/(dfr['timestamps'][1] - dfr['timestamps'][0])
        )
    fig = px.line(x=frequencies, y=power_spectrum, title='Power Spectrum')
    fig.update_xaxes(title_text='Frequency (Hz)')
    fig.update_yaxes(title_text='Power')
    fig.show()


