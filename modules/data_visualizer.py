import matplotlib.pyplot as plt
import seaborn as sns


def create_histogram(df, column, title='Histogram', bins=10, color=None):
    """
    Creates a histogram for a numerical column.

    Args:
        df (pd.DataFrame): The DataFrame.
        column (str): The column to plot.
        title (str, optional): The plot title. Defaults to 'Histogram'.
        bins (int, optional): Number of histogram bins. Defaults to 10.
        color: Color of the bars.
    """
    plt.figure(figsize=(8, 6))
    sns.histplot(df[column], bins=bins, kde=True, color=color)
    plt.title(title)
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.show()


def create_scatter_plot(df, x_col, y_col, title='Scatter Plot', color=None,
                        xlabel=None, ylabel=None):
    """
    Creates a scatter plot.

    Args:
        df (pd.DataFrame): The DataFrame.
        x_col (str): Column for the x-axis.
        y_col (str): Column for the y-axis.
        title (str, optional): The plot title. Defaults to 'Scatter Plot'.
        color: Color of the points.
        xlabel: Label for x-axis.
        ylabel: Label for y-axis.
    """

    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=x_col, y=y_col, data=df, color=color)
    plt.title(title)
    plt.xlabel(xlabel or x_col)  # Use xlabel if provided, else use column name
    plt.ylabel(ylabel or y_col)  # Use ylabel if provided, else use column name
    plt.show()


def create_bar_chart(df, x_col, y_col, title='Bar Chart', color=None,
                     xlabel=None, ylabel=None):
    """
    Creates a bar chart.

    Args:
        df (pd.DataFrame): The DataFrame.
        x_col (str): Column for the x-axis (categorical).
        y_col (str): Column for the y-axis (numerical).
        title (str, optional): The plot title. Defaults to 'Bar Chart'.
        color: Color of the bars.
        xlabel: Label for x-axis.
        ylabel: Label for y-axis.
    """
    plt.figure(figsize=(8, 6))
    sns.barplot(x=x_col, y=y_col, data=df, color=color)
    plt.title(title)
    plt.xlabel(xlabel or x_col)
    plt.ylabel(ylabel or y_col)
    plt.show()


def create_box_plot(df, x_col, y_col, title='Box Plot', color=None,
                    xlabel=None, ylabel=None):
    """
    Creates a box plot.

    Args:
        df (pd.DataFrame): The DataFrame.
        x_col (str): Column for the x-axis (categorical).
        y_col (str): Column for the y-axis (numerical).
        title (str, optional): The plot title. Defaults to 'Box Plot'.
        color: Color of the boxes.
        xlabel: Label for x-axis.
        ylabel: Label for y-axis.
    """

    plt.figure(figsize=(8, 6))
    sns.boxplot(x=x_col, y=y_col, data=df, color=color)
    plt.title(title)
    plt.xlabel(xlabel or x_col)
    plt.ylabel(ylabel or y_col)
    plt.show()
