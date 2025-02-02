## **DEVELOPMENT** Zaptec charger custom component for home assistant

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]][license]

[![hacs][hacsbadge]][hacs]
[![Project Maintenance][maintenance-shield]][user_profile]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]


# Features

* Integration for Home assistant for Zaptec Chargers through the Zaptec
  cloud API
* Provides start & stop of charging the EV
* Supports basic (native authentication)
* Sensors and status, current, energy
* Adjustable charging currents

To use this component, a user with access to
[Zaptec Portal](https://portal.zaptec.com/) is needed.

Confirmed to work with

* Zaptec Go

> *) Send a message to @sveinse if you have been able to use any other chargers
in order to put it on the list.


## :warning: Development version

**:information_source: IMPORTANT!** This is https://github.com/sveinse/zaptec
which is @sveinse fork of upstream/official zaptec integration at
https://github.com/custom-components/zaptec.
This is under active development, and any feedback on your experience using it
is very appreciated.

**:warning:  WARNING!** This is a major refactor of the upstream zaptec
integration. The names and device setup has been significantly refactored.
Installing this version will break your existing automations and templates.


## Beta testing

The component is currently under beta testing. Any feedback on problems,
improvements or joy can be given at: https://github.com/sveinse/zaptec/issues

In particular the following items is of particular interest:

* Is everything working as it should? Any error messages?
* Does your autpmations and operation of the charger work with your use?
* Any missing entities (sensors, buttons, switches)?
* Are the new entity names ok?
* What is missing from documentation?

In some cases it would help debugging to have access to the diagnostics info.
Please see the "Diagnostics" section below in how to generate if it is requested.


## What's new in this Beta

The zaptec integration has been completely refactored and the way to interact
with it in Home Assistant has changed. The zaptec data is now represented as
proper entities (like sensors, numbers, buttons, etc). This makes logging and
interactions much simpler and it needs no additional templates.

The integration is set up as one devices for each of the detected Zaptec
devices. Most users will have three devices: An installation device, a circuit
and a charger and each provide different functionality.

The previous zaptec entities were named `zaptec_charger_<uuid>`,
`zaptec_installation_<uuid>` and `zaptec_circute_<uuid>`. The full data were
available as attributes in these objects, and they could be retried with
the aid of manual templates. The same objects exists, but under the names
`<name> Installer`, `<name> Charger` and `<name> Circuit`.


# Installation

This repo can be installed manually into Home Assistant by manually adding the
URL in HACS.

**:information_source: NOTE!** Existing `zaptec` installations MUST be
uninstalled first. Installing this repo will clash with existing integration
already installed.

### Step 1
![Setup1](/img/hacs_custom.png)

### Step 2
![Setup2](/img/hacs_zaptec_custom.png)

### Step 3
![Setup3](/img/hacs_zaptec_dev.png)


# Usage

## Zaptec device concept

The Zaptec cloud API use three levels of abstractions in their EVCP setup. These are
represented as three devices in HA

* **Installation** - This is the top-level entity and represents the entire
  site. This is where the current limit for the entire installation is set.

* **Circuit** - An installation can have one or more (electrical) circuits. One
  circuit have one common circuit breaker. This device isn't directly used in
  HA.

* **Charger** - This is the actual EV charge point connected to a circuit. Each
  circuit might have more than one charger. This is where the start & stop
  interaction is done and information about the charging and sessions.


## Start & stop charging

Starting and stopping charging can be done by several methods. If the charger
is configured to no require authentication, connecting the charger to the
EV will by default start charging.

To start the charging from HA, this can be done in several ways:

- Press the _"Resume charging"_ button, or
- Toggle the _"Charging"_ switch, or
- Send `zaptec.restart_charger` service call

Similarly, pausing the charging can be done by:

- Pressing the _"Stop charging"_ button, or
- Turn off the _"Charging"_ switch, or
- Send `zaptec.stop_pause_charging` service call

**:information_source: NOTE:** Zaptec will unlocks the cable when charging
is paused unless it is permanently locked.


## Prevent charging auto start

Zaptec will by default start charging as soon as everything is ready
under the following conditions; (1) Cable connected to car, (2) Car is ready to
charge, (3) authentication is given (optional).

If auto start is not wanted, e.g. for delayed start or energy control, one
of the following will prevent auto start:

* Delay authorization of the charger
* Set the available charge current to `0 A`. There are two ways to do it
   * _"Available current"_ in the installation object
   * _"Charger max current"_ in the charger object

**:information_source: NOTE!** The _"Available current"_ is the official
way to control the charge current. However, it will affect __all__ chargers
connected to the installation.


## Setting charging current

The _"Available current"_ number entity in the installation device will set
the maximum current the EV can use. This slider will set all 3 phases at
the same time.

**:information_source: NOTE!** This entity is adjusting the available current
for the entire installation. If the installation has several chargers installed,
changing this value will affect all.

**:information_source: NOTE!** Many EVs doesn't like getting too frequent
changes to the available charge current. Zaptec recommends not changing the
values more often than 15 minutes.

#### 3 phase current adjustment

The service call `limit_current` can be used with the arguments
`available_current_phase1`, `available_current_phase2` and
`available_current_phase3` to set the available current on individual phases.


## Require charging authorization

Many users wants to setup their charger to require authorization before giving
power to charge any EV. This integration does not offer any options to configure
authorization. Please use the official
[Zaptec portal](https://portal.zaptec.com/) or app.

If the charger has been setup with authorization required, the car will go
into _Waiting_ mode when the cable is inserted. Authentication must be
presented before being able to charge. This can be RFID tags, the Zaptec app
and more.

If the installation is configured for _native authentication_ it is possible
to authorize charging from Home Assistant using the _"Authorize charging"_
button. It stays authorized until either the cable is removed or the button
_"Deauthorize charging"_ is pressed.

**:information_source: INFO:** Please note that Zaptec unlocks the cable when
charging is paused unless it is permanently locked.


## Templates

The special diagnostics entities named _"x Installation"_, _"x Circuit"_ and
_"x Charger"_ contains all attributes from the Zaptec API for each of these
devices. This corresponds to the old `zaptec_installation_*`, `zaptec_circuit_*`
and `zaptec_charger_*` objects. These attributes can be used with template
sensors to retrieve additional or missing information.

Example: Add the following to your `configuration.yaml`

```yaml
template:
  - sensor:
     - name: Charger Humidity
       unique_id: charger_humidity
       unit_of_measurement: '%Humidity'
       state: >
        {{ state_attr('binary_sensor.X_charger', 'humidity') | round(0) }}
      # Replace "X_charger" with actual entity name
```

The list of attributes can be found by looking at the attributes for the
entities. Note that the names cannot contain spaces. Replace captal letters
with small case and spaces with underscore (_). E.g. The attribute
_"Charger max current"_ is `charger_max_current` in the template.


## Diagnostics

The integration supports downloading of diagnostics data. This can be reached
by `Settings -> Devices & Services -> <one of your zaptec devices>` and then
press the "Download diagnostics". The file downloaded is anonymized and should
not contain any personal information. Please double check that the file
doesn't contain any personal information before sharing.


[zaptec]: https://github.com/custom-components/zaptec
[buymecoffee]: https://www.buymeacoffee.com/hellowlol1
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/custom-components/zaptec.svg?style=for-the-badge
[commits]: https://github.com/custom-components/zaptec/commits/master
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Default-blue.svg?style=for-the-badge
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[exampleimg]: example.png
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license]: https://github.com/custom-components/zaptec/blob/master/LICENSE
[license-shield]: https://img.shields.io/github/license/custom-components/zaptec.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Hellowlol-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/custom-components/zaptec.svg?style=for-the-badge
[releases]: https://github.com/custom-components/zaptec/releases
[user_profile]: https://github.com/hellowlol
