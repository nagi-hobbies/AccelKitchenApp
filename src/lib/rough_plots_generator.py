import matplotlib.pyplot as plt
import matplotlib_fontja
import numpy as np
import pandas as pd
import seaborn as sns


class RoughPlotsGenerator:
    def __init__(self, df: pd.DataFrame):
        sns.set_theme()
        matplotlib_fontja.japanize()
        self.df = df

    def plot_histgram(
        self,
        df: pd.DataFrame,
        column: str,
        figsize: tuple = (5, 4),
        bins: int = 100,
        title: str = None,
        x_label: str = None,
        y_label: str = None,
        x_lim: tuple = None,
        y_lim: tuple = None,
    ) -> plt.figure:
        """
        ヒストグラムを返します

        Args:
            df (pd.DataFrame): データフレーム
            column (str): ヒストグラムを作成する列
            figsize (tuple, optional): プロットのサイズ. Defaults to (5,5).
            bins (int, optional): ビンの数. Defaults to 100.
            title (str, optional): タイトル. Defaults to None.
            x_label (str, optional): x軸のラベル. Defaults to None.
            y_label (str, optional): y軸のラベル. Defaults to None.
            x_lim (tuple, optional): x軸の範囲. Defaults to None.
            y_lim (tuple, optional): y軸の範囲. Defaults to None.

        Returns:
            plt.figure: ヒストグラム
        """
        fig = plt.figure(figsize=figsize)
        data = df[column].dropna()
        counts, bin_edges = np.histogram(data, bins=bins, range=x_lim)
        # plt.hist(bin_edges[:-1], bin_edges, weights=counts)
        plt.bar(bin_edges[:-1], counts, width=np.diff(bin_edges), align="edge")
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.ylim(y_lim)
        return fig
