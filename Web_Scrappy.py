import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog, ttk
import textwrap
import os
import threading
from urllib.parse import urljoin
import time
import json
import csv

class WebScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Web Scraper")
        self.root.geometry("900x700")
        self.root.configure(bg="#2C3E50")
        
        # Variables
        self.scraping = False
        self.stop_scraping = False
        self.output_format = tk.StringVar(value="txt")
        
        # Create UI
        self.create_widgets()
        
        # Ensure output folder exists
        self.output_folder = os.path.join(os.getcwd(), "output")
        os.makedirs(self.output_folder, exist_ok=True)
    
    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg="#2C3E50")
        main_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # URL Entry
        url_frame = tk.Frame(main_frame, bg="#2C3E50")
        url_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(url_frame, text="Website URL:", font=("Arial", 12, "bold"), 
                fg="#ECF0F1", bg="#2C3E50").pack(side=tk.LEFT, padx=5)
        
        self.url_entry = tk.Entry(url_frame, width=70, font=("Arial", 12))
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Options Frame
        options_frame = tk.Frame(main_frame, bg="#2C3E50")
        options_frame.pack(fill=tk.X, pady=10)
        
        # Content to scrape
        tk.Label(options_frame, text="Scrape:", font=("Arial", 10), 
                fg="#ECF0F1", bg="#2C3E50").pack(side=tk.LEFT, padx=5)
        
        self.scrape_headings = tk.BooleanVar(value=True)
        tk.Checkbutton(options_frame, text="Headings", variable=self.scrape_headings, 
                      bg="#2C3E50", fg="#ECF0F1", selectcolor="#34495E").pack(side=tk.LEFT, padx=5)
        
        self.scrape_paragraphs = tk.BooleanVar(value=True)
        tk.Checkbutton(options_frame, text="Paragraphs", variable=self.scrape_paragraphs, 
                      bg="#2C3E50", fg="#ECF0F1", selectcolor="#34495E").pack(side=tk.LEFT, padx=5)
        
        self.scrape_lists = tk.BooleanVar(value=True)
        tk.Checkbutton(options_frame, text="Lists", variable=self.scrape_lists, 
                      bg="#2C3E50", fg="#ECF0F1", selectcolor="#34495E").pack(side=tk.LEFT, padx=5)
        
        self.scrape_tables = tk.BooleanVar(value=True)
        tk.Checkbutton(options_frame, text="Tables", variable=self.scrape_tables, 
                      bg="#2C3E50", fg="#ECF0F1", selectcolor="#34495E").pack(side=tk.LEFT, padx=5)
        
        # Output format
        tk.Label(options_frame, text="Format:", font=("Arial", 10), 
                fg="#ECF0F1", bg="#2C3E50").pack(side=tk.LEFT, padx=(20,5))
        
        formats = [("TXT", "txt"), ("JSON", "json"), ("CSV", "csv")]
        for text, value in formats:
            tk.Radiobutton(options_frame, text=text, variable=self.output_format, 
                         value=value, bg="#2C3E50", fg="#ECF0F1", selectcolor="#34495E").pack(side=tk.LEFT, padx=2)
        
        # Depth control
        tk.Label(options_frame, text="Depth:", font=("Arial", 10), 
                fg="#ECF0F1", bg="#2C3E50").pack(side=tk.LEFT, padx=(20,5))
        
        self.depth_var = tk.IntVar(value=1)
        tk.Spinbox(options_frame, from_=1, to=5, textvariable=self.depth_var, 
                 width=3, font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        
        # Button Frame
        button_frame = tk.Frame(main_frame, bg="#2C3E50")
        button_frame.pack(fill=tk.X, pady=10)
        
        self.scrape_button = tk.Button(button_frame, text="Start Scraping", font=("Arial", 12, "bold"), 
                                     bg="#27AE60", fg="white", command=self.toggle_scraping)
        self.scrape_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = tk.Button(button_frame, text="Stop", font=("Arial", 12), 
                                   bg="#E74C3C", fg="white", state=tk.DISABLED, command=self.stop_scraping_process)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Save As...", font=("Arial", 12), 
                bg="#3498DB", fg="white", command=self.save_as).pack(side=tk.RIGHT, padx=5)
        
        tk.Button(button_frame, text="Open Output Folder", font=("Arial", 12), 
                bg="#3498DB", fg="white", command=self.open_output_folder).pack(side=tk.RIGHT, padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.progress.pack(fill=tk.X, pady=5)
        
        # Status label
        self.status_label = tk.Label(main_frame, text="Ready", font=("Arial", 10), 
                                    fg="#ECF0F1", bg="#2C3E50", anchor=tk.W)
        self.status_label.pack(fill=tk.X, pady=5)
        
        # Text area
        self.text_area = scrolledtext.ScrolledText(main_frame, width=100, height=25, 
                                                 font=("Consolas", 10), bg="#34495E", fg="#ECF0F1")
        self.text_area.pack(fill=tk.BOTH, expand=True)
    
    def toggle_scraping(self):
        if self.scraping:
            self.stop_scraping_process()
        else:
            self.start_scraping_process()
    
    def start_scraping_process(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a valid URL")
            return
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        self.scraping = True
        self.stop_scraping = False
        self.scrape_button.config(text="Stop Scraping", bg="#E74C3C")
        self.stop_button.config(state=tk.NORMAL)
        self.text_area.delete('1.0', tk.END)
        self.update_status("Starting scraping process...")
        
        # Start scraping in a separate thread
        threading.Thread(target=self.scrape_website, args=(url,), daemon=True).start()
    
    def stop_scraping_process(self):
        self.stop_scraping = True
        self.update_status("Stopping scraping process...")
    
    def update_status(self, message):
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
    def update_progress(self, value):
        self.progress['value'] = value
        self.root.update_idletasks()
    
    def save_as(self):
        file_types = [
            ("Text files", "*.txt"),
            ("JSON files", "*.json"),
            ("CSV files", "*.csv"),
            ("All files", "*.*")
        ]
        
        file_path = filedialog.asksaveasfilename(
            initialdir=self.output_folder,
            title="Save As",
            filetypes=file_types,
            defaultextension=".txt"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.text_area.get('1.0', tk.END))
                messagebox.showinfo("Success", f"Data saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")
    
    def open_output_folder(self):
        try:
            os.startfile(self.output_folder)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open folder: {e}")
    
    def categorize_text(self, text):
        length = len(text.split())
        if length < 50:
            return "(Short)"
        elif length < 200:
            return "(Medium)"
        else:
            return "(Long)"
    
    def scrape_website(self, start_url):
        try:
            visited_urls = set()
            to_visit = [(start_url, 0)]  # (url, depth)
            all_data = []
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            max_depth = self.depth_var.get()
            total_pages = 0
            processed_pages = 0
            
            # First pass to count pages (for progress bar)
            if not self.stop_scraping:
                self.update_status("Counting pages to scrape...")
                temp_visited = set()
                temp_queue = [(start_url, 0)]
                while temp_queue and not self.stop_scraping:
                    current_url, depth = temp_queue.pop(0)
                    if current_url in temp_visited or depth > max_depth:
                        continue
                    temp_visited.add(current_url)
                    total_pages += 1
                    
                    try:
                        response = requests.get(current_url, headers=headers, timeout=10)
                        soup = BeautifulSoup(response.text, 'html.parser')
                        
                        for link in soup.find_all('a', href=True):
                            next_url = urljoin(current_url, link['href'])
                            if start_url in next_url and next_url not in temp_visited and depth < max_depth:
                                temp_queue.append((next_url, depth + 1))
                    except:
                        continue
            
            if total_pages == 0:
                total_pages = 1  # Prevent division by zero
            
            # Actual scraping
            while to_visit and not self.stop_scraping:
                current_url, depth = to_visit.pop(0)
                
                if current_url in visited_urls or depth > max_depth:
                    continue
                
                self.update_status(f"Scraping: {current_url} (Depth: {depth})")
                self.update_progress((processed_pages / total_pages) * 100)
                
                try:
                    response = requests.get(current_url, headers=headers, timeout=10)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    page_data = {
                        "url": current_url,
                        "headings": [],
                        "paragraphs": [],
                        "lists": [],
                        "tables": []
                    }
                    
                    # Extract requested content
                    if self.scrape_headings.get():
                        headings = [(h.name, h.get_text(strip=True), self.categorize_text(h.get_text(strip=True))) 
                                  for h in soup.find_all(['h1', 'h2', 'h3']) if h.get_text(strip=True)]
                        page_data["headings"] = headings
                    
                    if self.scrape_paragraphs.get():
                        paragraphs = [(p.get_text(strip=True), self.categorize_text(p.get_text(strip=True))) 
                                    for p in soup.find_all('p') if p.get_text(strip=True)]
                        page_data["paragraphs"] = paragraphs
                    
                    if self.scrape_lists.get():
                        lists = [(li.get_text(strip=True), self.categorize_text(li.get_text(strip=True))) 
                               for li in soup.find_all('li') if li.get_text(strip=True)]
                        page_data["lists"] = lists
                    
                    if self.scrape_tables.get():
                        tables = []
                        for table in soup.find_all('table'):
                            rows = table.find_all('tr')
                            for row in rows:
                                cells = row.find_all(['td', 'th'])
                                row_text = " | ".join(cell.get_text(strip=True) for cell in cells)
                                tables.append((row_text, self.categorize_text(row_text)))
                        page_data["tables"] = tables
                    
                    all_data.append(page_data)
                    visited_urls.add(current_url)
                    processed_pages += 1
                    
                    # Find and queue additional links
                    for link in soup.find_all('a', href=True):
                        next_url = urljoin(current_url, link['href'])
                        if start_url in next_url and next_url not in visited_urls and depth < max_depth:
                            to_visit.append((next_url, depth + 1))
                    
                    # Be polite to the server
                    time.sleep(0.5)
                
                except requests.exceptions.RequestException as e:
                    self.text_area.insert(tk.END, f"Error scraping {current_url}: {str(e)}\n")
                    continue
            
            # Save results
            if not self.stop_scraping and all_data:
                output_format = self.output_format.get()
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                output_file = os.path.join(self.output_folder, f"scraped_data_{timestamp}.{output_format}")
                
                try:
                    if output_format == "json":
                        with open(output_file, 'w', encoding='utf-8') as f:
                            json.dump(all_data, f, indent=2, ensure_ascii=False)
                    elif output_format == "csv":
                        # Flatten data for CSV
                        csv_data = []
                        for page in all_data:
                            for section in ['headings', 'paragraphs', 'lists', 'tables']:
                                for item in page[section]:
                                    csv_data.append({
                                        'url': page['url'],
                                        'type': section[:-1],  # Remove 's' (headings -> heading)
                                        'content': item[0],
                                        'category': item[1] if len(item) > 1 else ''
                                    })
                        
                        with open(output_file, 'w', encoding='utf-8', newline='') as f:
                            writer = csv.DictWriter(f, fieldnames=['url', 'type', 'content', 'category'])
                            writer.writeheader()
                            writer.writerows(csv_data)
                    else:  # txt
                        with open(output_file, 'w', encoding='utf-8') as f:
                            for page in all_data:
                                f.write(f"URL: {page['url']}\n\n")
                                
                                if page['headings']:
                                    f.write("=== Headings ===\n")
                                    for tag, text, category in page['headings']:
                                        f.write(f"{tag.upper()}: {text} {category}\n")
                                    f.write("\n")
                                
                                if page['paragraphs']:
                                    f.write("=== Paragraphs ===\n")
                                    for text, category in page['paragraphs']:
                                        f.write(f"{textwrap.fill(text, width=80)} {category}\n")
                                    f.write("\n")
                                
                                if page['lists']:
                                    f.write("=== Lists ===\n")
                                    for text, category in page['lists']:
                                        f.write(f"- {text} {category}\n")
                                    f.write("\n")
                                
                                if page['tables']:
                                    f.write("=== Table Data ===\n")
                                    for text, category in page['tables']:
                                        f.write(f"{text} {category}\n")
                                    f.write("\n")
                                
                                f.write("="*80 + "\n\n")
                    
                    # Display results in text area
                    self.text_area.delete('1.0', tk.END)
                    self.text_area.insert(tk.END, f"Scraping completed!\n\n")
                    self.text_area.insert(tk.END, f"Pages scraped: {len(all_data)}\n")
                    self.text_area.insert(tk.END, f"Data saved to:\n{output_file}\n\n")
                    
                    with open(output_file, 'r', encoding='utf-8') as f:
                        self.text_area.insert(tk.END, f.read())
                    
                    self.update_status(f"Scraping completed. Data saved to {output_file}")
                    messagebox.showinfo("Success", f"Data saved to {output_file}")
                
                except Exception as e:
                    self.text_area.insert(tk.END, f"\nError saving results: {str(e)}\n")
                    self.update_status(f"Error saving results: {str(e)}")
            
            elif self.stop_scraping:
                self.text_area.insert(tk.END, "\nScraping stopped by user\n")
                self.update_status("Scraping stopped by user")
            
            else:
                self.text_area.insert(tk.END, "\nNo data scraped\n")
                self.update_status("No data scraped")
        
        except Exception as e:
            self.text_area.insert(tk.END, f"\nError: {str(e)}\n")
            self.update_status(f"Error: {str(e)}")
        
        finally:
            self.scraping = False
            self.stop_scraping = False
            self.scrape_button.config(text="Start Scraping", bg="#27AE60")
            self.stop_button.config(state=tk.DISABLED)
            self.update_progress(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = WebScraperApp(root)
    root.mainloop()
