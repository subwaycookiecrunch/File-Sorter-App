"""
File Operations Module
Handles file operations for the File Sorter application.
"""
import os
import shutil
import logging
from typing import List, Tuple, Dict, Optional, Any

logger = logging.getLogger(__name__)

class FileOperations:
    """Handles file operations such as moving, copying, and backing up files."""
    
    def __init__(self):
        """Initialize the file operations handler."""
        self.backup_dir = None
    
    def move_file(self, source_path: str, dest_path: str, 
                 preserve_timestamps: bool = True) -> bool:
        """Move a file from source to destination.
        
        Args:
            source_path: Path to the source file
            dest_path: Path to the destination
            preserve_timestamps: Whether to preserve original timestamps
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure destination directory exists
            dest_dir = os.path.dirname(dest_path)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            
            # Store original timestamps if needed
            if preserve_timestamps:
                stat_info = os.stat(source_path)
                atime, mtime = stat_info.st_atime, stat_info.st_mtime
            
            # Move the file
            shutil.move(source_path, dest_path)
            
            # Restore original timestamps if needed
            if preserve_timestamps:
                os.utime(dest_path, (atime, mtime))
            
            logger.info(f"Moved {source_path} to {dest_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error moving file {source_path}: {e}")
            return False
    
    def handle_duplicate(self, dest_path: str) -> str:
        """Handle duplicate filenames by adding a number suffix.
        
        Args:
            dest_path: The destination path that already exists
            
        Returns:
            A new destination path that doesn't exist
        """
        if not os.path.exists(dest_path):
            return dest_path
            
        directory, filename = os.path.split(dest_path)
        name, ext = os.path.splitext(filename)
        
        counter = 1
        new_path = dest_path
        
        while os.path.exists(new_path):
            new_filename = f"{name}_{counter}{ext}"
            new_path = os.path.join(directory, new_filename)
            counter += 1
            
        return new_path
    
    def create_backup(self, source_dir: str) -> Optional[str]:
        """Create a backup of files before sorting.
        
        Args:
            source_dir: Directory to back up
            
        Returns:
            Path to backup directory if successful, None otherwise
        """
        try:
            # Create a backup directory
            import time
            backup_name = f"backup_{os.path.basename(source_dir)}_{int(time.time())}"
            backup_path = os.path.join(os.path.dirname(source_dir), backup_name)
            
            if not os.path.exists(backup_path):
                os.makedirs(backup_path)
            
            # Copy all files (not directories) to the backup
            for item in os.scandir(source_dir):
                if item.is_file():
                    shutil.copy2(item.path, backup_path)
            
            self.backup_dir = backup_path
            logger.info(f"Created backup at {backup_path}")
            return backup_path
            
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            return None
    
    def restore_from_backup(self) -> bool:
        """Restore files from the last backup.
        
        Returns:
            True if successful, False otherwise
        """
        if not self.backup_dir or not os.path.exists(self.backup_dir):
            logger.error("No backup directory available for restoration")
            return False
            
        try:
            # Get the original directory (parent of backup)
            original_dir = os.path.dirname(self.backup_dir)
            
            # Copy all files from backup to original directory
            for item in os.scandir(self.backup_dir):
                if item.is_file():
                    dest_path = os.path.join(original_dir, item.name)
                    shutil.copy2(item.path, dest_path)
            
            logger.info(f"Restored files from backup {self.backup_dir}")
            return True
            
        except Exception as e:
            logger.error(f"Error restoring from backup: {e}")
            return False
    
    def is_system_or_hidden_file(self, filename: str) -> bool:
        """Check if a file is a system or hidden file.
        
        Args:
            filename: Name of the file to check
            
        Returns:
            True if the file is a system or hidden file, False otherwise
        """
        # Simple check for hidden files on Windows and Unix
        return filename.startswith('.') or filename.startswith('~$')
