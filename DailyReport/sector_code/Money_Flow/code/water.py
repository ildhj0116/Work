#-*- coding:utf-8 -*-

from PIL import Image, ImageDraw

def add_watermark_to_image(image, watermark):
	rgba_image = image.convert('RGB')
	rgba_watermark = watermark.convert('RGB')
 
	image_x, image_y = rgba_image.size
	watermark_x, watermark_y = rgba_watermark.size
 
	# 缩放图片
	scale = 10
	watermark_scale = max(image_x / (scale * watermark_x), image_y / (scale * watermark_y))
	new_size = (int(watermark_x * watermark_scale), int(watermark_y * watermark_scale))
	rgba_watermark = rgba_watermark.resize(new_size, resample = Image.ANTIALIAS)
	# 透明度
	rgba_watermark_mask = rgba_watermark.convert("L").point(lambda x: min(x+150, 180))
	rgba_watermark.putalpha(rgba_watermark_mask)
 
	watermark_x, watermark_y = rgba_watermark.size
	# 水印位置
	rgba_image.paste(rgba_watermark, (image_x - watermark_x*2, image_y - watermark_y), rgba_watermark_mask)
	return rgba_image
 

