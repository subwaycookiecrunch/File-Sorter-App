# File Sorter Application

A Python application with a GUI interface that helps you organize files by automatically sorting them into categorized folders.

## Features

- **GUI Interface**: User-friendly interface built with tkinter
- **Automatic Categorization**: Sorts files into predefined categories based on file extensions
- **Preview Mode**: See what will be moved before actually moving files
- **Undo Functionality**: Reverse the last sorting operation
- **Progress Tracking**: Monitor sorting progress with a progress bar
- **Statistics**: View counts of files sorted by category
- **Detailed Logging**: Keep track of all operations performed

## File Categories

The application sorts files into the following categories:

- **Images**: .jpg, .jpeg, .png, .gif, .bmp, .tiff, .svg, .webp, .ico
- **Videos**: .mp4, .avi, .mkv, .mov, .wmv, .flv, .webm, .m4v, .3gp
- **Audio**: .mp3, .wav, .flac, .aac, .ogg, .wma, .m4a
- **Documents**: .txt, .rtf, .doc, .docx, .odt
- **PDFs**: .pdf
- **Executables**: .exe, .msi, .deb, .rpm, .dmg, .app
- **Compressed**: .zip, .rar, .7z, .tar, .gz, .bz2, .xz
- **Spreadsheets**: .xls, .xlsx, .csv, .ods
- **Presentations**: .ppt, .pptx, .odp
- **Code**: .py, .js, .html, .css, .java, .cpp, .c, .php, .rb, .go
- **Others**: Any file that doesn't match the above categories

## Safety Features

- Handles duplicate filenames by adding numbers
- Skips system/hidden files
- Error handling for permissions and file access
- Confirmation dialogs for destructive operations
- Preserves original file timestamps

## Requirements

- Python 3.6 or higher
- tkinter (usually comes with Python)

## Usage

1. Run the application: `python file_sorter.py`
2. Select a folder to sort using the "Browse" button
3. Choose whether to use Preview Mode or not
4. Click "Start Sorting" to begin the sorting process
5. View the log for details on each operation
6. Use "Undo Last Operation" if needed

## License

This project is open source and available under the MIT License.
