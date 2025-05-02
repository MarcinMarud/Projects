import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import os
import sys

# Import our custom modules
from modules.data_loader import load_data_from_file
from modules.data_cleaner import clean_missing_values, remove_duplicates, filter_data
from modules.data_analyzer import get_descriptive_stats, calculate_correlations, group_and_aggregate
from modules.data_visualizer import create_histogram, create_scatter_plot, create_bar_chart, create_box_plot


class DataAnalysisApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Data Analysis Dashboard")
        self.geometry("1200x800")
        self.df = None
        self.cleaned_df = None

        # Set up the tab control
        self.tab_control = ttk.Notebook(self)

        # Create tabs
        self.load_tab = ttk.Frame(self.tab_control)
        self.cleanse_tab = ttk.Frame(self.tab_control)
        self.analysis_tab = ttk.Frame(self.tab_control)
        self.visualization_tab = ttk.Frame(self.tab_control)
        self.dashboard_tab = ttk.Frame(self.tab_control)

        # Add tabs to the notebook
        self.tab_control.add(self.load_tab, text="Load Data")
        self.tab_control.add(self.cleanse_tab, text="Cleanse Data")
        self.tab_control.add(self.analysis_tab, text="Analysis")
        self.tab_control.add(self.visualization_tab, text="Visualization")
        self.tab_control.add(self.dashboard_tab, text="Dashboard")

        self.tab_control.pack(expand=1, fill="both")

        # Setup each tab
        self.setup_load_tab()
        self.setup_cleanse_tab()
        self.setup_analysis_tab()
        self.setup_visualization_tab()
        self.setup_dashboard_tab()

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(
            self, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def setup_load_tab(self):
        # Load tab layout
        frame = ttk.LabelFrame(self.load_tab, text="Load Data")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Button(frame, text="Load CSV/Excel File",
                   command=self.load_file).pack(pady=20)

        # Data preview frame
        preview_frame = ttk.LabelFrame(frame, text="Data Preview")
        preview_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Treeview for data preview
        self.preview_tree = ttk.Treeview(preview_frame)
        self.preview_tree.pack(fill="both", expand=True, side=tk.LEFT)

        # Scrollbars for the treeview
        vsb = ttk.Scrollbar(preview_frame, orient="vertical",
                            command=self.preview_tree.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.preview_tree.configure(yscrollcommand=vsb.set)

        hsb = ttk.Scrollbar(self.load_tab, orient="horizontal",
                            command=self.preview_tree.xview)
        hsb.pack(fill=tk.X)
        self.preview_tree.configure(xscrollcommand=hsb.set)

        # Data info frame
        info_frame = ttk.LabelFrame(frame, text="Data Information")
        info_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.info_text = tk.Text(info_frame, height=10)
        self.info_text.pack(fill="both", expand=True)

    def setup_cleanse_tab(self):
        # Cleanse tab layout
        frame = ttk.LabelFrame(self.cleanse_tab, text="Data Cleansing")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Missing values handling
        missing_frame = ttk.LabelFrame(frame, text="Handle Missing Values")
        missing_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Label(missing_frame, text="Method:").grid(
            row=0, column=0, padx=5, pady=5)
        self.missing_method = ttk.Combobox(
            missing_frame, values=["drop", "mean", "median", "ffill", "bfill", "constant"])
        self.missing_method.current(0)
        self.missing_method.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(missing_frame, text="Fill Value (for constant):").grid(
            row=1, column=0, padx=5, pady=5)
        self.fill_value = ttk.Entry(missing_frame)
        self.fill_value.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(missing_frame, text="Apply", command=self.handle_missing_values).grid(
            row=2, column=0, columnspan=2, pady=10)

        # Duplicates handling
        dup_frame = ttk.LabelFrame(frame, text="Remove Duplicates")
        dup_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Label(dup_frame, text="Keep:").grid(
            row=0, column=0, padx=5, pady=5)
        self.dup_keep = ttk.Combobox(
            dup_frame, values=["first", "last", "False"])
        self.dup_keep.current(0)
        self.dup_keep.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(dup_frame, text="Consider Columns (comma-separated):").grid(row=1,
                                                                              column=0, padx=5, pady=5)
        self.dup_subset = ttk.Entry(dup_frame)
        self.dup_subset.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(dup_frame, text="Apply", command=self.remove_dups).grid(
            row=2, column=0, columnspan=2, pady=10)

        # Filter data
        filter_frame = ttk.LabelFrame(frame, text="Filter Data")
        filter_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Label(filter_frame, text="Column:").grid(
            row=0, column=0, padx=5, pady=5)
        self.filter_column = ttk.Combobox(filter_frame)
        self.filter_column.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(filter_frame, text="Condition:").grid(
            row=1, column=0, padx=5, pady=5)
        self.filter_condition = ttk.Combobox(
            filter_frame, values=["==", "!=", ">", "<", ">=", "<=", "in", "not in"])
        self.filter_condition.current(0)
        self.filter_condition.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(filter_frame, text="Value:").grid(
            row=2, column=0, padx=5, pady=5)
        self.filter_value = ttk.Entry(filter_frame)
        self.filter_value.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(filter_frame, text="Apply", command=self.filter_dataframe).grid(
            row=3, column=0, columnspan=2, pady=10)

        # Cleansed data preview
        preview_frame = ttk.LabelFrame(frame, text="Cleansed Data Preview")
        preview_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Treeview for cleansed data preview
        self.cleansed_preview_tree = ttk.Treeview(preview_frame)
        self.cleansed_preview_tree.pack(fill="both", expand=True, side=tk.LEFT)

        # Scrollbars for the treeview
        vsb = ttk.Scrollbar(preview_frame, orient="vertical",
                            command=self.cleansed_preview_tree.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.cleansed_preview_tree.configure(yscrollcommand=vsb.set)

        # Save cleansed data button
        ttk.Button(frame, text="Save Cleansed Data",
                   command=self.save_cleansed_data).pack(pady=10)

    def setup_analysis_tab(self):
        # Analysis tab layout
        frame = ttk.LabelFrame(self.analysis_tab, text="Data Analysis")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Descriptive statistics
        stats_frame = ttk.LabelFrame(frame, text="Descriptive Statistics")
        stats_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Label(stats_frame, text="Include:").grid(
            row=0, column=0, padx=5, pady=5)
        self.stats_include = ttk.Combobox(
            stats_frame, values=["all", "numeric", "object"])
        self.stats_include.current(0)
        self.stats_include.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(stats_frame, text="Generate", command=self.show_descriptive_stats).grid(
            row=1, column=0, columnspan=2, pady=10)

        # Statistics result
        self.stats_result = tk.Text(stats_frame, height=10)
        self.stats_result.grid(row=2, column=0, columnspan=2,
                               padx=5, pady=5, sticky="nsew")

        # Correlation analysis
        corr_frame = ttk.LabelFrame(frame, text="Correlation Analysis")
        corr_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Label(corr_frame, text="Method:").grid(
            row=0, column=0, padx=5, pady=5)
        self.corr_method = ttk.Combobox(
            corr_frame, values=["pearson", "kendall", "spearman"])
        self.corr_method.current(0)
        self.corr_method.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(corr_frame, text="Generate", command=self.show_correlations).grid(
            row=1, column=0, columnspan=2, pady=10)

        # Correlation result
        self.corr_result = tk.Text(corr_frame, height=10)
        self.corr_result.grid(row=2, column=0, columnspan=2,
                              padx=5, pady=5, sticky="nsew")

        # Group and aggregate
        agg_frame = ttk.LabelFrame(frame, text="Group and Aggregate")
        agg_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Label(agg_frame, text="Group By (comma-separated):").grid(row=0,
                                                                      column=0, padx=5, pady=5)
        self.group_cols = ttk.Entry(agg_frame)
        self.group_cols.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(agg_frame, text="Aggregate (col:func, e.g., sales:sum,profit:mean):").grid(
            row=1, column=0, padx=5, pady=5)
        self.agg_funcs = ttk.Entry(agg_frame)
        self.agg_funcs.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(agg_frame, text="Generate", command=self.show_aggregation).grid(
            row=2, column=0, columnspan=2, pady=10)

        # Aggregation result
        self.agg_result = tk.Text(agg_frame, height=10)
        self.agg_result.grid(row=3, column=0, columnspan=2,
                             padx=5, pady=5, sticky="nsew")

    def setup_visualization_tab(self):
        # Visualization tab layout
        frame = ttk.LabelFrame(self.visualization_tab,
                               text="Data Visualization")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        controls_frame = ttk.Frame(frame)
        controls_frame.pack(side=tk.LEFT, fill="y", padx=10, pady=10)

        # Chart type selection
        ttk.Label(controls_frame, text="Chart Type:").pack(anchor="w", pady=5)
        self.chart_type = ttk.Combobox(controls_frame, values=[
                                       "Histogram", "Scatter Plot", "Bar Chart", "Box Plot"])
        self.chart_type.current(0)
        self.chart_type.pack(fill="x", pady=5)
        self.chart_type.bind("<<ComboboxSelected>>", self.update_chart_options)

        # Column selections for various chart types
        self.column_frame = ttk.Frame(controls_frame)
        self.column_frame.pack(fill="x", pady=5)

        # Add plot button
        ttk.Button(controls_frame, text="Create Plot",
                   command=self.create_plot).pack(fill="x", pady=10)

        # Save plot button
        ttk.Button(controls_frame, text="Save Plot",
                   command=self.save_plot).pack(fill="x", pady=5)

        # Plot frame where the visualizations will appear
        self.plot_frame = ttk.Frame(frame)
        self.plot_frame.pack(side=tk.RIGHT, fill="both",
                             expand=True, padx=10, pady=10)

        # Initial setup of column selectors
        self.update_chart_options(None)

    def setup_dashboard_tab(self):
        # Dashboard tab layout
        frame = ttk.LabelFrame(self.dashboard_tab, text="Data Dashboard")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        controls_frame = ttk.Frame(frame)
        controls_frame.pack(side=tk.LEFT, fill="y", padx=10, pady=10)

        ttk.Label(controls_frame, text="Select Charts for Dashboard").pack(
            anchor="w", pady=5)

        # Chart selection checkboxes
        self.dashboard_options = {
            "stats": tk.BooleanVar(value=True),
            "histogram": tk.BooleanVar(value=True),
            "scatter": tk.BooleanVar(value=True),
            "bar": tk.BooleanVar(value=False),
            "box": tk.BooleanVar(value=False),
            "correlation": tk.BooleanVar(value=True)
        }

        ttk.Checkbutton(controls_frame, text="Descriptive Statistics",
                        variable=self.dashboard_options["stats"]).pack(anchor="w")
        ttk.Checkbutton(controls_frame, text="Histogram",
                        variable=self.dashboard_options["histogram"]).pack(anchor="w")
        ttk.Checkbutton(controls_frame, text="Scatter Plot",
                        variable=self.dashboard_options["scatter"]).pack(anchor="w")
        ttk.Checkbutton(controls_frame, text="Bar Chart",
                        variable=self.dashboard_options["bar"]).pack(anchor="w")
        ttk.Checkbutton(controls_frame, text="Box Plot",
                        variable=self.dashboard_options["box"]).pack(anchor="w")
        ttk.Checkbutton(controls_frame, text="Correlation Heatmap",
                        variable=self.dashboard_options["correlation"]).pack(anchor="w")

        # Dashboard settings
        ttk.Label(controls_frame, text="Dashboard Title:").pack(
            anchor="w", pady=5)
        self.dashboard_title = ttk.Entry(controls_frame)
        self.dashboard_title.insert(0, "Data Analysis Dashboard")
        self.dashboard_title.pack(fill="x", pady=2)

        # Generate dashboard button
        ttk.Button(controls_frame, text="Generate Dashboard",
                   command=self.generate_dashboard).pack(fill="x", pady=10)

        # Save dashboard button
        ttk.Button(controls_frame, text="Save Dashboard",
                   command=self.save_dashboard).pack(fill="x", pady=5)

        # Dashboard canvas
        self.dashboard_canvas_frame = ttk.Frame(frame)
        self.dashboard_canvas_frame.pack(
            side=tk.RIGHT, fill="both", expand=True, padx=10, pady=10)

    # Load tab functions
    def load_file(self):
        self.df = load_data_from_file()
        if self.df is not None:
            self.cleaned_df = self.df.copy()  # Initialize cleaned_df with the original data
            self.status_var.set(
                f"Data loaded: {self.df.shape[0]} rows, {self.df.shape[1]} columns")
            self.update_data_preview()
            self.update_data_info()
            self.update_column_dropdowns()
            messagebox.showinfo("Success", "Data loaded successfully!")
        else:
            self.status_var.set("Data loading canceled or failed")

    def update_data_preview(self):
        # Clear existing data
        for item in self.preview_tree.get_children():
            self.preview_tree.delete(item)

        if self.df is None:
            return

        # Configure columns
        self.preview_tree["columns"] = list(self.df.columns)
        self.preview_tree["show"] = "headings"

        for col in self.df.columns:
            self.preview_tree.heading(col, text=col)
            self.preview_tree.column(col, width=100)

        # Add data rows (limit to first 100 rows for performance)
        for i, row in self.df.head(100).iterrows():
            values = row.tolist()
            # Convert any non-string values to strings
            values = [str(v) if v is not None else "" for v in values]
            self.preview_tree.insert("", "end", values=values)

    def update_data_info(self):
        if self.df is None:
            return

        # Clear existing info
        self.info_text.delete(1.0, tk.END)

        # Add general info
        info = f"Rows: {self.df.shape[0]}\n"
        info += f"Columns: {self.df.shape[1]}\n\n"

        # Add column info
        info += "Column Information:\n"
        for col in self.df.columns:
            dtype = self.df[col].dtype
            missing = self.df[col].isna().sum()
            pct_missing = (missing / len(self.df)) * 100
            info += f"- {col}: {dtype}, Missing: {missing} ({pct_missing:.2f}%)\n"

        self.info_text.insert(tk.END, info)

    def update_column_dropdowns(self):
        if self.df is None:
            return

        # Update all dropdown menus with the current column names
        columns = list(self.df.columns)

        # Update filter column dropdown
        self.filter_column['values'] = columns
        if columns:
            self.filter_column.current(0)

        # Clear and update visualization tab options
        self.update_chart_options(None)

    # Cleanse tab functions
    def handle_missing_values(self):
        if self.cleaned_df is None:
            messagebox.showerror("Error", "No data loaded")
            return

        method = self.missing_method.get()
        fill_value = None

        if method == "constant":
            try:
                value_str = self.fill_value.get()
                # Try to convert to numeric if possible
                try:
                    fill_value = float(value_str)
                    if fill_value.is_integer():
                        fill_value = int(fill_value)
                except ValueError:
                    fill_value = value_str  # Keep as string if not numeric
            except:
                messagebox.showerror("Error", "Invalid fill value")
                return

        try:
            self.cleaned_df = clean_missing_values(
                self.cleaned_df, method=method, fill_value=fill_value)
            self.update_cleansed_preview()
            self.status_var.set(
                f"Missing values handled using method: {method}")
            messagebox.showinfo(
                "Success", "Missing values handled successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def remove_dups(self):
        if self.cleaned_df is None:
            messagebox.showerror("Error", "No data loaded")
            return

        keep = self.dup_keep.get()
        if keep == "False":
            keep = False

        subset_str = self.dup_subset.get()
        subset = None if not subset_str else [
            col.strip() for col in subset_str.split(',')]

        try:
            self.cleaned_df = remove_duplicates(
                self.cleaned_df, subset=subset, keep=keep)
            self.update_cleansed_preview()
            self.status_var.set(
                f"Duplicates removed: {self.df.shape[0] - self.cleaned_df.shape[0]} rows")
            messagebox.showinfo("Success", "Duplicates removed successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def filter_dataframe(self):
        if self.cleaned_df is None:
            messagebox.showerror("Error", "No data loaded")
            return

        column = self.filter_column.get()
        condition = self.filter_condition.get()
        value_str = self.filter_value.get()

        # Process value based on condition
        value = value_str
        if condition in ["in", "not in"]:
            value = [v.strip() for v in value_str.split(',')]
        else:
            # Try to convert to numeric if possible
            try:
                value = float(value_str)
                if value.is_integer():
                    value = int(value)
            except ValueError:
                # Keep as string if not numeric
                pass

        try:
            self.cleaned_df = filter_data(
                self.cleaned_df, column, condition, value)
            self.update_cleansed_preview()
            self.status_var.set(
                f"Data filtered: {self.cleaned_df.shape[0]} rows remaining")
            messagebox.showinfo("Success", "Data filtered successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_cleansed_preview(self):
        # Clear existing data
        for item in self.cleansed_preview_tree.get_children():
            self.cleansed_preview_tree.delete(item)

        if self.cleaned_df is None:
            return

        # Configure columns
        self.cleansed_preview_tree["columns"] = list(self.cleaned_df.columns)
        self.cleansed_preview_tree["show"] = "headings"

        for col in self.cleaned_df.columns:
            self.cleansed_preview_tree.heading(col, text=col)
            self.cleansed_preview_tree.column(col, width=100)

        # Add data rows (limit to first 100 rows for performance)
        for i, row in self.cleaned_df.head(100).iterrows():
            values = row.tolist()
            # Convert any non-string values to strings
            values = [str(v) if v is not None else "" for v in values]
            self.cleansed_preview_tree.insert("", "end", values=values)

    def save_cleansed_data(self):
        if self.cleaned_df is None:
            messagebox.showerror("Error", "No cleansed data to save")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")]
        )

        if file_path:
            try:
                if file_path.endswith('.csv'):
                    self.cleaned_df.to_csv(file_path, index=False)
                else:
                    self.cleaned_df.to_excel(file_path, index=False)
                messagebox.showinfo("Success", f"Data saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save data: {str(e)}")

    # Analysis tab functions
    def show_descriptive_stats(self):
        if self.cleaned_df is None:
            messagebox.showerror("Error", "No data loaded")
            return

        include = self.stats_include.get()
        if include == "numeric":
            include = 'number'
        elif include == "object":
            include = 'object'

        try:
            stats_df = get_descriptive_stats(self.cleaned_df, include=include)

            # Clear previous results
            self.stats_result.delete(1.0, tk.END)

            # Display results
            self.stats_result.insert(tk.END, stats_df.to_string())
            self.status_var.set("Descriptive statistics generated")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_correlations(self):
        if self.cleaned_df is None:
            messagebox.showerror("Error", "No data loaded")
            return

        method = self.corr_method.get()

        try:
            corr_df = calculate_correlations(self.cleaned_df, method=method)

            # Clear previous results
            self.corr_result.delete(1.0, tk.END)

            # Display results
            self.corr_result.insert(tk.END, corr_df.to_string())
            self.status_var.set(
                f"Correlation matrix generated using {method} method")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_aggregation(self):
        if self.cleaned_df is None:
            messagebox.showerror("Error", "No data loaded")
            return

        group_cols_str = self.group_cols.get()
        if not group_cols_str:
            messagebox.showerror("Error", "Group by columns not specified")
            return

        group_cols = [col.strip() for col in group_cols_str.split(',')]

        agg_funcs_str = self.agg_funcs.get()
        if not agg_funcs_str:
            messagebox.showerror(
                "Error", "Aggregation functions not specified")
            return

        # Parse aggregation functions
        agg_dict = {}
        for agg_item in agg_funcs_str.split(','):
            parts = agg_item.split(':')
            if len(parts) != 2:
                messagebox.showerror(
                    "Error", f"Invalid aggregation format: {agg_item}")
                return

            col, func = parts[0].strip(), parts[1].strip()
            agg_dict[col] = func

        try:
            agg_df = group_and_aggregate(self.cleaned_df, group_cols, agg_dict)

            # Clear previous results
            self.agg_result.delete(1.0, tk.END)

            # Display results
            self.agg_result.insert(tk.END, agg_df.to_string())
            self.status_var.set(f"Data aggregated by {group_cols_str}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Visualization tab functions
    def update_chart_options(self, event):
        if self.df is None:
            return

        # Clear existing widgets in column frame
        for widget in self.column_frame.winfo_children():
            widget.destroy()

        chart_type = self.chart_type.get()
        columns = list(self.df.columns)

        if chart_type == "Histogram":
            ttk.Label(self.column_frame, text="Column:").grid(
                row=0, column=0, padx=5, pady=5)
            self.hist_column = ttk.Combobox(self.column_frame, values=columns)
            if columns:
                self.hist_column.current(0)
            self.hist_column.grid(row=0, column=1, padx=5, pady=5)

            ttk.Label(self.column_frame, text="Bins:").grid(
                row=1, column=0, padx=5, pady=5)
            self.hist_bins = ttk.Entry(self.column_frame)
            self.hist_bins.insert(0, "10")
            self.hist_bins.grid(row=1, column=1, padx=5, pady=5)

        elif chart_type == "Scatter Plot":
            ttk.Label(self.column_frame, text="X Column:").grid(
                row=0, column=0, padx=5, pady=5)
            self.scatter_x = ttk.Combobox(self.column_frame, values=columns)
            if columns:
                self.scatter_x.current(0)
            self.scatter_x.grid(row=0, column=1, padx=5, pady=5)

            ttk.Label(self.column_frame, text="Y Column:").grid(
                row=1, column=0, padx=5, pady=5)
            self.scatter_y = ttk.Combobox(self.column_frame, values=columns)
            if len(columns) > 1:
                self.scatter_y.current(1)
            else:
                self.scatter_y.current(0)
            self.scatter_y.grid(row=1, column=1, padx=5, pady=5)

        elif chart_type in ["Bar Chart", "Box Plot"]:
            ttk.Label(self.column_frame, text="X Column (Category):").grid(
                row=0, column=0, padx=5, pady=5)
            self.cat_x = ttk.Combobox(self.column_frame, values=columns)
            if columns:
                self.cat_x.current(0)
            self.cat_x.grid(row=0, column=1, padx=5, pady=5)

            ttk.Label(self.column_frame, text="Y Column (Value):").grid(
                row=1, column=0, padx=5, pady=5)
            self.cat_y = ttk.Combobox(self.column_frame, values=columns)
            if len(columns) > 1:
                self.cat_y.current(1)
            else:
                self.cat_y.current(0)
            self.cat_y.grid(row=1, column=1, padx=5, pady=5)

            if chart_type == "Histogram":
                ttk.Label(self.column_frame, text="Color:").grid(
                    row=2, column=0, padx=5, pady=5)
                self.plot_color = ttk.Combobox(self.column_frame, values=[
                                               "None", "red", "blue", "green", "black"])
                self.plot_color.current(0)
                self.plot_color.grid(row=2, column=1, padx=5, pady=5)
            elif chart_type == "Scatter Plot":
                ttk.Label(self.column_frame, text="Color:").grid(
                    row=2, column=0, padx=5, pady=5)
                self.plot_color = ttk.Combobox(self.column_frame, values=[
                                               "None", "red", "blue", "green", "black"])
                self.plot_color.current(0)
                self.plot_color.grid(row=2, column=1, padx=5, pady=5)
            elif chart_type == "Bar Chart":
                ttk.Label(self.column_frame, text="Color:").grid(
                    row=2, column=0, padx=5, pady=5)
                self.plot_color = ttk.Combobox(self.column_frame, values=[
                                               "None", "red", "blue", "green", "black"])
                self.plot_color.current(0)
                self.plot_color.grid(row=2, column=1, padx=5, pady=5)
            elif chart_type == "Box Plot":
                ttk.Label(self.column_frame, text="Color:").grid(
                    row=2, column=0, padx=5, pady=5)
                self.plot_color = ttk.Combobox(self.column_frame, values=[
                                               "None", "red", "blue", "green", "black"])
                self.plot_color.current(0)
                self.plot_color.grid(row=2, column=1, padx=5, pady=5)

    def create_plot(self):
        if self.df is None:
            messagebox.showerror("Error", "No data loaded")
            return

        chart_type = self.chart_type.get()
        color = self.plot_color.get()
        color = color if color != "None" else None

        # Clear previous plot
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        try:
            if chart_type == "Histogram":
                col = self.hist_column.get()
                bins = int(self.hist_bins.get())
                create_histogram(self.df, column=col, bins=bins, color=color)
            elif chart_type == "Scatter Plot":
                x_col = self.scatter_x.get()
                y_col = self.scatter_y.get()
                create_scatter_plot(self.df, x_col=x_col,
                                    y_col=y_col, color=color)
            elif chart_type == "Bar Chart":
                x_col = self.cat_x.get()
                y_col = self.cat_y.get()
                create_bar_chart(self.df, x_col=x_col,
                                 y_col=y_col, color=color)
            elif chart_type == "Box Plot":
                x_col = self.cat_x.get()
                y_col = self.cat_y.get()
                create_box_plot(self.df, x_col=x_col, y_col=y_col, color=color)

            # Embed the plot in the tkinter window
            figure = plt.gcf()  # Get the current figure
            canvas = FigureCanvasTkAgg(figure, master=self.plot_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

            self.status_var.set(f"{chart_type} created")

        except Exception as e:
            messagebox.showerror("Error", f"Could not create plot: {e}")

    def save_plot(self):
        if not plt.gcf().get_axes():  # Check if a plot exists
            messagebox.showerror("Error", "No plot to save")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("PDF files", "*.pdf")]
        )
        if file_path:
            try:
                plt.gcf().savefig(file_path)
                messagebox.showinfo("Success", f"Plot saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save plot: {str(e)}")

    # Dashboard tab functions
    def generate_dashboard(self):
        if self.cleaned_df is None:
            messagebox.showerror("Error", "No data loaded")
            return

        # Clear previous dashboard
        for widget in self.dashboard_canvas_frame.winfo_children():
            widget.destroy()

        # Create a new figure for the dashboard
        dashboard_fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(16, 24))
        dashboard_fig.suptitle(self.dashboard_title.get(), fontsize=20)

        row, col = 0, 0
        plots_added = 0

        # Add descriptive statistics to the dashboard if selected
        if self.dashboard_options["stats"].get():
            stats_df = get_descriptive_stats(self.cleaned_df)
            stats_text = axes[row, col].text(0.05, 0.95, stats_df.to_string(
            ), transform=axes[row, col].transAxes, fontsize=10, verticalalignment='top')
            axes[row, col].set_title("Descriptive Statistics")
            axes[row, col].axis('off')
            col += 1
            plots_added += 1
            if col > 1:
                col = 0
                row += 1

        # Add histogram to the dashboard if selected
        if self.dashboard_options["histogram"].get() and self.cleaned_df.select_dtypes(include=['number']).columns.any():
            num_col = self.cleaned_df.select_dtypes(
                include=['number']).columns[0]
            sns.histplot(self.cleaned_df[num_col], ax=axes[row, col], kde=True)
            axes[row, col].set_title(f"Histogram of {num_col}")
            axes[row, col].set_xlabel(num_col)
            axes[row, col].set_ylabel("Frequency")
            col += 1
            plots_added += 1
            if col > 1:
                col = 0
                row += 1

        # Add scatter plot to the dashboard if selected
        if self.dashboard_options["scatter"].get() and self.cleaned_df.select_dtypes(include=['number']).columns.any():
            num_cols = self.cleaned_df.select_dtypes(
                include=['number']).columns[:2].tolist()
            if len(num_cols) == 2:
                sns.scatterplot(
                    x=num_cols[0], y=num_cols[1], data=self.cleaned_df, ax=axes[row, col])
                axes[row, col].set_title(
                    f"Scatter Plot of {num_cols[0]} vs {num_cols[1]}")
                axes[row, col].set_xlabel(num_cols[0])
                axes[row, col].set_ylabel(num_cols[1])
                col += 1
                plots_added += 1
                if col > 1:
                    col = 0
                    row += 1

        # Add bar chart to the dashboard if selected
        if self.dashboard_options["bar"].get() and self.cleaned_df.select_dtypes(include=['object']).columns.any() and self.cleaned_df.select_dtypes(include=['number']).columns.any():
            cat_col = self.cleaned_df.select_dtypes(
                include=['object']).columns[0]
            num_col = self.cleaned_df.select_dtypes(
                include=['number']).columns[0]
            sns.barplot(x=cat_col, y=num_col,
                        data=self.cleaned_df, ax=axes[row, col])
            axes[row, col].set_title(f"Bar Chart of {cat_col} by {num_col}")
            axes[row, col].set_xlabel(cat_col)
            axes[row, col].set_ylabel(num_col)
            col += 1
            plots_added += 1
            if col > 1:
                col = 0
                row += 1

        # Add box plot to the dashboard if selected
        if self.dashboard_options["box"].get() and self.cleaned_df.select_dtypes(include=['object']).columns.any() and self.cleaned_df.select_dtypes(include=['number']).columns.any():
            cat_col = self.cleaned_df.select_dtypes(
                include=['object']).columns[0]
            num_col = self.cleaned_df.select_dtypes(
                include=['number']).columns[0]
            sns.boxplot(x=cat_col, y=num_col,
                        data=self.cleaned_df, ax=axes[row, col])
            axes[row, col].set_title(f"Box Plot of {num_col} by {cat_col}")
            axes[row, col].set_xlabel(cat_col)
            axes[row, col].set_ylabel(num_col)
            col += 1
            plots_added += 1
            if col > 1:
                col = 0
                row += 1

        # Add correlation heatmap to the dashboard if selected
        if self.dashboard_options["correlation"].get() and self.cleaned_df.select_dtypes(include=['number']).columns.any():
            corr_matrix = calculate_correlations(self.cleaned_df)
            sns.heatmap(corr_matrix, annot=True,
                        cmap='coolwarm', ax=axes[row, col])
            axes[row, col].set_title("Correlation Heatmap")
            plots_added += 1

        if plots_added == 0:
            axes[0, 0].text(0.5, 0.5, "No plots selected for dashboard",
                            ha='center', va='center', fontsize=12)
            axes[0, 0].axis('off')

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])  # Adjust layout to fit title

        # Embed the dashboard in the tkinter window
        canvas = FigureCanvasTkAgg(
            dashboard_fig, master=self.dashboard_canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.status_var.set("Dashboard generated")

    def save_dashboard(self):
        if not plt.gcf().get_axes():  # Check if a plot exists
            messagebox.showerror("Error", "No dashboard to save")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("PDF files", "*.pdf")]
        )
        if file_path:
            try:
                plt.gcf().savefig(file_path)
                messagebox.showinfo(
                    "Success", f"Dashboard saved to {file_path}")
            except Exception as e:
                messagebox.showerror(
                    "Error", f"Failed to save dashboard: {str(e)}")


if __name__ == "__main__":
    app = DataAnalysisApp()
    app.mainloop()
