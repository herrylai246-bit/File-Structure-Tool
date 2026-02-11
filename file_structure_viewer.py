import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import shutil
from pathlib import Path

class FileStructureViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("File Structure Viewer")
        self.root.geometry("900x600")
        
        # Top frame for buttons
        top_frame = ttk.Frame(root)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        # Browse button
        self.browse_btn = ttk.Button(top_frame, text="📁 Select Folder", command=self.browse_folder)
        self.browse_btn.pack(side=tk.LEFT, padx=5)
        
        # Export as text button
        self.export_btn = ttk.Button(top_frame, text="📄 Export as Text", command=self.export_as_text, state=tk.DISABLED)
        self.export_btn.pack(side=tk.LEFT, padx=5)
        
        # Path label
        self.path_label = ttk.Label(top_frame, text="No folder selected", foreground="gray")
        self.path_label.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        # Middle frame for tree view and scrollbar
        middle_frame = ttk.Frame(root)
        middle_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(middle_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview
        self.tree = ttk.Treeview(middle_frame, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)
        self.tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        # Bind right-click context menu and tree events
        self.tree.bind("<Button-3>", self.show_context_menu)
        self.tree.bind("<Button-1>", self.on_item_click)
        self.tree.bind("<<TreeviewOpen>>", self.on_expand)
        
        # Context menu
        self.context_menu = tk.Menu(root, tearoff=0)
        self.context_menu.add_command(label="📋 Copy Full Path", command=self.copy_full_path)
        self.context_menu.add_command(label="📋 Copy File Name", command=self.copy_file_name)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="🔄 Expand All", command=self.expand_all)
        self.context_menu.add_command(label="🔽 Collapse All", command=self.collapse_all)
        
        # Bottom frame for info
        bottom_frame = ttk.Frame(root)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        self.info_label = ttk.Label(bottom_frame, text="Right-click on items to copy paths", foreground="blue")
        self.info_label.pack(side=tk.LEFT)
        
        self.selected_item = None
        self.current_folder = None
    
    def browse_folder(self):
        folder = filedialog.askdirectory(title="Select a folder")
        if folder:
            self.current_folder = folder
            self.path_label.config(text=folder, foreground="black")
            self.export_btn.config(state=tk.NORMAL)
            self.load_folder_structure(folder)
    
    def load_folder_structure(self, path):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add root
        root_item = self.tree.insert("", "end", text=os.path.basename(path), open=True)
        self.populate_tree(root_item, path)
    
    def populate_tree(self, parent, path):
        try:
            items = sorted(os.listdir(path), key=lambda x: (not os.path.isdir(os.path.join(path, x)), x.lower()))
            
            for item in items:
                item_path = os.path.join(path, item)
                
                if os.path.isdir(item_path):
                    node = self.tree.insert(parent, "end", text=f"📁 {item}", open=False)
                    # Add dummy child to show expand arrow
                    self.tree.insert(node, "end", text="loading...")
                else:
                    # Get file extension for icon
                    ext = os.path.splitext(item)[1].lower()
                    icon = self.get_file_icon(ext)
                    self.tree.insert(parent, "end", text=f"{icon} {item}")
        except PermissionError:
            pass
    
    def on_expand(self, event):
        item = self.tree.selection()[0] if self.tree.selection() else None
        if not item:
            return
            
        children = self.tree.get_children(item)
        
        # Check if there's a "loading..." placeholder
        if children and self.tree.item(children[0], "text") == "loading...":
            self.tree.delete(children[0])
            
            # Get the full path
            full_path = self.get_item_path(item)
            
            if os.path.isdir(full_path):
                self.populate_tree(item, full_path)
    
    def get_item_path(self, item):
        path_parts = []
        current = item
        
        while current:
            text = self.tree.item(current, "text")
            # Remove icon emoji
            text = text.replace("📁 ", "").replace("📄 ", "").replace("📋 ", "")
            for ext_icon in ["🐍", "📝", "🎵", "🖼️", "⚙️", "🔗"]:
                text = text.replace(ext_icon + " ", "")
            
            path_parts.insert(0, text)
            parent = self.tree.parent(current)
            if not parent:
                break
            current = parent
        
        full_path = os.path.join(*path_parts) if self.current_folder else "/".join(path_parts)
        
        if self.current_folder and path_parts[0] == os.path.basename(self.current_folder):
            full_path = self.current_folder
            for part in path_parts[1:]:
                full_path = os.path.join(full_path, part)
        
        return full_path
    
    def get_file_icon(self, ext):
        icons = {
            '.py': '🐍',
            '.txt': '📝',
            '.pdf': '📄',
            '.mp3': '🎵',
            '.wav': '🎵',
            '.jpg': '🖼️',
            '.png': '🖼️',
            '.gif': '🖼️',
            '.exe': '⚙️',
            '.zip': '🔗',
        }
        return icons.get(ext, '📄')
    
    def show_context_menu(self, event):
        item = self.tree.identify("item", event.x, event.y)
        if item:
            self.selected_item = item
            self.tree.selection_set(item)
            try:
                self.context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.context_menu.grab_release()
    
    def on_item_click(self, event):
        item = self.tree.identify("item", event.x, event.y)
        if item:
            self.selected_item = item
    
    def copy_full_path(self):
        if self.selected_item:
            full_path = self.get_item_path(self.selected_item)
            self.copy_to_clipboard(full_path)
            self.info_label.config(text=f"✓ Copied: {full_path}", foreground="green")
            self.root.after(3000, lambda: self.info_label.config(text="Right-click on items to copy paths", foreground="blue"))
    
    def copy_file_name(self):
        if self.selected_item:
            text = self.tree.item(self.selected_item, "text")
            # Remove icons
            text = text.replace("📁 ", "").replace("📄 ", "").replace("📋 ", "")
            for ext_icon in ["🐍", "📝", "🎵", "🖼️", "⚙️", "🔗"]:
                text = text.replace(ext_icon + " ", "")
            
            self.copy_to_clipboard(text)
            self.info_label.config(text=f"✓ Copied: {text}", foreground="green")
            self.root.after(3000, lambda: self.info_label.config(text="Right-click on items to copy paths", foreground="blue"))
    
    def copy_to_clipboard(self, text):
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()
    
    def expand_all(self):
        self.expand_tree(self.tree.get_children()[0])
    
    def expand_tree(self, item):
        self.tree.item(item, open=True)
        for child in self.tree.get_children(item):
            self.expand_tree(child)
    
    def collapse_all(self):
        self.collapse_tree(self.tree.get_children()[0])
    
    def collapse_tree(self, item):
        self.tree.item(item, open=False)
        for child in self.tree.get_children(item):
            self.collapse_tree(child)
    
    def export_as_text(self):
        if not self.current_folder:
            messagebox.showwarning("No Folder", "Please select a folder first")
            return
        
        # Generate text representation
        text_content = self.generate_tree_text(self.current_folder)
        
        # Create new window
        export_window = tk.Toplevel(self.root)
        export_window.title("File Structure - Text Format")
        export_window.geometry("800x600")
        
        # Create frame with scrollbar
        frame = ttk.Frame(export_window)
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Text widget
        text_widget = tk.Text(frame, yscrollcommand=scrollbar.set, font=("Courier", 10), wrap=tk.NONE)
        text_widget.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        scrollbar.config(command=text_widget.yview)
        
        # Insert text
        text_widget.insert("1.0", text_content)
        text_widget.config(state=tk.DISABLED)
        
        # Button frame
        btn_frame = ttk.Frame(export_window)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        def copy_all():
            text_widget.config(state=tk.NORMAL)
            text_widget.tag_add(tk.SEL, "1.0", tk.END)
            text_widget.event_generate("<<Copy>>")
            text_widget.tag_remove(tk.SEL, "1.0", tk.END)
            text_widget.config(state=tk.DISABLED)
            messagebox.showinfo("Success", "File structure copied to clipboard!")
        
        def save_to_file():
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if file_path:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(text_content)
                messagebox.showinfo("Success", f"Saved to {file_path}")
        
        copy_btn = ttk.Button(btn_frame, text="📋 Copy All to Clipboard", command=copy_all)
        copy_btn.pack(side=tk.LEFT, padx=5)
        
        save_btn = ttk.Button(btn_frame, text="💾 Save to File", command=save_to_file)
        save_btn.pack(side=tk.LEFT, padx=5)
    
    def generate_tree_text(self, path, prefix=""):
        """Generate text representation of directory tree - shows all files"""
        result = []
        
        try:
            items = sorted(os.listdir(path), key=lambda x: (not os.path.isdir(os.path.join(path, x)), x.lower()))
        except PermissionError:
            return ""
        
        # Add root folder
        root_name = os.path.basename(path)
        result.append(f"{root_name}/")
        
        # Process items
        for idx, item in enumerate(items):
            item_path = os.path.join(path, item)
            is_last_item = (idx == len(items) - 1)
            
            # Build connector
            connector = "└── " if is_last_item else "├── "
            result.append(f"{prefix}{connector}{item}")
            
            # Recursively add subdirectories
            if os.path.isdir(item_path):
                try:
                    next_prefix = prefix + ("    " if is_last_item else "│   ")
                    sub_result = self.generate_tree_text(item_path, next_prefix)
                    if sub_result:
                        # Remove the root folder name from sub_result since we already added it
                        sub_lines = sub_result.split("\n")
                        result.extend(sub_lines[1:])  # Skip first line (folder name)
                except PermissionError:
                    pass
        
        return "\n".join(result)


if __name__ == "__main__":
    root = tk.Tk()
    app = FileStructureViewer(root)
    root.mainloop()
