from PySide2 import QtWidgets
import hou

class FontDemo(QtWidgets.QWidget):
    
    def __init__(self, parent=None):

        user = hou.hscriptExpression('$USER')

        # Check if user has nodes selected.
        try:
            selected_node = hou.selectedNodes()[0]
            if not selected_node.type().category() == hou.ropNodeTypeCategory():
               raise
        except:
            mssg = "Please select a OUT node to continue"
            hou.ui.displayMessage(mssg, severity=hou.severityType.Error)
            quit()
            
        
        QtWidgets.QWidget.__init__(self, parent)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowStaysOnTopHint)
        
        layout = QtWidgets.QVBoxLayout(self)
        grpBox = QtWidgets.QGroupBox("Pisciniqui tools")
        
        hbox = QtWidgets.QHBoxLayout()
        vbox = QtWidgets.QVBoxLayout()
        low = QtWidgets.QVBoxLayout()

        self.resize(500, 140)
        self.setMaximumHeight(140)
        self.setMinimumHeight(140)
        
        self.setWindowTitle('Updator')
        
        self.label = QtWidgets.QLabel('Select one of the folowing options:', self)

        self.setLayout(hbox)

        self.button = QtWidgets.QPushButton('Updates Cahes', self)
        self.button.setFocusPolicy(QtCore.Qt.NoFocus)

        
        self.chechbox = QtWidgets.QCheckBox('Save Houdini File', self)

        hbox.addWidget(self.button)
        
        self.button2 = QtWidgets.QPushButton('Save and Increment', self)
        self.button2.setFocusPolicy(QtCore.Qt.NoFocus)
        
        hbox.addWidget(self.button2)
        vbox.addWidget(self.chechbox)
        
        low.addWidget(self.label)
        low.addLayout(hbox)
        low.addLayout(vbox)
        
        grpBox.setLayout(low)
        
        layout.addWidget(grpBox)
        
        self.button.clicked.connect(self.UpdateCaches)
        self.button2.clicked.connect(self.SaveIncrement)

    def UpdateCaches(self):
        nodes = hou.selectedNodes()
        for node in nodes:            
            node_type = node.type().nameComponents()[2]    
            
            hip_name = hou.hipFile.path()
            hn_list = hip_name.split(".")
            length = len(hn_list)
            last_s = hn_list[length - 1]
            
            tmp_str = hn_list[length-3]
            
            subindex = -1
            if 'v' not in tmp_str:
                subindex = tmp_str
                tmp_str = hn_list[length-4]
                
            #    Adjusting the cache version according to the hip file version
            name = node.name()
            path = ''
            parameter = ''
            
            if(node_type == 'arnold'):
                parameter = node.parm("ar_picture")
                path = node.parm("ar_picture").unexpandedString()
            if(node_type == 'ifd'):
                parameter = node.parm("vm_picture")
                path = node.parm("vm_picture").unexpandedString() 
            
            #   Formating the base path, in case is not setted-up
            shot = hou.hscriptExpression('$SHOT')
            layer = hou.hscriptExpression('$LAYER')
            discipline = hou.hscriptExpression('$DISCIPLINE')
            element = hou.hscriptExpression('$ELEMENT')
            
            if (element != ''):
                element =  '.' + hou.hscriptExpression('$ELEMENT') + '.'  
                
            user = hou.hscriptExpression('$USER')
            cache_path = '$JOB/render/' + shot + '/' + layer + element[:-1] + '/' + tmp_str + '/' + shot + '.' + layer + element + discipline + '.$OS.' + tmp_str + '.' + user + '.$F4.exr'
            
            if subindex == -1:
                cache_path = '$JOB/render/' + shot + '/' + layer + element[:-1] + '/' + tmp_str + '/' + shot + '.' + layer + element + discipline + '.$OS.' + tmp_str + '.1.' + user + '.$F4.exr'
            else:
                i_subindex = int(subindex)
                cache_path = '$JOB/render/' + shot + '/' + layer + element[:-1] + '/' + tmp_str + '/' + shot + '.' + layer + element + discipline + '.$OS.' + tmp_str + '.' + str(i_subindex) + '.' + user + '.$F4.exr'
            
            parameter.set(cache_path)
            
            # Updating deep path
            b_deep = node.parm('vm_deepresolver').eval()
            
            if b_deep == 'camera':
                deep_cache_path = '$JOB/render/' + shot + '/' + layer + element[:-1] + '/' + tmp_str + '/' + shot + '.' + layer + element + discipline + '.`$OS`_deep.' + tmp_str + '.' + user + '.$F4.exr'
                
                if subindex == -1:
                    deep_cache_path = '$JOB/render/' + shot + '/' + layer + element[:-1] + '/' + tmp_str + '/' + shot + '.' + layer + element + discipline + '.`$OS`_deep.' + tmp_str + '.1.' + user + '.$F4.exr'
                else:
                    i_subindex = int(subindex)
                    deep_cache_path = '$JOB/render/' + shot + '/' + layer + element[:-1] + '/' + tmp_str + '/' + shot + '.' + layer + element + discipline + '.`$OS`_deep.' + tmp_str + '.' + str(i_subindex) + '.' + user + '.$F4.exr'
                
                node.parm('vm_dcmfilename').set(deep_cache_path)
                
    def SaveIncrement(self):
        nodes = hou.selectedNodes()
        for node in nodes:
        
            node_type = node.type().nameComponents()[2]    
            
            hip_name = hou.hipFile.path()
            hn_list = hip_name.split(".")
            length = len(hn_list)
            last_s = hn_list[length - 1]
            
            tmp_str = hn_list[length-3]
            
            subindex = -1
            if 'v' not in tmp_str:
                subindex = tmp_str
                tmp_str = hn_list[length-4]
                
            #    Formating the new hip file
            split1 = hip_name.split(tmp_str)
            new_hf = split1[0] + tmp_str 
            if subindex == -1:
                new_hf = new_hf + '.'  + '1'  +  split1[1]
            else:
                i_subindex = int(subindex) + 1
                new_hf = new_hf + '.' + str(i_subindex) + '.' + hn_list[length-2] + '.' + hn_list[length-1]  
            
        #    Adjusting the cache version according to the hip file version
            name = node.name()
            path = ''
            parameter = ''
            
            if(node_type == 'arnold'):
                parameter = node.parm("ar_picture")
                path = node.parm("ar_picture").unexpandedString()
            if(node_type == 'ifd'):
                parameter = node.parm("vm_picture")
                path = node.parm("vm_picture").unexpandedString() 
            
           #   Formating the base path, in case is not setted-up
            shot = hou.hscriptExpression('$SHOT')
            layer = hou.hscriptExpression('$LAYER')
            discipline = hou.hscriptExpression('$DISCIPLINE')
            element = hou.hscriptExpression('$ELEMENT')
            if (element != ''):
                element =  '.' + hou.hscriptExpression('$ELEMENT') + '.'              
            user = hou.hscriptExpression('$USER')
            
            cache_path = '$JOB/render/' + shot + '/' + layer + element[:-1] + '/' + tmp_str + '/' + shot + '.' + layer + element + discipline + '.$OS.' + tmp_str + '.' + user + '.$F4.exr'
            if subindex == -1:
                cache_path = '$JOB/render/' + shot + '/' + layer + element[:-1] + '/' + tmp_str + '/' + shot + '.' + layer + element + discipline + '.$OS.' + tmp_str + '.1.' + user + '.$F4.exr'
            else:
                i_subindex = int(subindex) + 1
                cache_path = '$JOB/render/' + shot + '/' + layer + element[:-1] + '/' + tmp_str + '/' + shot + '.' + layer + element + discipline + '.$OS.' + tmp_str + '.' + str(i_subindex) + '.' + user + '.$F4.exr'
            
            parameter.set(cache_path)

            # Updating deep path
            b_deep = node.parm('vm_deepresolver').eval()
            if b_deep == 'camera':
                deep_cache_path = '$JOB/render/' + shot + '/' + layer + element[:-1] + '/' + tmp_str + '/' + shot + '.' + layer + element + discipline + '.`$OS`_deep.' + tmp_str + '.' + user + '.$F4.exr'
                if subindex == -1:
                    deep_cache_path = '$JOB/render/' + shot + '/' + layer + element[:-1] + '/' + tmp_str + '/' + shot + '.' + layer + element + discipline + '.`$OS`_deep.' + tmp_str + '.1.' + user + '.$F4.exr'
                else:
                    i_subindex = int(subindex) + 1
                    deep_cache_path = '$JOB/render/' + shot + '/' + layer + element[:-1] + '/' + tmp_str + '/' + shot + '.' + layer + element + discipline + '.`$OS`_deep.' + tmp_str + '.' + str(i_subindex) + '.' + user + '.$F4.exr'
                node.parm('vm_dcmfilename').set(deep_cache_path)
            
        if(self.chechbox.isChecked()):
            hou.hipFile.save(new_hf)
            
    def test(self):
    def culo(self):
        if self.chechbox.isChecked():
            print("checked")
        else:
            print("no checked")
            
            
dialog = FontDemo()


