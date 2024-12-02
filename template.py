def gettemplate(W, H, From="untitled1.py"):
    text = open(From, "r").read()
    text1 = text[:text.find("""<widget class="QWidget" name="Field" native="true">""")]
    text1 += f"""<widget class="QWidget" name="Field" native="true">
      <property name="geometry">
       <rect>
        <x>20</x>
        <y>240</y>
        <width>{W * 40}</width>
        <height>{H * 40}</height>
       </rect>
      </property>"""
    for i in range(W):
        for j in range(H):
            b = f"""
      <widget class="QPushButton" name="B{i}B{j}">
       <property name="geometry">
        <rect>
         <x>{40 * i}</x>
         <y>{40 * j}</y>
         <width>35</width>
         <height>35</height>
        </rect>
       </property>
       <property name="text">
        <string>.</string>
       </property>
      </widget>"""
            text1 += b
    text1 += """
     </widget>
    </widget>
   </item>
  </layout>
 </widget>
 <resources/>
 <connections/>
</ui>
"""
    return (text1)
