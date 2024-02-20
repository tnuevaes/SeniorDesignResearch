#!/usr/bin/env python

# Usage: python MapToModel.py ./res/IMAGE.jpg ./obj/MODEL.obj

# noinspection PyUnresolvedReferences
import vtkmodules.vtkInteractionStyle
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkFiltersTexture import vtkTextureMapToSphere
from vtkmodules.vtkIOImage import vtkJPEGReader
from vtkmodules.vtkIOImage import vtkPNGReader
from vtkmodules.vtkIOGeometry import vtkOBJReader

from vtkmodules.vtkFiltersSources import (
    vtkCubeSource,
    vtkParametricFunctionSource,
    vtkTexturedSphereSource
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTexture
)


def get_program_parameters():
    import argparse
    description = 'Texture an object with an image.'
    epilogue = '''
   '''
    parser = argparse.ArgumentParser(description=description, epilog=epilogue,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('filename1', help='masonry-wide.jpg.')
    parser.add_argument('filename2', help='tshirt.obj')
    args = parser.parse_args()
    arg1 = args.filename1
    arg2 = args.filename2
    return arg1, arg2
    # takes in jpg file and obj file IN THAT ORDER

    

def main():
    colors = vtkNamedColors()
    
    jpegfile, objfile = get_program_parameters()
    
    #jpegfile = "./res/8k_earth_daymap.jpg"
    #objfile  = "./obj/tshirt.obj"
    
    # Create a render window
    ren = vtkRenderer()
    renWin = vtkRenderWindow()
    renWin.AddRenderer(ren)
    renWin.SetSize(480, 480)
    renWin.SetWindowName('Model Render')

    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    # Read the image data from a file
    reader = vtkJPEGReader()
    reader.SetFileName(jpegfile)
    
    # read the obj data from a file
    objreader = vtkOBJReader()
    objreader.SetFileName(objfile)

    # Create texture object
    texture = vtkTexture()
    texture.SetInputConnection(reader.GetOutputPort())

    # Map texture coordinates
    
    map_to_model = vtkTextureMapToSphere()
    map_to_model.SetInputConnection(objreader.GetOutputPort())
    map_to_model.PreventSeamOn()

    # Create mapper and set the mapped texture as input
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(map_to_model.GetOutputPort())

    # Create actor and set the mapper and the texture
    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.SetTexture(texture)

    ren.AddActor(actor)
    ren.SetBackground(colors.GetColor3d('Black'))

    iren.Initialize()
    renWin.Render()
    iren.Start()


if __name__ == '__main__':
    main()
