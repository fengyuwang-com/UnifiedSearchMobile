import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
import webbrowser
from urllib.parse import quote
from datetime import datetime

# 配置文件路径
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'platforms_config.json')
HISTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'query_history.json')

# 配色方案
COLORS = {
    'bg': '#f5f5f7',
    'card': '#ffffff',
    'primary': '#0071e3',
    'primary_hover': '#0077ed',
    'success': '#34c759',
    'warning': '#ff9500',
    'text': '#1d1d1f',
    'text_secondary': '#86868b',
    'border': '#d2d2d7',
    'hover': '#f5f5f7',
}

# 默认平台配置 - 哔哩哔哩默认勾选，GitHub默认不勾选
DEFAULT_PLATFORMS = [
    {
        "id": "perplexity",
        "name": "Perplexity AI",
        "url": "https://www.perplexity.ai/search?q=%query%",
        "type": "ai",
        "description": "AI搜索引擎",
        "enabled": True
    },
    {
        "id": "google",
        "name": "Google",
        "url": "https://www.google.com/search?q=%query%",
        "type": "search",
        "description": "谷歌搜索",
        "enabled": True
    },
    {
        "id": "bing",
        "name": "Bing",
        "url": "https://www.bing.com/search?q=%query%",
        "type": "search",
        "description": "必应搜索",
        "enabled": True
    },
    {
        "id": "you",
        "name": "You.com",
        "url": "https://you.com/search?q=%query%",
        "type": "ai",
        "description": "AI搜索引擎",
        "enabled": True
    },
    {
        "id": "bilibili",
        "name": "Bilibili",
        "url": "https://search.bilibili.com/all?keyword=%query%",
        "type": "search",
        "description": "B站搜索",
        "enabled": True
    },
    {
        "id": "github",
        "name": "GitHub",
        "url": "https://github.com/search?q=%query%",
        "type": "search",
        "description": "代码搜索",
        "enabled": False
    },
    {
        "id": "youtube",
        "name": "YouTube",
        "url": "https://www.youtube.com/results?search_query=%query%",
        "type": "search",
        "description": "视频搜索",
        "enabled": False
    },
    {
        "id": "ecosia",
        "name": "Ecosia",
        "url": "https://www.ecosia.org/search?q=%query%",
        "type": "search",
        "description": "环保搜索引擎",
        "enabled": False
    },
    {
        "id": "chatgpt",
        "name": "ChatGPT",
        "url": "https://chat.openai.com",
        "type": "ai",
        "description": "需手动输入",
        "enabled": False
    },
    {
        "id": "claude",
        "name": "Claude",
        "url": "https://claude.ai",
        "type": "ai",
        "description": "需手动输入",
        "enabled": False
    },
]

class UnifiedSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("一键搜索")
        self.root.geometry("750x620")
        self.root.minsize(650, 500)
        self.root.resizable(True, True)
        self.root.configure(bg=COLORS['bg'])
        
        self.center_window()
        
        # 加载配置 - 先从JSON读取
        self.platforms = self.load_config()
        
        self.setup_ui()
        
    def center_window(self):
        """窗口居中"""
        self.root.update_idletasks()
        width = 750
        height = 620
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        """设置界面"""
        main_container = tk.Frame(self.root, bg=COLORS['bg'])
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_rowconfigure(4, weight=1)
        
        # ===== 标题区域 =====
        header = tk.Frame(main_container, bg=COLORS['bg'])
        header.grid(row=0, column=0, sticky='ew', pady=(0, 10))
        
        tk.Label(header, text="一键搜索", font=('Arial', 20, 'bold'),
                bg=COLORS['bg'], fg=COLORS['primary']).pack()
        tk.Label(header, text="同时在多个搜索引擎和AI平台提问", 
                font=('Arial', 10), bg=COLORS['bg'], fg=COLORS['text_secondary']).pack()
        
        # ===== 输入区域 =====
        input_card = tk.Frame(main_container, bg=COLORS['card'], bd=0)
        input_card.grid(row=1, column=0, sticky='ew', pady=(0, 10))
        
        input_inner = tk.Frame(input_card, bg=COLORS['card'])
        input_inner.pack(fill='both', expand=True, padx=12, pady=12)
        
        # 输入框标题行
        input_header = tk.Frame(input_inner, bg=COLORS['card'])
        input_header.pack(fill='x', pady=(0, 6))
        
        tk.Label(input_header, text="输入你的问题或关键词：", 
                font=('Arial', 11, 'bold'), bg=COLORS['card'], fg=COLORS['text']).pack(side='left')
        
        # 统计标签
        self.stats_label = tk.Label(input_header, 
                                   text=f"已启用 {self.get_enabled_count()} 个平台",
                                   font=('Arial', 9), bg=COLORS['card'], fg=COLORS['text_secondary'])
        self.stats_label.pack(side='right')
        
        # 多行输入框
        self.query_text = scrolledtext.ScrolledText(
            input_inner,
            font=('Arial', 11),
            bg='white',
            relief='solid',
            bd=1,
            height=3,
            wrap=tk.WORD
        )
        self.query_text.pack(fill='x', pady=(0, 8))
        
        # 按钮行
        btn_row = tk.Frame(input_inner, bg=COLORS['card'])
        btn_row.pack(fill='x')
        
        # 清空按钮
        tk.Button(btn_row, text="🗑️ 清空", font=('Arial', 9),
                 bg='#e8e8ed', relief='flat', bd=0, cursor='hand2',
                 padx=12, pady=4, command=self.clear_input).pack(side='left', padx=(0, 8))
        
        # 剪贴板复选框
        self.clipboard_var = tk.BooleanVar(value=False)
        clipboard_chk = tk.Checkbutton(btn_row, text="📋 复制到剪贴板", 
                                      variable=self.clipboard_var,
                                      font=('Arial', 9),
                                      bg=COLORS['card'], cursor='hand2')
        clipboard_chk.pack(side='left')
        
        # 主要操作按钮
        search_btn = tk.Button(btn_row, text="🚀 一键搜索", 
                              font=('Arial', 11, 'bold'),
                              bg=COLORS['success'], fg='white', 
                              relief='flat', bd=0, cursor='hand2',
                              padx=25, pady=6, command=self.search_all)
        search_btn.pack(side='right')
        
        # 剪贴板说明
        clipboard_hint = tk.Label(input_inner, 
                                 text="💡 勾选\"复制到剪贴板\"后，搜索时会自动复制问题，方便粘贴到ChatGPT等需要手动输入的AI平台",
                                 font=('Arial', 8), bg=COLORS['card'], 
                                 fg=COLORS['text_secondary'], wraplength=700)
        clipboard_hint.pack(fill='x', pady=(5, 0))
        
        # ===== 平台管理工具栏 =====
        toolbar_card = tk.Frame(main_container, bg=COLORS['card'])
        toolbar_card.grid(row=2, column=0, sticky='ew', pady=(0, 8))
        
        toolbar_inner = tk.Frame(toolbar_card, bg=COLORS['card'])
        toolbar_inner.pack(fill='x', padx=12, pady=8)
        
        tk.Label(toolbar_inner, text="平台列表（勾选以启用）：", 
                font=('Arial', 10, 'bold'), bg=COLORS['card'], fg=COLORS['text']).pack(side='left')
        
        # 右侧按钮
        btn_frame = tk.Frame(toolbar_inner, bg=COLORS['card'])
        btn_frame.pack(side='right')
        
        tk.Button(btn_frame, text="➕ 添加", font=('Arial', 9, 'bold'),
                 bg=COLORS['primary'], fg='white', relief='flat', bd=0,
                 cursor='hand2', padx=10, pady=3, command=self.add_platform).pack(side='left')
        
        # ===== 平台列表区域 =====
        list_frame = tk.Frame(main_container, bg=COLORS['card'])
        list_frame.grid(row=3, column=0, sticky='nsew')
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(0, weight=1)
        
        # 创建Canvas和滚动条
        canvas_frame = tk.Frame(list_frame, bg=COLORS['card'])
        canvas_frame.grid(row=0, column=0, sticky='nsew', padx=(12, 0), pady=8)
        canvas_frame.grid_columnconfigure(0, weight=1)
        canvas_frame.grid_rowconfigure(0, weight=1)
        
        self.canvas = tk.Canvas(canvas_frame, bg=COLORS['card'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.canvas.yview)
        
        self.platforms_frame = tk.Frame(self.canvas, bg=COLORS['card'])
        self.canvas.create_window((0, 0), window=self.platforms_frame, anchor='nw', width=700)
        
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns', padx=(0, 12), pady=8)
        
        # 绑定滚动事件
        self.platforms_frame.bind('<Configure>', 
                                 lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        
        # 绑定鼠标滚轮事件
        self.canvas.bind_all('<MouseWheel>', self._on_mousewheel)
        self.canvas.bind_all('<Button-4>', self._on_mousewheel_linux)
        self.canvas.bind_all('<Button-5>', self._on_mousewheel_linux)
        
        # 状态栏
        self.status_label = tk.Label(main_container, 
                                    text="就绪 - 输入问题后点击\"一键搜索\"",
                                    font=('Arial', 9),
                                    bg=COLORS['bg'], fg=COLORS['text_secondary'])
        self.status_label.grid(row=4, column=0, sticky='ew', pady=(8, 0))
        
        # 刷新列表
        self.refresh_platforms_list()
        
        # 加载上次输入
        self.load_last_query()
    
    def _on_mousewheel(self, event):
        """Windows鼠标滚轮事件"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def _on_mousewheel_linux(self, event):
        """Linux鼠标滚轮事件"""
        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")
    
    def get_enabled_count(self):
        """获取启用的平台数量"""
        return sum(1 for p in self.platforms if p.get('enabled', True))
    
    def refresh_platforms_list(self):
        """刷新平台列表 - 从self.platforms读取当前状态"""
        # 清除旧的项目
        for widget in self.platforms_frame.winfo_children():
            widget.destroy()
        
        for i, platform in enumerate(self.platforms):
            # 创建行
            row = tk.Frame(self.platforms_frame, bg=COLORS['card'])
            row.pack(fill='x', pady=1)
            
            # 从platform读取当前的enabled状态
            is_enabled = platform.get('enabled', True)
            
            # 复选框 - 使用IntVar(0/1)来跟踪状态
            var = tk.IntVar(value=1 if is_enabled else 0)
            chk = tk.Checkbutton(row, variable=var, bg=COLORS['card'])
            chk.pack(side='left', padx=(3, 6))

            # 使用trace_add监听变量变化
            var.trace_add('write', lambda *args, idx=i, v=var: self.on_checkbox_changed(idx, v))
            
            # 类型标签（AI/搜索）
            type_color = '#34c759' if platform.get('type') == 'ai' else '#0071e3'
            type_text = 'AI' if platform.get('type') == 'ai' else '搜索'
            type_label = tk.Label(row, text=type_text, font=('Arial', 8, 'bold'),
                                bg=type_color, fg='white', width=5)
            type_label.pack(side='left', padx=(0, 8))
            
            # 平台名称
            name_label = tk.Label(row, text=platform['name'], font=('Arial', 10, 'bold'),
                                bg=COLORS['card'], fg=COLORS['text'], width=15, 
                                anchor='w')
            name_label.pack(side='left', padx=(0, 8))
            
            # 描述
            desc = platform.get('description', '')
            desc_label = tk.Label(row, text=desc, font=('Arial', 9),
                                bg=COLORS['card'], fg=COLORS['text_secondary'], 
                                anchor='w')
            desc_label.pack(side='left', fill='x', expand=True)
            
            # URL预览
            url_text = platform['url'][:25] + '...' if len(platform['url']) > 25 else platform['url']
            url_label = tk.Label(row, text=url_text, font=('Arial', 8),
                               bg=COLORS['card'], fg='#999999', anchor='e')
            url_label.pack(side='right', padx=(8, 4))
            
            # 分隔线
            if i < len(self.platforms) - 1:
                line = tk.Frame(self.platforms_frame, bg='#e8e8ed', height=1)
                line.pack(fill='x', padx=8, pady=1)
        
        # 更新Canvas的滚动区域
        self.platforms_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
        
        # 更新统计
        enabled_count = self.get_enabled_count()
        self.stats_label.config(text=f"已启用 {enabled_count} 个平台")
    
    def on_checkbox_changed(self, index, var):
        """复选框状态改变时的回调"""
        # 获取当前勾选状态 (IntVar返回0或1，需要转换为bool)
        is_checked = bool(var.get())

        # 更新platforms数据
        self.platforms[index]['enabled'] = is_checked
        
        # 立即保存到JSON文件
        self.save_config()
        
        # 更新统计显示
        enabled_count = self.get_enabled_count()
        self.stats_label.config(text=f"已启用 {enabled_count} 个平台")
        
        # 显示状态提示
        status_text = "启用" if is_checked else "禁用"
        platform_name = self.platforms[index]['name']
        self.set_status(f"已{status_text} {platform_name}")
    

    
    def search_all(self):
        """一键搜索所有选中的平台"""
        query = self.query_text.get('1.0', 'end-1c').strip()
        if not query:
            messagebox.showwarning("提示", "请输入问题或关键词")
            return
        
        enabled_platforms = [p for p in self.platforms if p.get('enabled', True)]
        if not enabled_platforms:
            messagebox.showwarning("提示", "请至少启用一个平台")
            return
        
        # 复制到剪贴板（如果勾选了）
        if self.clipboard_var.get():
            try:
                self.root.clipboard_clear()
                self.root.clipboard_append(query)
                self.set_status("✓ 已复制到剪贴板，正在打开平台...")
            except Exception:
                self.set_status("⚠ 复制失败，正在打开平台...")
        
        # 保存输入
        self.save_last_query()
        
        success_count = 0
        
        for i, platform in enumerate(enabled_platforms):
            try:
                url_template = platform['url']
                
                # 替换URL中的占位符
                if '%query%' in url_template:
                    url = url_template.replace('%query%', quote(query))
                elif '%question%' in url_template:
                    url = url_template.replace('%question%', quote(query))
                elif '%poker%' in url_template:
                    url = url_template.replace('%poker%', quote(query))
                else:
                    url = url_template
                
                # 使用 webbrowser 打开
                if i == 0:
                    webbrowser.open(url, new=1)
                else:
                    webbrowser.open(url, new=2)
                
                success_count += 1
            except Exception:
                pass
        
        clipboard_status = "（已复制到剪贴板）" if self.clipboard_var.get() else ""
        self.set_status(f"✓ 已打开 {success_count} 个平台{clipboard_status}", COLORS['success'])
    
    def load_config(self):
        """加载配置 - 从JSON文件读取，如果不存在则使用默认配置"""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    platforms = config.get('platforms', [])
                    if platforms:
                        return platforms
            except Exception as e:
                print(f"读取配置文件失败: {e}")
        
        # 如果配置文件不存在或读取失败，使用内存中的默认配置（不创建文件）
        return DEFAULT_PLATFORMS.copy()
    
    def save_config(self):
        """保存配置到JSON文件"""
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump({'platforms': self.platforms}, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("错误", f"保存配置失败: {e}")
    
    def load_last_query(self):
        """加载上次输入"""
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    last_query = data.get('last_query', '')
                    self.query_text.insert('1.0', last_query)
            except:
                pass
    
    def save_last_query(self):
        """保存当前输入"""
        try:
            with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump({'last_query': self.query_text.get('1.0', 'end-1c')}, 
                         f, ensure_ascii=False)
        except:
            pass
    
    def clear_input(self):
        """清空输入"""
        self.query_text.delete('1.0', tk.END)
        self.save_last_query()
    
    def set_status(self, text, color=COLORS['text_secondary']):
        """设置状态栏"""
        self.status_label.config(text=text, fg=color)
        self.root.update()
    
    def add_platform(self):
        """添加平台"""
        dialog = PlatformDialog(self.root, "添加平台")
        if dialog.result:
            self.platforms.append({
                'id': f"platform_{len(self.platforms)}",
                'name': dialog.result['name'],
                'url': dialog.result['url'],
                'type': dialog.result['type'],
                'description': dialog.result.get('description', ''),
                'enabled': True
            })
            self.save_config()
            self.refresh_platforms_list()
    



class PlatformDialog:
    """平台对话框"""
    def __init__(self, parent, title, name='', url='', platform_type='search', description=''):
        self.result = None
        
        dialog = tk.Toplevel(parent)
        dialog.title(title)
        dialog.geometry("500x350")
        dialog.resizable(False, False)
        dialog.transient(parent)
        dialog.grab_set()
        dialog.configure(bg=COLORS['bg'])
        
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (350 // 2)
        dialog.geometry(f'+{x}+{y}')
        
        frame = tk.Frame(dialog, bg=COLORS['bg'])
        frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # 平台名称
        tk.Label(frame, text="平台名称", font=('Arial', 11, 'bold'),
                bg=COLORS['bg'], fg=COLORS['text']).pack(anchor='w', pady=(0, 5))
        name_var = tk.StringVar(value=name)
        tk.Entry(frame, textvariable=name_var, font=('Arial', 12),
                bg='white', relief='solid', bd=1).pack(fill='x', pady=(0, 12))
        
        # 平台类型
        tk.Label(frame, text="平台类型", font=('Arial', 11, 'bold'),
                bg=COLORS['bg'], fg=COLORS['text']).pack(anchor='w', pady=(0, 5))
        type_var = tk.StringVar(value=platform_type)
        type_frame = tk.Frame(frame, bg=COLORS['bg'])
        type_frame.pack(fill='x', pady=(0, 12))
        
        # 创建单选按钮
        search_radio = tk.Radiobutton(type_frame, text="搜索引擎", variable=type_var, 
                                     value='search', bg=COLORS['bg'], font=('Arial', 10))
        search_radio.pack(side='left', padx=(0, 20))
        ai_radio = tk.Radiobutton(type_frame, text="AI平台", variable=type_var, 
                                 value='ai', bg=COLORS['bg'], font=('Arial', 10))
        ai_radio.pack(side='left')
        
        # URL
        tk.Label(frame, text="URL 模板", font=('Arial', 11, 'bold'),
                bg=COLORS['bg'], fg=COLORS['text']).pack(anchor='w', pady=(0, 5))
        url_var = tk.StringVar(value=url)
        tk.Entry(frame, textvariable=url_var, font=('Arial', 12),
                bg='white', relief='solid', bd=1).pack(fill='x', pady=(0, 5))
        tk.Label(frame, text="使用 %query% 作为查询占位符\n例如：https://www.google.com/search?q=%query%",
                font=('Arial', 9), bg=COLORS['bg'], fg=COLORS['text_secondary'], 
                justify='left').pack(anchor='w', pady=(0, 12))
        
        # 描述
        tk.Label(frame, text="描述（可选）", font=('Arial', 11, 'bold'),
                bg=COLORS['bg'], fg=COLORS['text']).pack(anchor='w', pady=(0, 5))
        desc_var = tk.StringVar(value=description)
        tk.Entry(frame, textvariable=desc_var, font=('Arial', 12),
                bg='white', relief='solid', bd=1).pack(fill='x', pady=(0, 15))
        
        # 按钮
        btn_frame = tk.Frame(frame, bg=COLORS['bg'])
        btn_frame.pack(fill='x')
        
        def on_ok():
            name_val = name_var.get().strip()
            url_val = url_var.get().strip()
            type_val = type_var.get()
            
            if not name_val or not url_val:
                messagebox.showwarning("提示", "请填写完整信息", parent=dialog)
                return
            
            self.result = {
                'name': name_val,
                'url': url_val,
                'type': type_val,
                'description': desc_var.get().strip()
            }
            dialog.destroy()
        
        tk.Button(btn_frame, text="取消", font=('Arial', 11),
                 bg='#e8e8ed', relief='flat', bd=0, cursor='hand2',
                 padx=20, pady=6, command=dialog.destroy).pack(side='right', padx=(10, 0))
        
        tk.Button(btn_frame, text="确定", font=('Arial', 11, 'bold'),
                 bg=COLORS['primary'], fg='white', relief='flat', bd=0,
                 cursor='hand2', padx=20, pady=6, command=on_ok).pack(side='right')
        
        parent.wait_window(dialog)


def main():
    root = tk.Tk()
    app = UnifiedSearchApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
