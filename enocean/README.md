EnOcean - under development !!!

Please do not remove any comments until stable.
  
Configure plugin.conf 
=
  
Add the following lines to your plugin.conf and just change the serialport to the portname of your enocean-adpater.
A udev-rules for the enocean-adapter is recommend. The specification of the enocean tx_id is optional but mandatory for sending control commands from the stick to a device. When controlling multiple devices, it is recommended to use the stick's BaseID (not ChipID) as transmitting ID. 
For further information regarding the difference between BaseID and ChipId, see https://www.enocean.com/en/knowledge-base-doku/enoceansystemspecification:issue:what_is_a_base_id/
With the specification of the BaseID, 128 different transmit IDs are available, ranging between BaseID and BaseID + 127.
  
<pre>
[enocean]
    class_name = EnOcean
    class_path = plugins.enocean
    serialport = /dev/ttyUSB0
    tx_id      = FFFF_4680
</pre>


Learning Mode:
For some enocean devices it is important to teach in the enocean stick first. In order to send a special learning message, start smarthome with the interactive console: ./smarthome.py -i
Then use the following command:
<pre>
	sh.enocean.send_learn(ID_Offset)
</pre>
, where ID_Offset, range (0-127), specifies the sending ID offset with respect to the BaseID. Later, the ID offset is specified in the item.conf for every outgoing send command, see example below.
Use different ID offsets for different groups of actors.
That's it!
  
Configure items
=
  
According to the plugin-implementation of the enocean-devices you have to specify at least a enocean-id (enocean serial number in format 01:a2:f3:2d), the correct enocean-rorg-code and an enocean-value. 
   
The following example ist for a rocker/switch with two rocker and 6 available combinations.  
left rocker down = A1  
left rocker up = A0  
right rocker down = B1   
right rocker up = B0  
both rockers down = A1B1   
both rockers up = A0B0   

Mechnical handle example:
handle_status = STATUS


<pre>
[A1]
type = bool
enforce_updates = true
enocean_id = 00:22:60:37
enocean_rorg = F6_02_02
enocean_value = A1
</pre>

Example item.conf
=
<pre>
	[[dimmer1]]
		enocean_rx_id = 00112233
		enocean_rx_eep = A5_11_04
		enforce_updates = true
		[[[light]]]
			type = bool
			enocean_rx_key = STAT
			visu_acl = rw
			enforce_updates = true
			enocean_tx_eep = A5_38_08
			enocean_tx_id_offset = 1
			[[[[level]]]]
				type = num
				value = -1
				enocean_rx_key = D
				visu_acl = rw
				enforce_updates = true
				enocean_tx_eep = A5_38_08
				enocean_tx_id_offset = 1
				ref_level = 80
	[[handle]]
		enocean_rx_id = 01234567
		enocean_rx_eep = F6_10_00
		[[[status]]]
			type = num
			enocean_rx_key = STATUS
			visu_acl = ro
			cache = True
			enforce_updates = true

  	[[actor1]]
    		enocean_rx_id = FFAABBCC
    		enocean_rx_eep = A5_12_01
    		enforce_updates = true
    		[[[power]]]
        		type = num
        		value = -1
        		enocean_rx_key = VALUE
        		enforce_updates = true
        		visu_acl = ro  
  	[[actor12]]
    		enocean_rx_id = FFAABBCD
    		enocean_rx_eep = F6_02_03
    		enforce_updates = true
    		[[[light]]]
        		type = bool
        		enocean_rx_key = B
        		visu_acl = rw   
        		enforce_updates = true
        		enocean_tx_eep = A5_38_08
        		enocean_tx_id_offset = 2

</pre> 
	
Add new listening enocean devices
=
  
You have to know about the EnOcean RORG of your device, so pleas ask Mr.Google or the vendor. Further the RORG must be declared in the plugin. The following EEPs are supported:

F6_02_02	2-Button-Rocker
F6_02_03	2-Button-Rocker, Status feedback from manual buttons on different actors.
F6_10_00	Mechanical Handle  

A5_11_04	Dimmer status feedback
A5_12_01	Power Measurement
A5_38_08	to do...
