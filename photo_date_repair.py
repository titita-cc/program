# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 19:36:35 2023

@author: 46526
"""

import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image
import piexif
from datetime import datetime, timedelta
import pandas as pd
original_date=""
corrected_date=""
df = pd.DataFrame([], columns = ['文件名' , '原日期', '已修正日期'])
wrong_date = datetime(2013, 6, 28)  
right_date= datetime(2023, 3, 30)
date_shijiancha=(right_date-wrong_date).days #默认日期偏差为3564天
folder_path=""
def modify_date():
    global corrected_date,original_date,date_shijiancha,folder_path
    entry0.config(state=tk.NORMAL)
    # 选择文件夹
    folder_path = filedialog.askdirectory()
    print(folder_path)
    file1=(os.listdir(folder_path)[0])    
    if file1.endswith(('jpg','JPG','jpeg','bmp')):
        file_path = os.path.join(folder_path, file1)
        #print(file_path)
        file_path=file_path.replace('\\', '\\\\')
        file_path=file_path.replace(r'/', r'\\')
        # 打开图片
        image = Image.open(file_path)
        exif_data = piexif.load(image.info['exif'])
        if exif_data is not None:
            original_date = exif_data['Exif'][piexif.ExifIFD.DateTimeOriginal].decode('utf-8')
            string=str(original_date)[:11].replace(":","/")
            lb_filename.config(text=file_path)
            lb_filename.grid()
            entry0.delete(0, tk.END) #清空文字
            entry0.insert(tk.END, string)  # 框中插入文字
            entry0.config(state=tk.DISABLED)
            
            # 计算正确的拍摄日期
            corrected_date = datetime.strptime(original_date, "%Y:%m:%d %H:%M:%S") + timedelta(days=date_shijiancha)
            #print('修正日期：',corrected_date)
            # 将修正后的拍摄日期转换为字符串
            new_date = corrected_date.strftime("%Y:%m:%d %H:%M:%S")
            
            string=str(new_date[:11]).replace(":","/")
            entry1.delete(0, tk.END) #清空文字
            entry1.insert(tk.END, string)  # 框中插入文字
            entry1.grid()
    button2["state"] = tk.NORMAL #设置按钮可用
def xiugai():
    global corrected_date,original_date,df 
    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        #print(filename)
        if filename.endswith(('jpg','JPG','jpeg','bmp')):
            file_path = os.path.join(folder_path, filename) #图片x=文件夹路径+图片名x
            #print(file_path)
            file_path=file_path.replace('\\', '\\\\')
            file_path=file_path.replace(r'/', r'\\')
            #print(file_path)
            # 打开图片
            image = Image.open(file_path) #打开图片
            #image.show()
            exif_data = piexif.load(image.info['exif']) #获取图片信息
            #print("33333",exif_data)
            # 获取当前的拍摄日期
            if exif_data is not None:
                original_date = exif_data['Exif'][piexif.ExifIFD.DateTimeOriginal].decode('utf-8') # 获取错误的拍摄日期
                #print('原日期：',original_date)
                date1=datetime(int(original_date[:4]), int(original_date[5:7]), int(original_date[8:10]))
                date2=entry1.get()
                date2=datetime(int(date2[:4]), int(date2[5:7]), int(date2[8:10]))
                date_shijiancha=(date2-date1).days  
                #print(date_shijiancha)
                # 计算正确的拍摄日期
                corrected_date = datetime.strptime(original_date, "%Y:%m:%d %H:%M:%S") + timedelta(days=date_shijiancha)
                #print('修正日期：',corrected_date)
                # 将修正后的拍摄日期转换为字符串
                new_date = corrected_date.strftime("%Y:%m:%d %H:%M:%S")

                # 修改拍摄日期
                exif_data['Exif'][piexif.ExifIFD.DateTimeOriginal] = new_date.encode('utf-8')
                
                # 保存修改后的图片
                exif_bytes = piexif.dump(exif_data)
                image.save(file_path, exif = exif_bytes)
                
                df=df.append({"文件名":filename,"原日期":original_date,"已修正日期":corrected_date}, ignore_index=True)
                
    tk.messagebox.showinfo("完成", "拍摄日期修改完成！")
    print(df)
    button2["state"] = tk.DISABLED #设置按钮不可用
    
# 创建主窗口
root = tk.Tk()
root.title("批量修改照片拍摄日期")

# 创建按钮
button = tk.Button(root, text="选择文件夹", command=modify_date)
button.grid(row=0,column=0,columnspan=3)

#文件名称标签
lb_filename=tk.Label(root,text="")  
lb_filename.grid(row=1,column=0,columnspan=3,sticky='w')

#原日期标签
lb=tk.Label(root,text='原日期：')
lb.grid(row=2,column=0,sticky='w')
#原日期文本框
entry0=tk.Entry(root)
entry0.grid(row=2,column=1,sticky='w')

#"修改为"标签
lb3=tk.Label(root,text="修改为：")
lb3.grid(row=3,column=0,sticky='w')

#日期修改文本输入框
entry1=tk.Entry(root)
entry1.grid(row=3,column=1,sticky='w')

#日期修改按钮
button2 = tk.Button(root, text="开始修正", command=xiugai)
button2.grid(row=3,column=2,sticky='w')
button2["state"] = tk.DISABLED #设置按钮不可用

# 运行主循环
root.mainloop()