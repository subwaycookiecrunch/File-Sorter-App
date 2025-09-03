"""
Modern GUI Components Module
Contains custom GUI components for the File Sorter application with modern design.
"""
import tkinter as tk
from tkinter import ttk
import logging
from typing import Dict, List, Optional

class ModernProgressFrame(ttk.LabelFrame):
    """A modern frame containing a progress bar and percentage label."""
    
    def __init__(self, parent):
        """Initialize the progress frame.
        
        Args:
            parent: The parent widget
        """
        super().__init__(parent, text="📊 Progress", padding="15")
        
        # Create main container
        container = ttk.Frame(self)
        container.pack(fill=tk.X, expand=True)
        
        # Create progress bar with modern styling
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(
            container, 
            orient=tk.HORIZONTAL, 
            length=200, 
            mode='determinate',
            variable=self.progress_var
        )
        self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # Create percentage label with modern styling
        self.percentage_var = tk.StringVar(value="0%")
        percentage_label = ttk.Label(
            container, 
            textvariable=self.percentage_var,
            font=("Segoe UI", 12, "bold")
        )
        percentage_label.pack(side=tk.RIGHT)
        
        # Set initial maximum value
        self.maximum = 100
    
    def set_maximum(self, value: int):
        """Set the maximum value for the progress bar.
        
        Args:
            value: The maximum value
        """
        self.maximum = max(1, value)  # Ensure maximum is at least 1
        self.progress_bar.configure(maximum=self.maximum)
    
    def update_progress(self, value: int):
        """Update the progress bar with a new value.
        
        Args:
            value: The current progress value
        """
        # Update progress variable
        self.progress_var.set(value)
        
        # Calculate and update percentage
        percentage = min(100, int((value / self.maximum) * 100))
        self.percentage_var.set(f"{percentage}%")
        
        # Update the UI
        self.update()
    
    def reset(self):
        """Reset the progress bar to zero."""
        self.progress_var.set(0)
        self.percentage_var.set("0%")
        self.update()


class ModernStatsFrame(ttk.LabelFrame):
    """A modern frame displaying statistics about the file sorting operation."""
    
    def __init__(self, parent):
        """Initialize the statistics frame.
        
        Args:
            parent: The parent widget
        """
        super().__init__(parent, text="📈 Statistics", padding="15")
        
        # Create main container with grid layout
        self.container = ttk.Frame(self)
        self.container.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid columns
        self.container.columnconfigure(0, weight=1)
        self.container.columnconfigure(1, weight=1)
        self.container.columnconfigure(2, weight=1)
        self.container.columnconfigure(3, weight=1)
        
        # Create header row
        header_style = ("Segoe UI", 10, "bold")
        
        # Total files section
        total_frame = ttk.Frame(self.container)
        total_frame.grid(row=0, column=0, columnspan=2, sticky=tk.EW, padx=10, pady=5)
        
        ttk.Label(total_frame, text="📁 Total Files:", font=header_style).pack(side=tk.LEFT)
        self.total_files_var = tk.StringVar(value="0")
        ttk.Label(total_frame, textvariable=self.total_files_var, font=("Segoe UI", 12, "bold")).pack(side=tk.LEFT, padx=(5, 0))
        
        # Files processed section
        processed_frame = ttk.Frame(self.container)
        processed_frame.grid(row=0, column=2, columnspan=2, sticky=tk.EW, padx=10, pady=5)
        
        ttk.Label(processed_frame, text="✅ Processed:", font=header_style).pack(side=tk.LEFT)
        self.processed_files_var = tk.StringVar(value="0")
        ttk.Label(processed_frame, textvariable=self.processed_files_var, font=("Segoe UI", 12, "bold")).pack(side=tk.LEFT, padx=(5, 0))
        
        # Category counts container
        self.categories_frame = ttk.Frame(self.container)
        self.categories_frame.grid(row=1, column=0, columnspan=4, sticky=tk.EW, padx=10, pady=10)
        
        # Category counts (will be added dynamically)
        self.category_vars = {}
        self.next_row = 0
    
    def update_total_files(self, count: int):
        """Update the total files count.
        
        Args:
            count: The total number of files
        """
        self.total_files_var.set(str(count))
    
    def update_processed_files(self, count: int):
        """Update the processed files count.
        
        Args:
            count: The number of processed files
        """
        self.processed_files_var.set(str(count))
    
    def update_category_count(self, category: str, count: int):
        """Update the count for a specific category.
        
        Args:
            category: The category name
            count: The number of files in this category
        """
        # Create category variable if it doesn't exist
        if category not in self.category_vars:
            row = self.next_row // 2
            col = self.next_row % 2
            
            # Create category frame
            cat_frame = ttk.Frame(self.categories_frame)
            cat_frame.grid(row=row, column=col, sticky=tk.EW, padx=5, pady=2)
            
            # Category icon mapping
            icons = {
                "Images": "🖼️",
                "Documents": "📄",
                "Videos": "🎥",
                "Audio": "🎵",
                "Archives": "📦",
                "Code": "💻",
                "Spreadsheets": "📊",
                "Presentations": "📋",
                "Other": "📁"
            }
            icon = icons.get(category, "📁")
            
            # Create label for category
            ttk.Label(cat_frame, text=f"{icon} {category}:", font=("Segoe UI", 9)).pack(side=tk.LEFT)
            
            # Create variable for count
            self.category_vars[category] = tk.StringVar(value="0")
            ttk.Label(cat_frame, textvariable=self.category_vars[category], font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=(5, 0))
            
            self.next_row += 1
        
        # Update the count
        self.category_vars[category].set(str(count))
        
        # Update processed files count
        total_processed = sum(int(var.get()) for var in self.category_vars.values())
        self.update_processed_files(total_processed)
    
    def reset_stats(self):
        """Reset all statistics to zero."""
        self.processed_files_var.set("0")
        for var in self.category_vars.values():
            var.set("0")


class ModernLogFrame(ttk.LabelFrame):
    """A modern frame displaying log messages."""
    
    def __init__(self, parent):
        """Initialize the log frame.
        
        Args:
            parent: The parent widget
        """
        super().__init__(parent, text="📝 Activity Log", padding="15")
        
        # Create main container
        container = ttk.Frame(self)
        container.pack(fill=tk.BOTH, expand=True)
        
        # Create text widget with scrollbar
        self.log_text = tk.Text(
            container, 
            height=12, 
            width=80, 
            wrap=tk.WORD,
            font=("Consolas", 9),
            bg="#f8f9fa",
            fg="#212529",
            insertbackground="#007bff",
            selectbackground="#007bff",
            selectforeground="white"
        )
        
        scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        # Pack widgets
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure tags for different log levels with modern colors
        self.log_text.tag_configure("INFO", foreground="#28a745", font=("Consolas", 9))
        self.log_text.tag_configure("WARNING", foreground="#ffc107", font=("Consolas", 9, "bold"))
        self.log_text.tag_configure("ERROR", foreground="#dc3545", font=("Consolas", 9, "bold"))
        self.log_text.tag_configure("DEBUG", foreground="#6c757d", font=("Consolas", 8))
        self.log_text.tag_configure("SUCCESS", foreground="#28a745", font=("Consolas", 9, "bold"))
        
        # Make text widget read-only
        self.log_text.configure(state=tk.DISABLED)
    
    def add_log_entry(self, message: str, level=logging.INFO):
        """Add a new log entry to the log display.
        
        Args:
            message: The log message
            level: The logging level
        """
        # Map logging level to tag name
        level_tags = {
            logging.INFO: "INFO",
            logging.WARNING: "WARNING",
            logging.ERROR: "ERROR",
            logging.DEBUG: "DEBUG"
        }
        tag = level_tags.get(level, "INFO")
        
        # Enable text widget for editing
        self.log_text.configure(state=tk.NORMAL)
        
        # Add timestamp and message
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        entry = f"[{timestamp}] {message}\n"
        
        # Insert with appropriate tag
        self.log_text.insert(tk.END, entry, tag)
        
        # Scroll to the end
        self.log_text.see(tk.END)
        
        # Disable text widget again
        self.log_text.configure(state=tk.DISABLED)
    
    def clear_log(self):
        """Clear all log entries."""
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.configure(state=tk.DISABLED)


class ModernFolderSelector(ttk.Frame):
    """A modern folder selection component."""
    
    def __init__(self, parent, command):
        """Initialize the folder selector.
        
        Args:
            parent: The parent widget
            command: Callback function when folder is selected
        """
        super().__init__(parent)
        
        # Create main container
        container = ttk.Frame(self)
        container.pack(fill=tk.X, expand=True)
        
        # Folder icon and label
        ttk.Label(container, text="📁 Source Folder:", font=("Segoe UI", 11, "bold")).pack(side=tk.LEFT, padx=(0, 10))
        
        # Entry field
        self.folder_var = tk.StringVar()
        self.entry = ttk.Entry(
            container, 
            textvariable=self.folder_var, 
            width=50,
            font=("Segoe UI", 10)
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # Browse button
        self.browse_btn = ttk.Button(
            container,
            text="Browse",
            command=command,
            width=10
        )
        self.browse_btn.pack(side=tk.RIGHT)
    
    def get_folder(self):
        """Get the selected folder path."""
        return self.folder_var.get()
    
    def set_folder(self, path):
        """Set the folder path."""
        self.folder_var.set(path)


class ModernOptionsFrame(ttk.LabelFrame):
    """A modern options frame with checkboxes and settings."""
    
    def __init__(self, parent):
        """Initialize the options frame.
        
        Args:
            parent: The parent widget
        """
        super().__init__(parent, text="⚙️ Options", padding="15")
        
        # Create main container
        container = ttk.Frame(self)
        container.pack(fill=tk.X, expand=True)
        
        # Preview mode checkbox
        self.preview_var = tk.BooleanVar(value=True)
        self.preview_check = ttk.Checkbutton(
            container,
            text="🔍 Preview Mode (no actual file movement)",
            variable=self.preview_var
        )
        self.preview_check.pack(side=tk.LEFT, padx=(0, 20))
        
        # Additional options can be added here
        self.auto_scan_var = tk.BooleanVar(value=True)
        self.auto_scan_check = ttk.Checkbutton(
            container,
            text="🔄 Auto-scan folder on selection",
            variable=self.auto_scan_var
        )
        self.auto_scan_check.pack(side=tk.LEFT)
    
    def is_preview_mode(self):
        """Check if preview mode is enabled."""
        return self.preview_var.get()
    
    def is_auto_scan_enabled(self):
        """Check if auto-scan is enabled."""
        return self.auto_scan_var.get()


class ModernActionButtons(ttk.Frame):
    """A modern action buttons frame."""
    
    def __init__(self, parent):
        """Initialize the action buttons frame.
        
        Args:
            parent: The parent widget
        """
        super().__init__(parent)
        
        # Create main container
        container = ttk.Frame(self)
        container.pack(fill=tk.X, expand=True)
        
        # Left side buttons
        left_frame = ttk.Frame(container)
        left_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Start sorting button
        self.start_btn = ttk.Button(
            left_frame,
            text="🚀 Start Sorting",
            width=15
        )
        self.start_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Undo button
        self.undo_btn = ttk.Button(
            left_frame,
            text="↩️ Undo Last Operation",
            width=18
        )
        self.undo_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Right side buttons
        right_frame = ttk.Frame(container)
        right_frame.pack(side=tk.RIGHT)
        
        # Save preferences button
        self.save_btn = ttk.Button(
            right_frame,
            text="💾 Save Preferences",
            width=15
        )
        self.save_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Clear log button
        self.clear_btn = ttk.Button(
            right_frame,
            text="🗑️ Clear Log",
            width=12
        )
        self.clear_btn.pack(side=tk.RIGHT)
