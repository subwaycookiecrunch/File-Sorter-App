#!/usr/bin/env python3
"""
File Sorter Application
A GUI application that sorts files into categorized folders with preview mode,
undo functionality, and detailed logging.
"""
import os
import sys
import shutil
import logging
import json
import threading
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
from typing import Dict, List, Tuple, Set, Optional, Any

# Import custom modules
from file_operations import FileOperations
from file_categories import FileCategories
from gui_components import (
    ModernProgressFrame, ModernLogFrame, ModernStatsFrame,
    ModernFolderSelector, ModernOptionsFrame, ModernActionButtons
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class FileSorterApp:
    """Main application class for the File Sorter."""
    
    def __init__(self, root):
        """Initialize the application.
        
        Args:
            root: The tkinter root window
        """
        self.root = root
        self.root.title("🚀 File Sorter Pro")
        self.root.geometry("1000x800")
        self.root.minsize(900, 700)
        
        # Set application icon if available
        try:
            self.root.iconbitmap("icon.ico")
        except tk.TclError:
            pass  # Icon not found, continue without it
        
        # Initialize variables
        self.source_folder = tk.StringVar()
        self.is_preview_mode = tk.BooleanVar(value=True)
        self.is_sorting = False
        self.last_operation = None  # For undo functionality
        self.file_ops = FileOperations()
        self.categories = FileCategories()
        
        # Load user preferences if available
        self.user_prefs_file = "user_preferences.json"
        self.load_preferences()
        
        # Create the main UI
        self.create_widgets()
        
    def load_preferences(self):
        """Load user preferences from file if it exists."""
        try:
            if os.path.exists(self.user_prefs_file):
                with open(self.user_prefs_file, 'r') as f:
                    prefs = json.load(f)
                    
                # Apply custom categories if defined
                if 'custom_categories' in prefs:
                    self.categories.update_custom_categories(prefs['custom_categories'])
                    
                # Apply other preferences
                if 'last_directory' in prefs:
                    self.source_folder.set(prefs['last_directory'])
                    
                logger.info("User preferences loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load preferences: {e}")
    
    def save_preferences(self):
        """Save user preferences to file."""
        try:
            prefs = {
                'last_directory': self.source_folder.get(),
                'custom_categories': self.categories.get_custom_categories()
            }
            
            with open(self.user_prefs_file, 'w') as f:
                json.dump(prefs, f, indent=4)
                
            logger.info("User preferences saved successfully")
        except Exception as e:
            logger.error(f"Failed to save preferences: {e}")
    
    def create_widgets(self):
        """Create all the widgets for the application."""
        # Create main frame with modern styling
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header with title
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(
            header_frame, 
            text="🚀 File Sorter Pro", 
            font=("Segoe UI", 24, "bold")
        )
        title_label.pack()
        
        subtitle_label = ttk.Label(
            header_frame,
            text="Organize your files with style and efficiency",
            font=("Segoe UI", 12)
        )
        subtitle_label.pack()
        
        # Modern folder selector
        self.folder_selector = ModernFolderSelector(main_frame, self.browse_folder)
        self.folder_selector.pack(fill=tk.X, pady=(0, 15))
        
        # Modern options frame
        self.options_frame = ModernOptionsFrame(main_frame)
        self.options_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Modern action buttons
        self.action_buttons = ModernActionButtons(main_frame)
        self.action_buttons.pack(fill=tk.X, pady=(0, 15))
        
        # Connect button commands
        self.action_buttons.start_btn.configure(command=self.start_sorting)
        self.action_buttons.undo_btn.configure(command=self.undo_last_operation)
        self.action_buttons.save_btn.configure(command=self.save_preferences)
        self.action_buttons.clear_btn.configure(command=self.clear_log)
        
        # Progress frame
        self.progress_frame = ModernProgressFrame(main_frame)
        self.progress_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Statistics frame
        self.stats_frame = ModernStatsFrame(main_frame)
        self.stats_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Log frame
        self.log_frame = ModernLogFrame(main_frame)
        self.log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Modern status bar
        self.status_var = tk.StringVar(value="✨ Ready to organize your files!")
        status_bar = ttk.Label(
            self.root, 
            textvariable=self.status_var, 
            relief=tk.FLAT, 
            anchor=tk.W,
            padding="10",
            font=("Segoe UI", 10)
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def browse_folder(self):
        """Open a dialog to select a folder."""
        folder = filedialog.askdirectory(title="Select Folder to Sort")
        if folder:
            self.source_folder.set(folder)
            self.folder_selector.set_folder(folder)
            self.log_message(f"📁 Selected folder: {folder}")
            if self.options_frame.is_auto_scan_enabled():
                self.scan_folder_info()
    
    def scan_folder_info(self):
        """Scan the selected folder and display basic information."""
        folder = self.source_folder.get()
        if not folder or not os.path.isdir(folder):
            return
            
        try:
            file_count = sum(1 for _ in os.scandir(folder) if _.is_file())
            self.log_message(f"Found {file_count} files in the selected folder")
            self.stats_frame.update_total_files(file_count)
        except Exception as e:
            self.log_message(f"Error scanning folder: {e}", level=logging.ERROR)
    
    def start_sorting(self):
        """Start the file sorting process in a separate thread."""
        folder = self.source_folder.get()
        if not folder or not os.path.isdir(folder):
            messagebox.showerror("Error", "Please select a valid folder first")
            return
            
        if self.is_sorting:
            messagebox.showinfo("Info", "Sorting is already in progress")
            return
            
        # Confirm if not in preview mode
        if not self.options_frame.is_preview_mode():
            if not messagebox.askyesno("Confirm", 
                                      "This will move files to categorized folders. Continue?"):
                return
        
        # Start sorting in a separate thread
        self.is_sorting = True
        self.status_var.set("🔄 Sorting in progress...")
        threading.Thread(target=self.sort_files_thread, daemon=True).start()
    
    def sort_files_thread(self):
        """Thread function to perform the actual sorting."""
        folder = self.source_folder.get()
        is_preview = self.options_frame.is_preview_mode()
        
        try:
            # Reset statistics and progress
            self.stats_frame.reset_stats()
            self.progress_frame.reset()
            
            # Get all files in the directory
            files = [f for f in os.scandir(folder) if f.is_file()]
            total_files = len(files)
            
            if total_files == 0:
                self.log_message("No files found in the selected folder")
                self.is_sorting = False
                self.status_var.set("Ready")
                return
                
            self.log_message(f"Starting to {'analyze' if is_preview else 'sort'} {total_files} files")
            self.progress_frame.set_maximum(total_files)
            
            # Track operations for undo functionality
            operations = []
            stats = {category: 0 for category in self.categories.get_all_categories()}
            
            # Process each file
            for i, file_entry in enumerate(files):
                if not self.is_sorting:  # Check if sorting was cancelled
                    break
                    
                file_path = file_entry.path
                file_name = file_entry.name
                
                # Skip hidden/system files
                if file_name.startswith('.') or file_name.startswith('~$'):
                    self.log_message(f"Skipping system/hidden file: {file_name}")
                    continue
                
                # Determine category based on extension
                category = self.categories.get_category_for_file(file_name)
                
                # Create category folder if needed
                category_path = os.path.join(folder, category)
                if not os.path.exists(category_path) and not is_preview:
                    os.makedirs(category_path)
                
                # Determine destination path
                dest_path = os.path.join(category_path, file_name)
                
                # Handle duplicate filenames
                if os.path.exists(dest_path) and not is_preview:
                    base_name, ext = os.path.splitext(file_name)
                    counter = 1
                    while os.path.exists(dest_path):
                        new_name = f"{base_name}_{counter}{ext}"
                        dest_path = os.path.join(category_path, new_name)
                        counter += 1
                
                # Log the operation
                operation_type = "Would move" if is_preview else "Moving"
                self.log_message(f"{operation_type} {file_name} to {category}")
                
                # Actually move the file if not in preview mode
                if not is_preview:
                    try:
                        # Store original timestamp for restoration
                        stat_info = os.stat(file_path)
                        atime, mtime = stat_info.st_atime, stat_info.st_mtime
                        
                        # Move the file
                        shutil.move(file_path, dest_path)
                        
                        # Restore original timestamps
                        os.utime(dest_path, (atime, mtime))
                        
                        # Record operation for undo
                        operations.append((dest_path, file_path))
                    except Exception as e:
                        self.log_message(f"Error moving {file_name}: {e}", level=logging.ERROR)
                        continue
                
                # Update statistics
                stats[category] += 1
                self.stats_frame.update_category_count(category, stats[category])
                
                # Update progress
                self.progress_frame.update_progress(i + 1)
                
                # Small delay to prevent UI freezing
                time.sleep(0.01)
            
            # Save the operations for undo functionality if not in preview mode
            if not is_preview and operations:
                self.last_operation = operations
                
            # Final log message
            mode_text = "Preview completed" if is_preview else "Sorting completed"
            self.log_message(f"✅ {mode_text}. Processed {total_files} files.")
            
            # Update UI
            self.status_var.set("✨ Ready")
            
        except Exception as e:
            self.log_message(f"❌ Error during sorting: {e}", level=logging.ERROR)
            self.status_var.set("❌ Error occurred")
            
        finally:
            self.is_sorting = False
    
    def undo_last_operation(self):
        """Undo the last sorting operation."""
        if not self.last_operation:
            messagebox.showinfo("Info", "No previous operation to undo")
            return
            
        if not messagebox.askyesno("Confirm", 
                                  "This will move files back to their original locations. Continue?"):
            return
            
        self.log_message("Starting undo operation...")
        
        success_count = 0
        error_count = 0
        
        for src_path, dest_path in self.last_operation:
            try:
                # Ensure the destination directory exists
                dest_dir = os.path.dirname(dest_path)
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                    
                # Store original timestamp for restoration
                stat_info = os.stat(src_path)
                atime, mtime = stat_info.st_atime, stat_info.st_mtime
                
                # Move the file back
                shutil.move(src_path, dest_path)
                
                # Restore original timestamps
                os.utime(dest_path, (atime, mtime))
                
                self.log_message(f"Restored {os.path.basename(src_path)} to original location")
                success_count += 1
                
            except Exception as e:
                self.log_message(f"Error during undo: {e}", level=logging.ERROR)
                error_count += 1
        
        # Clear the last operation
        self.last_operation = None
        
        # Final log message
        self.log_message(f"Undo completed. Restored {success_count} files. Errors: {error_count}")
    
    def log_message(self, message, level=logging.INFO):
        """Log a message to both the log file and the UI.
        
        Args:
            message: The message to log
            level: The logging level
        """
        # Log to file
        logger.log(level, message)
        
        # Log to UI
        self.log_frame.add_log_entry(message, level)
    
    def clear_log(self):
        """Clear the log display."""
        self.log_frame.clear_log()
        self.log_message("Log cleared")
    
    def on_closing(self):
        """Handle window closing event."""
        if self.is_sorting:
            if messagebox.askyesno("Confirm", "Sorting is in progress. Do you want to quit anyway?"):
                self.is_sorting = False
            else:
                return
                
        # Save preferences before exiting
        self.save_preferences()
        self.root.destroy()

def main():
    """Main entry point for the application."""
    root = tk.Tk()
    app = FileSorterApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
