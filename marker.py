#! /usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import os
import ast
try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    exit("This script requires the PIL module.\nInstall with pip install Pillow")

def watermark(filename, text, needID, needCredit, color, fontfamily, fontsize, opacity):
    image = Image.open(filename).convert('RGBA')

    if not needCredit and not needID:
        return image
    
    mark = Image.new('RGBA', image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(mark)
    width, height = image.size

    if fontsize is None:
        fontsize = int(height / 20)

    if height > width:
        fontsize = int(1.6 * fontsize)
    
    if text is None:
        text = u"Sample"
    
    font = ImageFont.truetype(fontfamily, fontsize)
    textWidth, textHeight = draw.textsize(text, font)
    margin = 75

    if needCredit:
        x = 0
        if height > width:
            x = (width - textWidth) / 2
        else:
            x = (width - textWidth) / 2   
        y = (height - textHeight) / 2
        draw.text((x, y), text, fill=color, font=font, encoding="utf-8")

    if needID:
        fileid = filename.split('_')[-1]
        x = 0
        if height > width:
            x = width - textWidth + int(5.5 * margin)
        else:
            x = width - textWidth + int(3.5 * margin)
        y = margin - textHeight
        draw.text((x, y), fileid[0:4], fill=color, font=font)

    print("watermarking " + filename)
    combined = Image.alpha_composite(image, mark).convert('RGB')
    return combined

def resize(filename, width, height, needResize):
    image = Image.open(filename)

    if not needResize:
        return image
    
    imageWidth, imageHeight = image.size
    
    if width is None and height is not None:
        imageWidth = (imageWidth * height) / imageHeight
        imageHeight = height
    elif width is not None and height is None:
        imageHeight = (imageHeight * width) / imageWidth
        imageWidth = width
    elif width is not None and height is not None:
        imageWidth = width
        imageHeight = width
    
    # print "(%i, %i)" % (imageWidth, imageHeight)
    # if width == imageWidth and height == imageHeight:
    #     print "image does not need to be resized"
    # else:
    #     print "resizing " + filename + "..."
    # print "(%i, %i)" % (imageWidth, imageHeight)
        
    print("resizing " + filename + "...")
    return image.resize((int(imageWidth), int(imageHeight)),
                        Image.ANTIALIAS)

def main():
    parser = argparse.ArgumentParser(description='Automates basic image manipulation.')
    parser.add_argument('-d', '--directory', nargs='?', default='.', help='A directory of images to process')
    parser.add_argument('-O', '--output-directory', help='The directory to place the processed images')
    parser.add_argument('-w', '--width', type=int, help='Resize the width of the image to <width>')
    parser.add_argument('--height', type=int, help='Resize the height of the images to <height>')
    parser.add_argument('-f', '--font-family', help='Sets the font family for the text watermark to <font family>')
    parser.add_argument('-s', '--font-size', type=int, help="Sets the font size of the text watermark to <font size>")
    parser.add_argument('-o', '--opacity', type=float, help="Sets the opacity of the watermark to <opacity>. This is a number between 0 and 1.")
    parser.add_argument('-c', '--color', type=ast.literal_eval, help="Sets the color of the text watermark to <color>. Expects the <color> in RGBA tuple format.")
    parser.add_argument('-t', '--text', help="Sets the watermark to <text>")
    parser.add_argument('--need-id', default='yes', help="yes if ID is needed, no otherwise")
    parser.add_argument('--need-credit', default='yes', help="yes if credit is needed, no otherwise")
    parser.add_argument('-r', '--need-resize', default='yes', help="yes if credit is needed, no otherwise")
    
    args = parser.parse_args()
    os.chdir(args.directory)
    output_dirname = args.output_directory
    
    if output_dirname is None:
        output_dirname = os.getcwd() + "_processed"
    if not os.path.isdir(output_dirname):
        cmd = "mkdir " + output_dirname
        os.system(cmd)

    needID = args.need_id == 'yes'
    needCredit = args.need_credit == 'yes'
    needResize = args.need_resize == 'yes'
    
    for filename in os.listdir(os.getcwd()):
        if filename.lower().endswith('.jpg'):

            fileid = filename.split('_')[1].split('.')[0]
            
            resized = resize(filename, args.width, args.height, needResize)
            resized.save(output_dirname + "/" + filename.split('.')[0] + "tv.jpg")
            
            watermarked = watermark(output_dirname + "/" + filename.split('.')[0] + "tv.jpg", args.text, needID, needCredit,
                                    args.color, args.font_family, args.font_size, args.opacity)
            watermarked.save(output_dirname + "/" + filename.split('.')[0] + "tv.jpg")

if __name__ == '__main__':
    main()
