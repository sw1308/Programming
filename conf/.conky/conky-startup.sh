sleep 0s
killall conky
cd "/home/sam/.conky/Gotham"
conky -c "/home/sam/.conky/Gotham/Gotham" &
cd "/home/sam/.conky/TeejeeTech"
conky -c "/home/sam/.conky/TeejeeTech/CPU Panel (4-core)" &
cd "/home/sam/.conky/TeejeeTech"
conky -c "/home/sam/.conky/TeejeeTech/Network Panel" &
cd "/home/sam/.conky/TeejeeTech"
conky -c "/home/sam/.conky/TeejeeTech/Process Panel" &
