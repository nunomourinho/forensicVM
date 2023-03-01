vmconfig=`cat $1 | grep -v net0 | grep -v display | grep -v qxl | grep -v balloon | grep -v viosock`
extra_parameters="   -display vnc=0.0.0.0:0,websocket=5901 \\
    -chardev socket,id=mon0,host=localhost,port=4444,server=on,wait=off \\
    -mon chardev=mon0,mode=control,pretty=on \\
    -usb -device usb-tablet -device usb-kbd \\
    -vga virtio "

echo "$vmconfig
 $extra_parameters" >$2
chmod 700 $2
