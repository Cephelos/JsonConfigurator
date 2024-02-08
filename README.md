# JsonConfigurator
Minimal GUI for modifying JSON files, made specifically for Baldur's Gate 3 Mods
The executable *should* find your config files automatically if its in the normal spot, but otherwise you will be asked to direct it to the "Baldur's Gate 3" folder that contains your saves, mods, etc.

***If a mod author isn't using this for their mod's config stuff (and they probably aren't), don't bother them or me about it. This tool is primarily for my own use, it's only here in case anyone else wanted to use it.***

The JSON must fit a specific format for it to work (the text below is not valid JSON as it is commented; this same template without the comments is located in format.json)
If you split your mod config into multiple files, each one will show up as a seperate tab.
```javascript
{
    "BooleanFormat": {  // Template for boolean values, appears as a checkbox. This will be the name of the option in the GUI
        "description": "This is the display for boolean values.",  // Text that appears below the option to describe it
        "value": false,  // current value of the variable
        "default": false  // default value of the variable, used when hitting the reset button
    },
    "IntegerFormat": {  // Template for integer values, appears as an input box. This will be the name of the option in the GUI
        "description": "This is the display for integer values",  // Text that appears below the option to describe it
        "value": 41,  // current value of the variable
        "default": 60,  // default value of the variable, used when hitting the reset button
        "range": [  // ranges for this variable. "None" can be entered for min and max to leave the value unbounded. If set to "None", the step will be 1.
            1,  // minimum value
            100,  // maximum value
            1  // step of the value
        ],
        "extras": {  // optional values that can be added
            "slider": true  // adds a slider next to the input box; will be ignored if any value in "range" isn't an int
        }
    },
    "FloatFormat": {  // Template for float values, appears as an input box. This will be the name of the option in the GUI
        "description": "This is the display for float values",  // Text that appears below the option to describe it
        "value": 0.1,  // current value of the variable
        "default": 70.5,  // default value of the variable, used when hitting the reset button
        "range": [  // ranges for this variable. "None" can be entered for min and max to leave the value unbounded. If set to "None", the step will be 1.0  
            -1.5,  // minimum value
            1.5,  // maximum value
            0.1  // step of the value
        ],
        "extras": {  // optional values that can be added
            "precision": 2,  // number of digits after the decimal point to include. If not included, will default to the precision of tthe step
            "slider": true  // adds a slider next to the input box; will be ignored if any value in "range" isn't a float
        }
    },
    "ChoicesFormat": {  // Template for multiple-choice values, appears as radio buttons. This will be the name of the option in the GUI
        "description": "This is the display for multiple-choice options",  // Text that appears below the option to describe it
        "value": "choice 3",  // current value of the variable
        "choices": [  // choices that will each appear as a radio buttons
            "choice 1",
            "choice 2",
            "choice 3"
        ],
        "default": "choice 3"  // default value of the variable, used when hitting the reset button
    },
    "__CephelosModConfig": true  // if this line isn't present, the program will assume the json isn't the right format and ignore it
}
```

![Image of the GUI](/GUI.png)
