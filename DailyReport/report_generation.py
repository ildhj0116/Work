# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 08:25:48 2018

@author: Administrator
"""


from docx import Document
from docx.oxml.ns import qn
from docx.shared import Pt
from docx.shared import Inches
#from PIL import Image



def Report_Generation(report_date,head_list,tail_list,image_name_list)

    title_dict = {1:report_date}
    head_rank_list = [12,16,20,25,31,42,45,49,52,56,59]
    tail_rank_list = [13,17,21,26,32,43,46,50,53,57,60]
    image_list = [14,18,22,27,33,34,38,44,47,51,54,58,61,65,67,73,74,75,76]
    
    head_rank_dict = dict(zip(head_rank_list,head_list))
    tail_rank_dict = dict(zip(tail_rank_list,tail_list))
    image_name_dict = dict(zip(image_list,image_name_list))
    
    document = Document("report.docx")
    counter = 0
    for p in document.paragraphs:
        counter += 1
        rrr = p.runs
        print p.text
        if counter == 1:
            p.text = u"2018-04-09量化日报"
            p.style.font.size = Pt(18)
            p.style.font.bold = True
        if counter == 14:
            r = p.runs[0]
            r.clear()
            r.add_picture(u'output/Daily/2018-04-09/品种日收益.jpg',width=Inches(7))
            
    
    
            
    document.styles['Normal'].font.name = u'楷体'
    document.styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), u'楷体')        
    document.save("report_tmp.docx")        
        
