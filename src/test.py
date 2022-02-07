from svg_to_gcode.svg_parser import parse_file
from svg_to_gcode.compiler import Compiler, interfaces
from laser_gcode_interface import LaserInterface

# Instantiate a compiler, specifying the interface type and the speed at which the tool should move. pass_depth controls
# how far down the tool moves after every pass. Set it to 0 if your machine does not support Z axis movement.
gcode_compiler = Compiler(LaserInterface, movement_speed=1000, cutting_speed=300, pass_depth=0,
                        laser_power= 0.5, laser_mode=True)

curves = parse_file("/Users/rodrigogodoy/Documents/dev/multiplegcodes/drawing.svg") # Parse an svg file into geometric curves
print(curves)
if len(curves):
    gcode_compiler.append_curves(curves) 
    gcode_compiler.compile_to_file("drawing.gcode", passes=2)