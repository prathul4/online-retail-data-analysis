"""Shared matplotlib helpers so every chart in the pipeline looks consistent."""

import matplotlib.pyplot as plt

from src import config


def _save(filename):
    plt.tight_layout()
    plt.savefig(config.PROCESSED_DIR / filename)
    plt.close()


def bar_chart(labels, values, title, xlabel, ylabel, filename,
              horizontal=False, invert=False, rotation=45, figsize=(10, 6)):
    plt.figure(figsize=figsize)
    if horizontal:
        plt.barh(labels, values)
        if invert:
            plt.gca().invert_yaxis()
    else:
        plt.bar(labels, values)
        plt.xticks(rotation=rotation)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    _save(filename)


def line_chart(x, y, title, xlabel, ylabel, filename, rotation=45, figsize=(12, 6)):
    plt.figure(figsize=figsize)
    plt.plot(x, y, marker="o")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=rotation)
    _save(filename)


def multi_line_chart(series_list, title, xlabel, ylabel, filename, rotation=45, figsize=(12, 6)):
    """series_list: list of (x, y, label, style_kwargs) tuples."""
    plt.figure(figsize=figsize)
    for x, y, label, style in series_list:
        plt.plot(x, y, label=label, **style)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=rotation)
    plt.legend()
    _save(filename)


def pie_chart(series, title, filename, figsize=(8, 8)):
    plt.figure(figsize=figsize)
    series.plot(kind="pie", autopct="%1.1f%%")
    plt.title(title)
    plt.ylabel("")
    _save(filename)


def heatmap(matrix, title, xlabel, ylabel, filename, xticklabels, yticklabels,
            cbar_label="", figsize=(14, 8), cmap="YlGnBu"):
    plt.figure(figsize=figsize)
    plt.imshow(matrix, aspect="auto", cmap=cmap)
    plt.colorbar(label=cbar_label)
    plt.xticks(range(len(xticklabels)), xticklabels)
    plt.yticks(range(len(yticklabels)), yticklabels)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    _save(filename)
