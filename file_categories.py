"""
File Categories Module
Defines the categories and file extensions for the File Sorter application.
"""
import os
from typing import Dict, List, Set, Optional

class FileCategories:
    """Manages file categories and their associated extensions."""
    
    def __init__(self):
        """Initialize with default categories and extensions."""
        # Default category definitions
        self.categories = {
            "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp", ".ico"],
            "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".m4v", ".3gp"],
            "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a"],
            "Documents": [".txt", ".rtf", ".doc", ".docx", ".odt"],
            "PDFs": [".pdf"],
            "Executables": [".exe", ".msi", ".deb", ".rpm", ".dmg", ".app"],
            "Compressed": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"],
            "Spreadsheets": [".xls", ".xlsx", ".csv", ".ods"],
            "Presentations": [".ppt", ".pptx", ".odp"],
            "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".php", ".rb", ".go"],
            "Others": []  # Catch-all category
        }
        
        # Extension to category mapping for quick lookups
        self.extension_map = {}
        self._build_extension_map()
        
    def _build_extension_map(self):
        """Build a mapping of extensions to categories for quick lookups."""
        self.extension_map = {}
        for category, extensions in self.categories.items():
            for ext in extensions:
                self.extension_map[ext.lower()] = category
    
    def get_category_for_file(self, filename: str) -> str:
        """Determine the category for a given filename based on its extension.
        
        Args:
            filename: The name of the file to categorize
            
        Returns:
            The category name for the file
        """
        _, ext = os.path.splitext(filename)
        ext = ext.lower()
        
        # Return the category if the extension is known
        if ext in self.extension_map:
            return self.extension_map[ext]
        
        # Return "Others" for unknown extensions
        return "Others"
    
    def get_all_categories(self) -> List[str]:
        """Get a list of all category names.
        
        Returns:
            List of category names
        """
        return list(self.categories.keys())
    
    def get_extensions_for_category(self, category: str) -> List[str]:
        """Get all extensions for a specific category.
        
        Args:
            category: The category name
            
        Returns:
            List of extensions for the category
        """
        if category in self.categories:
            return self.categories[category]
        return []
    
    def update_custom_categories(self, custom_categories: Dict[str, List[str]]):
        """Update or add custom categories.
        
        Args:
            custom_categories: Dictionary mapping category names to lists of extensions
        """
        for category, extensions in custom_categories.items():
            self.categories[category] = extensions
        
        # Rebuild the extension map
        self._build_extension_map()
    
    def get_custom_categories(self) -> Dict[str, List[str]]:
        """Get the current categories configuration.
        
        Returns:
            Dictionary of all categories and their extensions
        """
        return self.categories
