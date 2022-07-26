from panda3d.core import LVector3
from panda3d.core import GeomVertexFormat, GeomVertexData
from panda3d.core import Geom, GeomTriangles, GeomVertexWriter,GeomTristrips
from utils_geom import *


from PIL import Image, ImageDraw, ImageFont

font = ImageFont.truetype("font/Arial.ttf", size=40)

# You can't normalize inline so this is a helper function
def normalized(*args):
    myVec = LVector3(*args)
    myVec.normalize()
    return myVec



# generate a surface with given vertexs and color
def makeQuad(x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4, color_value,origin,mode):

    format = GeomVertexFormat.getV3n3c4t2()
    vdata = GeomVertexData('square', format, Geom.UHStatic)
    color = GeomVertexWriter(vdata, 'color')
    vertex = GeomVertexWriter(vdata, 'vertex')
    normal = GeomVertexWriter(vdata, 'normal')
    texcoord = GeomVertexWriter(vdata, 'texcoord')

    [a,b,c] = solve_normal_with_three_point([x1, y1, z1], [x2, y2, z2], [x3, y3, z3])


    vertex.addData3(x1-origin[0], y1-origin[1], z1-origin[2])
    vertex.addData3(x2-origin[0], y2-origin[1], z2-origin[2])
    vertex.addData3(x3-origin[0], y3-origin[1], z3-origin[2])
    vertex.addData3(x4-origin[0], y4-origin[1], z4-origin[2])

    normal.addData3(normalized(a,b,c))
    normal.addData3(normalized(a,b,c))
    normal.addData3(normalized(a,b,c))
    normal.addData3(normalized(a,b,c))
    '''

    normal.addData3(normalized(0,0,1))
    normal.addData3(normalized(0,0,1))
    normal.addData3(normalized(0,0,1))
    normal.addData3(normalized(0,0,1))
    '''

    if mode==0:
        for color_v in color_value:
            color.addData4(abs(color_v[0]), abs(color_v[1]), abs(color_v[2]), 0.5)
    elif mode==1:
        color.addData4(abs(color_value[0]), abs(color_value[1]), abs(color_value[2]),0.5)
        color.addData4(abs(color_value[0]), abs(color_value[1]), abs(color_value[2]), 0.5)
        color.addData4(abs(color_value[0]), abs(color_value[1]), abs(color_value[2]), 0.5)
        color.addData4(abs(color_value[0]), abs(color_value[1]), abs(color_value[2]), 0.5)

    texcoord.addData2f(0, 0)
    texcoord.addData2f(0, 1)
    texcoord.addData2f(1, 0)
    texcoord.addData2f(1, 1)

    tris = GeomTristrips(Geom.UHDynamic)
    tris.addVertices(0,1,2,3)

    # store the generated Geom function
    square = Geom(vdata)
    square.addPrimitive(tris)
    return square


def draw_text_texture(message, width, height, font, color_value):

    img = Image.new('RGB', (width, height), color=(int(255*abs(color_value[0])), int(255*abs(color_value[1])), int(255*abs(color_value[2]))))

    imgDraw = ImageDraw.Draw(img)

    r = imgDraw.textbbox((0,0),message, font = font)
    textWidth = r[2] - r[0]
    textHeight = r[3] - r[1]

    new_width = int(1.2*textWidth)
    new_height = int(1.2*textWidth*width/height)

    img = Image.new('RGB', (new_width, new_height), color=(int(255*abs(color_value[0])), int(255*abs(color_value[1])), int(255*abs(color_value[2]))))

    imgDraw = ImageDraw.Draw(img)

    imgDraw.text(((new_width-textWidth)/2, (new_height-textHeight)/2), message, fill=(100,100,100),font = font)

    img.save("texture/"+message+'.png')
