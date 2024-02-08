# JsonConfigurator
Minimal GUI for modifying JSON files, made specifically for Baldur's Gate 3 Mods
The executable *should* find your config files automatically if its in the normal spot, but otherwise you will be asked to direct it to the "Baldur's Gate 3" folder that contains your saves, mods, etc.

***If a mod author isn't using this for their mod's config stuff (and they probably aren't), don't bother them or me about it. This tool is primarily for my own use, it's only here in case anyone else wanted to use it.***

The JSON must fit a specific format for it to work (the text below is not valid JSON as it is commented; this same template without the comments is located in format.json)

Each json will generate tabs named after each object at the highest level. That object's children will populate the tab.

Each mod folder will generate its own tab, which contains all of the tabs generated for that json. **Multiple json files within the same mod folder will break things.**
```javascript
{   "Templates" : {
        "BooleanTemplate": {  // Template for boolean values, appears as a checkbox. This will be the name of the option in the GUI
            "description": "This is the display for boolean values.",  // Text that appears below the option to describe it
            "value": false,  // current value of the variable
            "default": false  // default value of the variable, used when hitting the reset button
        },
        "IntegerTemplate": {  // Template for integer values, appears as an input box. This will be the name of the option in the GUI
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
        "FloatTemplate": {  // Template for float values, appears as an input box. This will be the name of the option in the GUI
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
        "ChoicesTemplate": {  // Template for multiple-choice values, appears as radio buttons. This will be the name of the option in the GUI
            "description": "This is the display for multiple-choice options",  // Text that appears below the option to describe it
            "value": "choice 3",  // current value of the variable
            "default": "choice 3"  // default value of the variable, used when hitting the reset button
            "choices": [  // choices that will each appear as a radio button
                "choice 1",
                "choice 2",
                "choice 3"
            ]
        },
        "MultipleChoicesTemplate": {    // Template for multiple-choice values (where you can select multiple), appears as checkboxes. This will be the name of the option in the GUI
            "description": "This is the display for multiple-choice options, where you can select any number of options",   // Text that appears below the option to describe it
            "value": [  // current values of the variable. Can be in any order
                "choice 3",
                "choice 2",
            ],
            "default": [  // default values of the variable, used when hitting the reset button. Can be in any order
                "choice 3",
                "choice 1",
            ],
            "choices": [  // choices that will each appear as a checkbox
                "choice 1",
                "choice 2",
                "choice 3"
            ]
        },
        "Placeholder1": {   // If you have more options than can fit on the normal screen size, a scroll bar will appear, allowing you to see everything
            "description": "This is just here to take up space, so I can show off the scroll bar.",
            "value": false,
            "default": false
        },
        "Placeholder2": {
            "description": "This is just here to take up space, so I can show off the scroll bar.",
            "value": false,
            "default": false
        },
        "Placeholder3": {
            "description": "This is just here to take up space, so I can show off the scroll bar.",
            "value": false,
            "default": false
        }
    }
    "Another Tab": {    // If there's multiple objects at the highest level of the json, it will form its own tab, with its own children objects displayed on it

    },
    "A Third Tab": {

    },
    "__CephelosModConfig": 2  // if this line isn't present, the program will assume the json isn't the right format and ignore it. The number isn't used in the GUI, but it can be used for versioning
}
```

![Image of the GUI](/GUI.png)
