# Linux connected devices search
Looks whole networks your Linux machine is connected too.<br>
For each network which is not local (127.x.x.x) make a default getway out of your IP & for length for subnet mask.<br>
Will run whole class subnet even if it's lower:<br>
/28 will still do /24.<br>
There is not knowing if the IP pool for smaller subnet start from, so there is need to look for the full subnet mask.<br>
Pings each ip posible for that default gateway & subnet, if other side answer for the ping request saves the ip as found device.
