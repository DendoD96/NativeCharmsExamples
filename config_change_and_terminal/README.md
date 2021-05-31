# Config change and terminal 
This example mainly shows how to react to configuration changes and execute terminal commands. The example is taken from the code in this [repo](https://github.com/charmed-osm/srs-enb-ue-operator).

As suggested in this [issue](https://github.com/canonical/operator/issues/189), the ConfigChanged event doesn't provide any information on what has changed. This example assumes that this information is of no interest. If not you can refer to [this example](https://github.com/DendoD96/NativeCharmsExamples/tree/main/config_change_awarness) for a possible solution.
 
