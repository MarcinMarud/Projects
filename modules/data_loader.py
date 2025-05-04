import pandas as pd
from tkinter import filedialog, messagebox


def load_data_from_file():
    """Opens a file dialog for the user to select a CSV or Excel file.

    Returns:
        pandas.DataFrame or None: The loaded DataFrame if successful, None otherwise.
    """
    file_path = filedialog.askopenfilename(
        title="Select Data File",
        filetypes=(("CSV files", "*.csv"), ("Excel files", "*.xlsx *.xls"))
    )
    if file_path:
        try:
            if file_path.endswith(('.csv')):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)
            return df
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found.")
            return None
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            return None
    return None


if __name__ == '__main__':
    # Example usage if you run this file directly
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    data = load_data_from_file()
    if data is not None:
        print("Data loaded successfully:")
        print(data.head())
