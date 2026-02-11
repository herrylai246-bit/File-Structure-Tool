# 📁 File Structure Viewer

A simple and powerful GUI application to visualize, explore, and export file directory structures. Perfect for understanding project layouts, documentation, and sharing folder hierarchies.

## ✨ Features

- 🗂️ **Interactive Tree View** - Browse folders and files with an intuitive tree interface
- 📋 **Copy Paths** - Right-click to copy full file paths or just file names
- 📄 **Export as Text** - Generate a text representation of the entire folder structure
- 💾 **Save to File** - Export the directory tree to a `.txt` file
- 🎯 **Expand/Collapse** - Quickly expand or collapse all folders
- 🎨 **File Icons** - Visual indicators for different file types
- ⚡ **Fast & Lightweight** - No dependencies, uses only Python's built-in libraries

## 🚀 Quick Start

### Option 1: Using Python (Recommended for Development)

**Requirements:**
- Python 3.x (with Tkinter, which comes pre-installed on Windows and macOS)

**Steps:**
1. Clone or download this repository
2. Run the application:
   ```bash
   python file_structure_viewer.py
   ```
3. Click "📁 Select Folder" to choose a directory
4. Explore the structure, right-click to copy paths
5. Click "📄 Export as Text" to see the entire structure as text

### Option 2: Standalone Executable (No Python Required)

Download the pre-built `.exe` file from the [Releases](../../releases) page and simply double-click to run!

## 📖 How to Use

### Viewing the Structure
1. Launch the application
2. Click "📁 Select Folder" button
3. Select any folder from your computer
4. Double-click folders to expand/collapse them

### Copying Paths
- **Right-click** on any file or folder
- Choose "📋 Copy Full Path" to copy the complete file path
- Choose "📋 Copy File Name" to copy just the name

### Exporting Structure
1. Click "📄 Export as Text" button (enabled after selecting a folder)
2. A new window opens showing the entire directory tree
3. Use "📋 Copy All to Clipboard" to copy everything
4. Use "💾 Save to File" to export as a `.txt` file

### Example Output
```
MyProject/
├── src/
│   ├── main.py
│   ├── utils.py
│   └── config.py
├── tests/
│   ├── test_main.py
│   └── test_utils.py
├── README.md
└── .gitignore
```

## 🛠️ Building the Executable

To create a standalone `.exe` file (no Python required):

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Run the build script:
   ```bash
   build.bat
   ```

3. Find your executable in the `dist/` folder:
   - `dist/File Structure Viewer.exe`

## 📋 System Requirements

| OS | Python | Tkinter |
|---|---|---|
| **Windows** | 3.x | ✅ Included |
| **macOS** | 3.x | ✅ Included |
| **Linux** | 3.x | Run: `sudo apt-get install python3-tk` |

## 📁 Project Structure

```
.
├── file_structure_viewer.py    # Main application
├── run.bat                      # Quick launcher (Windows)
├── build.bat                    # Build executable
└── README.md                    # This file
```

## 🎯 Use Cases

- 📚 Document project structure for documentation
- 🔍 Analyze large folder hierarchies
- 📤 Share folder layouts with team members
- 📝 Include directory trees in reports or wikis
- 🗂️ Navigate complex project structures easily

## 🤝 Contributing

Found a bug? Have a feature request? Feel free to open an issue or submit a pull request!

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Credits

Built with Python and Tkinter

## 📞 Support

If you encounter any issues:
1. Make sure Python 3.x is installed correctly
2. Verify Tkinter is available on your system
3. Check that you have read permissions for the folders you're viewing

---

**Made with ❤️ for developers and power users**
