# Native charms basic examples (OSM rel 9.1)
As suggested in title this repo contains some basic examples about use of native charms for day1 and day2 configurations.

## Juju charm in OSM Overview 
A “charm” is a generic set of scripts for deploying and operating software which can be adapted to any use case.
There are two kinds of Charms:
 * Native charms
 * Proxy charms 

The structure of native charms is the same of proxy charms the difference is that in the first the set of scripts run inside the VNF components, in the set of scripts run in LXC containers in an OSM-managed machine (which could be where OSM resides), which use ssh or other methods to get into the VNF instances and configure them.
As suggest in [Day 1: VNF Services Initialization](https://osm.etsi.org/docs/vnf-onboarding-guidelines/03-day1.html) to decide which to use you need to consider the nature of your workload. This repo will only take care of native charms, the basic documentation about proxy charms is contained at previous link and some examples are available at [OSM packages gitlab](https://osm.etsi.org/gitlab/vnf-onboarding/osm-packages/-/tree/master).

## Native charm in OSM development
This section introduce the basic steps necessary in order to create a native charm for VDU/VNF. A pragmatic approach is used, without repeating theoretical concepts contained in  [Day 1: VNF Services Initialization](https://osm.etsi.org/docs/vnf-onboarding-guidelines/03-day1.html).

### Adding Day-1 primitives to the descriptor
``` yaml
vnfd:
...
    df:
    - ...
    # VNF/VDU Configuration must use the ID of the VNF/VDU to be configured
    lcm-operations-configuration:
      operate-vnf-op-config:
        day1-2:
        -  id: vnf_id
           execution-environment-list:
           - id: configure-vnf
             connection-point-ref: vnf-mgmt
             juju:
               charm: samplecharm
              config-primitive:
              - name: action1 
                execution-environment-ref: env
                parameter:
                -     name: param1
                      data-type: STRING
                      default-value: 'Param'
                -     name: param2
                      data-type: INTEGER
                      default-value: 1
              - ...
              initial-config-primitive:
              - name: action1 
                execution-environment-ref: env
                parameter:
                -     name: param1
                      data-type: STRING
                      default-value: 'Param'
                -     name: param2
                      data-type: INTEGER
                      default-value: 1
                seq: 1  
              - name: action2
                execution-environment-ref: env
                seq: 2 
              - ...                
```
**What is the difference between `initial-config-primitive` and `config-primitive`?**\
The first one is used to specify Day-1 configuration (**NOTE:** you have to specify actions order `seq` primitive), the second one is used to specify actions for Day-2 that will be available on-demand (i.e they can be called while the network functions are running).
### Create the charm 
```bash
sudo snap install charmcraft
mkdir samplecharm; cd samplecharm
charmcraft init
```
Edit the `metadata.yaml` file: 
```yaml
name: samplecharm
summary: this is an example
maintainer: Daniele Rossi <daniele.rossi27@unibo.com>
description: |
  This is an example of a proxy charm deployed by Open Source Mano.
tags:
  # tags list: https://jujucharms.com/docs/stable/authors-charm-metadata
  - network
  - openstack
subordinate: false
series:
  - bionic
  - xenial
# provides:
#   provides-relation:
#     interface: interface-name
# requires:
#   requires-relation:
#     interface: interface-name
# peers:
#   peer-relation:
#     interface: interface-name
```
As suggested by last lines of the file, charms can be related to each other. Additional informations about relations can be found at this [link](http://osm-download.etsi.org/ftp/osm-8.0-eight/OSM10-hackfest/presentations/OSM%2310%20Hackfest%20-%20HD2.4%20Intro%20to%20Juju%20relations.pdf).

Edit the `config.yaml` file:
```yaml
options:
  config-param-1:
    type: string
    description: |
      This is a string config param
    default: ""
  config-param-2:
    type: int
    description: |
      This is an int config param
    default: 1
```
If no configuration parameters are required insert `options: {}`

Edit the `actions.yaml` file:
```yaml
action1:
  description: action1 is an action
  params:
    param1:
      description: param1 is a param
      type: string
      default: "Param"
    param2:
      description: param2 is a param
      type: integer
      default: 1
action2:
  description: action1 is an action      
```
**NOTE:** this file contains the same actions and params of the descriptor file. Actions will be implemented in `charm.py`.

Edit the `charm.py` file:
```python
#!/usr/bin/env python3

import logging

from ops.charm import CharmBase
from ops.framework import StoredState
from ops.main import main
from ops.model import ActiveStatus

logger = logging.getLogger(__name__)

class SamplecharmCharm(CharmBase):
    # A class used to store data the charm needs persisted across invocations.
    _stored = StoredState()

    def __init__(self, *args):
        super().__init__(*args)
        
        # Sets an attribute in _stored and initialize it
        self._stored.set_default(things=[])
    
        # Listen to charm hooks
        self.framework.observe(self.on.config_changed, self.on_config_changed)
        self.framework.observe(self.on.install, self.on_install)
        self.framework.observe(self.on.start, self.on_start)
        
        # Listen to the action events
        self.framework.observe(self.on.action1_action, self.on_action1)
        self.framework.observe(self.on.action2_action, self.on_action2)
        
    def on_config_changed(self, event):
        """Handle changes in configuration"""
        self.model.unit.status = ActiveStatus()

    def on_install(self, event):
        """Called when the charm is being installed"""
        self.model.unit.status = ActiveStatus()
        
    def on_start(self, event):
        """Called when the charm is being started"""
        self.model.unit.status = ActiveStatus()
        
    def on_action1(self, event):
        """Action1 body."""
        
    def on_action2(self, event):
        """Action2 body."""

if __name__ == "__main__":
    main(SamplecharmCharm)

```
The whole list of charm hooks and when they are invoked can be found at this [link](https://discourse.charmhub.io/t/charm-hooks/1040)

The full API of Canonical operator framework are available at this [link](https://ops.readthedocs.io/en/latest/).

**NOTE:** registration for action events is done via: `self.framework.observe(self.on.<action_name>_action, self.<method_name>)`

Once the charm has been implemented, you can run the `charmcraft build` command in the base directory. Copy the contents of the `build` folder generated by the command into `<vnf_package>/charms/samplecharm`. 

### Troubleshooting
 * Check that the top of the `charm.py` contains **#!/usr/bin/env python3**.
 * Ensure that the hooks directory has symlinks to `charm.py` named **install**, **upgrade-charm** and **start**.
 * Check that `charm.py` is marked executable.

### Example execution
Each example contains a `build-charm.sh` script that is useful for building the charm. Once this is done you can run the commands:
```bash
osm package-build ./simple_native_charm_vnf/
osm package-build ./simple_native_charm_ns/
```
and proceed with onboarding.
#### Requirements
 * [OSM client](https://osm.etsi.org/docs/user-guide/10-osm-client-commands-reference.html#installing-standalone-osm-client)
 * [Charmcraft](https://github.com/canonical/charmcraft)
