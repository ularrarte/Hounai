import hou, math

def conversor():
    nodes = hou.selectedNodes()


    for node in nodes:

        node_type = node.type().nameComponents()[2]

        if node_type != 'arnold_light':
            mssg = "Please select one Arnold light to continue"
            hou.ui.displayMessage(mssg, severity=hou.severityType.Error)
            quit()
    
        
        # Function the get parameters from the Arnold Node
        
        def getKeyframes():
            kfms = {}
            parameters = node.parms()
            for p in parameters:
                kfm = node.parm(p.name()).keyframes()
                if p.isTimeDependent():
                    kfms[p.name()] = kfm
            return kfms
                    
        
        def getTras():
            tx = node.parm('tx').eval()
            ty = node.parm('ty').eval()
            tz = node.parm('tz').eval()
            trans = [tx, ty, tz] 
            return trans
            
        def getRot():
            rx = node.parm('rx').eval()
            ry = node.parm('ry').eval()
            rz = node.parm('rz').eval()
            rot = [rx, ry, rz] 
            return rot
            
        def getColor():
            cr = node.parm('ar_colorr').eval()
            cg = node.parm('ar_colorg').eval()
            cb = node.parm('ar_colorb').eval()
            color = [cr, cg, cb]
            return color
            

        def createLight(type, position):
            position[0] = position[0] + 2.5
            if type == 6:
                m_node = dest.createNode('envlight', node_name)
                m_node.setPosition(position)
            else:
                m_node = dest.createNode('hlight::2.0', node_name)
                m_node.setPosition(position)
            return m_node
            
        
        # Functions to set the parameters for the mantra light

        def setTras(trs):
            m_node.parm('tx').set(trs[0])
            m_node.parm('ty').set(trs[1])
            m_node.parm('tz').set(trs[2])
            
        def setRot(rot):
            m_node.parm('rx').set(rot[0])
            m_node.parm('ry').set(rot[1])
            m_node.parm('rz').set(rot[2])
            
        def setKeyframes(keys):
        
            ##Create a dictionary for each correspondant Arnold-Mantra parameters
            dict = {}
            dict['ar_intensity'] = 'light_intensity'
            dict['ar_exposure'] = 'light_exposure'
            dict['ar_spread'] = 'None'
            
            dict['tx'] = 'tx'
            dict['ty'] = 'ty'
            dict['tz'] = 'tz'
            
            dict['rx'] = 'rx'
            dict['ry'] = 'ry'
            dict['rz'] = 'rz'      
            
            
            for parm, keys in keys.items():
                m_parm = dict.get(parm)
                if m_parm != None:
                    print(m_parm)
                    m_node.parm(m_parm).setKeyframes(keys)
                    
                    
        def setColor(color):
            m_node.parm('light_colorr').set(color[0])
            m_node.parm('light_colorg').set(color[1])
            m_node.parm('light_colorb').set(color[2])
            
        
        
        
        def setType(type, trs, m_node):

            # Type 0 in Arnold (Point) is type 0 in Mantra (Point)
            # Type 1 in Arnold (Distant) is type 7 in Mantra
            # Type 2 in Arnold (Spot) is type 3 in Mantra
            # Type 3 in Arnold (Quad) is type 2 in Mantra
            # Type 4 in Arnold (Disk) is type 3 in Mantra 
            # Type 5 in Arnold (Cylinder) is type 5 in Mantra (Tube)
            # Type 6 in Arnold (Skydome) is envlight in Mantra
            
            mantra_types = [0, 7, 3, 2, 3, 5, -1]
            
            # If is not Skydome Light, we set the type of mantra light using the mantra_types array
            if type != 6:
                m_node.parm('light_type').set(mantra_types[type])
            elif type == 0:
                # Setting the parameters that are for this kinf od light
                print('Punto')
            elif type == 1:
                # Setting the parameters that are for this kinf od light
                print('Distant')
            elif type == 2:
                ## SPOT LIGHT
                m_node.parm('coneenable').set(1)
                c_angle = node.parm('ar_cone_angle').eval()
                m_node.parm('coneangle').set(c_angle)
                
                # Set spot light radius
                s_rad = node.parm('ar_spot_radius').eval()
                m_node.parm('areasize1').set(s_rad)
                m_node.parm('areasize2').set(s_rad)
                
                # Extra settings to match Mantra Light
                m_node.parm('light_conefov').set(1)            
                m_node.parm('conedelta').set(0)            

            elif type == 3:
                ## QUAD LIGHT

                # Set the grid scale
                quad_x = node.parm('ar_quad_sizex').eval()
                quad_y = node.parm('ar_quad_sizey').eval()
                m_node.parm('areasize1').set(quad_x)
                m_node.parm('areasize2').set(quad_y)
            elif type == 4:
                # DISK/CONE LIGHT

                # Set radius scale for the cone
                disk_r = node.parm('ar_disk_radius').eval()
                # In mantra we set the perimeter, not the radius
                m_node.parm('areasize1').set(disk_r * 2)
                m_node.parm('areasize2').set(disk_r * 2)
            elif type == 5:
                # CYLINDER/TUBE LIGHT

                # Get tube rad. and height from the arnold node
                tube_r = node.parm('ar_cylinder_radius').eval()
                tube_h = node.parm('ar_height').eval()
                # Setting the parameters for the new light
                m_node.parm('areasize1').set(tube_h)
                m_node.parm('areasize2').set(tube_r * 13)
                # We also need to rotate de light 90 in Z axis to match the orientation
                rot[2] = rot[2] + 90
                setRot(rot)
            elif type == 6:
                # SKYDOME/ENVIRONMENTAL LIGHT

                # Checking the color type for this node
                texture = node.parm('ar_light_color_type').eval()
                # If there is a texture, we copy that path to our mantra node
                if texture == 1:
                    path_exr = node.parm('ar_light_color_texture').eval()
                    m_node.parm('env_map').set(path_exr)
                # We can also the color type to 'shader', so we need to dive into the node to find the path.
                if texture == 2:
                    mat_node = hou.node(node.parm('ar_light_color_shader').eval())
                    mat_node = node.node('shopnet').node('arnold_vopnet').node('image1').parm('filename').eval()
                    m_node.parm('env_map').set(mat_node)
                    
                    # In order to match the initial rotation, we need to rotate it 180
                    m_node.parm('ry').set(m_node.parm('ry').eval() + 180)
            
            
        
        def setIntExp(int, exp, type):        
            
            
            total_int = int * pow(2, exp)
            m_node.parm('light_intensity').set(int)
            
            # Using the type that we used to set the light type.
            if type == 0:
                # int * pow(2, exp) = total_int
                # pow(2, exp) = total_int/int
                r_side = (total_int/int)/6
                exposure = (math.log(r_side))/(math.log(2))
                m_node.parm('light_exposure').set(exposure)
            if type == 1:
                # int * pow(2, exp) = total_int
                # pow(2, exp) = total_int/int
                r_side = (total_int/int)/6
                exposure = (math.log(r_side))/(math.log(2))
                m_node.parm('light_exposure').set(exposure)
            if type == 2:
                # int * pow(2, exp) = total_int
                # pow(2, exp) = total_int/int
                r_side = (total_int/int)/6
                exposure = (math.log(r_side))/(math.log(2))
                m_node.parm('light_exposure').set(exposure)
            if type == 3:
                # int * pow(2, exp) = total_int
                # pow(2, exp) = total_int/int
                r_side = (total_int/int)/6        
                exposure = (math.log(r_side))/(math.log(2))
                exposure = exposure + ( 1 - node.parm('ar_spread').eval())
                int = int + int/node.parm('ar_spread').eval()
                
                m_node.parm('light_exposure').set(exposure)
                m_node.parm('light_intensity').set(int)
                m_node.parm('normalizearea').set(0)
            if type == 4:
                # int * pow(2, exp) = total_int
                # pow(2, exp) = total_int/int
                r_side = (total_int/int)/3
                exposure = (math.log(r_side))/(math.log(2))
                
                exposure = exposure + ( 1 - node.parm('ar_spread').eval())
                int = int + int/node.parm('ar_spread').eval()
                
                m_node.parm('light_exposure').set(exposure)
                
            if type == 5:
                # int * pow(2, exp) = total_int
                # pow(2, exp) = total_int/int
                r_side = (total_int/int)/10
                exposure = (math.log(r_side))/(math.log(2))
                m_node.parm('light_exposure').set(exposure)

            if type == 6:
                m_node.parm('light_exposure').set(exp)
                    
            
                
        # Get the type of Arnold light    
        light_type = node.parm('ar_light_type').eval()        
        # Get node name
        node_name = node.name()    
        # Get the location of the current node
        dest = node.path()
        # Splitting the path using the name of the node
        dest_array = dest.split(node_name)
        dest = dest_array[0][:-1]
        dest = hou.node(dest)
        # Create the new name
        node_name = node_name  + '_mantra'
        
        # Get source intensity and exposure
        int = node.parm('ar_intensity').eval()
        exp = node.parm('ar_exposure').eval()
        # Get trs, rot and color of the node
        trs = getTras()
        rot = getRot()
        color = getColor()
        
        # Checking time dependant parameters, and storing the keyframes
        keyframes = getKeyframes()
        
        # Position of the Arnold node
        position = node.position()
        
        # Creating the light using the type and the position
        m_node = createLight(light_type, position)
        # Set trasnlation and rotation of the mantra node
        setTras(trs)
        setRot(rot)
        # Set the color of the mantra node
        setColor(color)
        # In case that we have some keyframed parameters, we copy the animation
        setKeyframes(keyframes)
        # Set the type of light of the mantra node
        setType(light_type, trs, m_node)    
        # Set the intensity and exposure
        setIntExp(int, exp, light_type)