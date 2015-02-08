EnOcean - Still under development.

  
Configure plugin.conf 
=
  
Add the following lines to your plugin.conf and just adapt the serial port to your port name of your enocean-adpater.
A udev-rules for the enocean-adapter is recommend. The specification of the enocean tx_id is optional but mandatory for sending control commands from the stick to a device. When controlling multiple devices, it is recommended to use the stick's BaseID (not ChipID) as transmitting ID. 
For further information regarding the difference between BaseID and ChipID, see https://www.enocean.com/en/knowledge-base-doku/enoceansystemspecification:issue:what_is_a_base_id/
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
Then use one of the following commands:
<pre>
	sh.enocean.send_learn_telegram(ID_Offset=0, Rorg=0, Func=0, Type=0, Manufactur_ID =0, variation=3), generic command for all Rorgs and variations
	sh.enocean.send_learn_dim(ID_Offset), ready to use command for dimmers
	sh.enocean.send_learn_switch(ID_Offset), ready to use command for switches, e.g. Eltako FSR61G-230V, etc.
</pre>
depending on whether to lern in a dimmer or switch as they have different teach in messages. In this case ID_Offset is within the range (0-127) and specifies the sending ID offset with respect to the BaseID. Later, the ID offset is specified in the item.conf for every outgoing send command, see example below.
Use different ID offsets for different groups of actors.
That's it!
  
Configure items
=
  
 The following example is for a rocker/switch with two rocker and 6 available combinations (EEP F6_02_02).  
left rocker down = A1  
left rocker up = A0  
right rocker down = B1   
right rocker up = B0  
both rockers up = A1B1  
both rockers down = A0B0  
  
  
The following example is for a rocker/switch with two rocker and 6 available combinations (EEP F6_02_03).  
left rocker down = A1  
left rocker up = A0  
right rocker down = B1   
right rocker up = B0  
last state of left rocker = A  
last state of right rocker = B  

Mechanical handle example:
handle_status = STATUS

The following example is for a rocker/switch with two rocker and 6 available combinations (EEP A5_20_01).  

value_in_percent = VALUE
service = SERVICE
replace_battery = BATTERY
temperature = TEMPERATURE

Example item.conf
=
<pre>
[Enocean]
	[[HeatingActor1]]
		enocean_rx_id = 01234567
		enocean_rx_eep = A5_20_01
		[[[valve]]]
			type = num
			enocean_rx_key = VALUE
			visu_acl = ro
		[[[battery]]]
			type = bool
			enocean_rx_key = BATTERY
			visu_acl = ro
		[[[is_temperature]]]
			type = num
			enocean_rx_key = TEMPERATURE
			visu_acl = ro
	[[Door]]
		enocean_rx_id = 01234567
		enocean_rx_eep = D5_00_01
		[[[status]]]
			type = bool
			enocean_rx_key = STATUS
			visu_acl = ro
			cache = True
			enforce_updates = true
	[[FT55switch]]
		enocean_rx_id = 012345AA
		enocean_rx_eep = F6_02_03
        	[[[up]]]
			type = bool
           		enocean_rx_key = B0
        		visu_acl = ro
        		enforce_updates = true
    		[[[down]]]
        		type = bool
        		enocean_rx_key = B1
        		visu_acl = ro   
        		enforce_updates = true
	[[dimmer1]]
		enocean_rx_id = 00112233
		enocean_rx_eep = A5_11_04
		enforce_updates = true
		[[[light]]]
			type = bool
			enocean_rx_key = STAT
			visu_acl = rw
			enforce_updates = true
			enocean_tx_eep = A5_38_08_02
			enocean_tx_id_offset = 1
			[[[[level]]]]
				type = num
				value = -1
				enocean_rx_key = D
				visu_acl = rw
				enforce_updates = true
				enocean_tx_eep = A5_38_08_03
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
  	[[actor1B]]
    		enocean_rx_id = FFAABBCD
    		enocean_rx_eep = F6_02_03
    		enforce_updates = true
    		[[[light]]]
        		type = bool
        		enocean_rx_key = B
        		visu_acl = rw   
        		enforce_updates = true
        		enocean_tx_eep = A5_38_08_01
        		enocean_tx_id_offset = 2

</pre> 
	
Add new listening enocean devices
=
  
You have to know about the EnOcean RORG of your device, so pleas ask Mr.Google or the vendor. Further the RORG must be declared in the plugin. The following EEPs are supported:

F6_02_02	2-Button-Rocker

F6_02_03	2-Button-Rocker, Status feedback from manual buttons on different actors, e.g. Eltako FT55, FSUD-230, FSVA-230V, FSR61G-230V or Gira switches.

F6_10_00	Mechanical Handle  

A5_11_04	Dimmer status feedback

A5_12_01	Power Measurement

A5_20_01	4BS Telegram, HVAC component, Battery powered device, for example Alpha Eos
		
D5_00_01	Door/Window Contact, e.g. Eltako FTK, FTKB

Send commands: Tx EEPs
=

A5_38_08_01	Regular switch actor command (on/off), e.g. Eltako FSR61G-230V

A5_38_08_02	Dimmer command with fix on off command (on: 100, off:0)

A5_38_08_03	Dimmer command with specified dim level (0-100)


