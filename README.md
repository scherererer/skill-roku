To submit your skill, replace this file with text from 
https://rawgit.com/MycroftAI/mycroft-skills/master/meta_editor.html


## Roku
Interfaces with roku

## Description 
This is a mycroft skill for controlling your roku. It uses the Roku External Control API found here: https://sdkdocs.roku.com/display/sdkdoc/External+Control+API

When you ask your mycroft to play a show, this skill will do a search at the "roku" level for the show. If it finds what you are looking for on the correct provider (e.g. netflix, amazon, etc.) then it will launch it automatically. If it doesn't, you'll end up with some search results on your screen.

## Installation

In order for this skill to discover your roku on the network, you will need to poke some holes in your firewall. If you have a mark 1, then skip to the instructions in the next subsection. This skill uses the ephemeral port range (typically 32768-60999 on linux machines) over UDP to bind to. You'll need to open up this range of ports.

### Mark 1
If you have a mark 1, ssh into the unit (typically with `ssh pi@mark1.local`), and then run the following command:

```bash
sudo ufw allow proto udp from any port 1900 to any port 32768:61000
```

## Examples 
* "Show altered carbon on netflix"

## Testing
Tested using a Roku 3.

## Credits 
Michael P. Scherer
