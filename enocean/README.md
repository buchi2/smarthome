EnOcean - under development !!!

Please do not remove any comments until stable.
  
Configure plugin.conf 
=
  
Add the following lines to your plugin.conf and just change the serialport to the portname of your enocean-adpater.
A udev-rules for the enocean-adapter is recommend. The specification of the enocean tx_id is optional when receiving only. However, tt is necessary for sending control commands from the stick to a device.
Additionally, the stick's enocean ID is read out during the plugin start and globally defined if not yet done so in the plugin.conf.
  
<pre>
[enocean]
    class_name = EnOcean
    class_path = plugins.enocean
    serialport = /dev/ttyUSB0
    tx_id      = 01B5FE80
</pre>


Learning Mode:
For some enocean devices it is important to teach in the enocean stick first. Therefore, the according device must be set to learning mode and a special learning message has to be sent from the stick. In order to trigger the special learning message, start smarthome with the interactive console: ./smarthome.py -i
Then use the following command: sh.enocean.send_learn(). The device will confirm the reception of the telegram and listen to that stick from now on.
That's it!
  
Configure items
=
  
According to the plugin-implementation of the enocean-devices you have to specify at least a enocean-id (enocean serial number in format 01:a2:f3:2d), the correct enocean-rorg-code and an enocean-value. 
The following list defines the enocean key values for use in the Item.conf:
   
Example is for a rocker/switch with two rocker and 6 available combinations:  
left rocker down = A1  				//For detection of the lower A switch button only
left rocker up = A0  
right rocker down = B1   
right rocker up = B0  
both rockers down = A1B1   
both rockers up = A0B0   
left rocker state = A				//For use as a classical on/off switch
right rocker state = B

Mechnical handle example:
handle_status = STATUS				//0= window closed, 1= window open, 2= window tilted

Dimmer exampler:
current dimmer value = D			//Dim value from 0-100(max)
current dimmer status = STAT		//0= off, 1 = on

Item.conf:

<pre>
[[dimmer]]
    enocean_rx_id = 00ABCDEF
    enocean_rx_eep = A5_11_04
    enforce_updates = true
    [[[light]]]
        type = bool
        enocean_rx_key = STAT
        visu_acl = rw   
        enforce_updates = true
        enocean_tx_eep = A5_38_08
        [[[[level]]]]
            type = num
            value = -1
            enocean_rx_key = D
            visu_acl = rw
            enforce_updates = true
            enocean_tx_eep = A5_38_08
            ref_level = 80				#optional: defines the dimmer value if light item is switched on. If not specified, maximum dim 100 is assumed.
[[switch]]
    enocean_rx_id = 10ABCDEF
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
[[handle]]
    enocean_rx_id = 0ACDBFFE
    enocean_rx_eep = F6_10_00
    [[[status]]]
        type = num
        enocean_rx_key = STATUS
        visu_acl = ro
        cache = True
        enforce_updates = true
</pre>
  
Add new enocean devices
=
  
You have to know about the EnOcean RORG of your device, so pleas ask Mr.Google or the vendor. Further the RORG must be declared in the plugin. The following EEPs are supported:

F6_02_02	2-Button-Rocker
F6_02_03	2-Button-Rocker
F6_10_00	Mechanical handle status 

A5_11_04	Dimmer status feedback
A5_3F_7F
A5_12_01	Status feedback from switch actors with power-merter.
A5_38_08	Dimmer feedback