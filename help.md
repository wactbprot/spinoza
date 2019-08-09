

@spinoza
--------

**interacts with the servers (redis, relay, ssmp, couchdb) at localhost**


@spinoza knows the following direct commands
--------------------------------------------

* I'll *observe* or *watch* redis keys periodically if you command: **observe key** e.g. @spinoza observe info@0 or  @spinoza watch raw_result@2
* To list all the keys available use: **all** or **list** e.g. @spinoza list or @spinoza all
* *Get* or *show* the value behind the key by : **get** or **show** e.g. @spinoza show raw_result@2 or @spinoza get info@0
* To list all keys at an line use: **line n** e.g. @spinoza line 2
* Try @spinoza who (or .sw)

@spinoza listens to the the following commands
--------------------------------------------
* .sh or .s?: help
* .st: observe current target pressure
* .si: observe info 
* .so: stop all observing
* .sv: state of the se3 valves
* .ss: state of the se3 servo motors
* .sp: pressure of the se3 group normal cdgs

:robot: 
    