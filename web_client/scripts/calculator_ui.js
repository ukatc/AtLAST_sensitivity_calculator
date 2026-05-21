import { setInstrument } from './rest_calls.js';

const setUIInitialState = (paramData) => {
    // Set all inputs to a valid state
    const allUserInput = document.querySelectorAll(".param-input");
    allUserInput.forEach(input => {
        input.setCustomValidity("");
    });

    // Hide all the invalid messages
    hideInvalidMessages(true);

    // Enable the Calculate button
    disableCalculateBtn(false);

    // Show the Sensitivity input and hide the Integration time input
    const sensitivityInput = document.getElementById("row-sensitivity");
    sensitivityInput.classList.remove("d-none");
    const intTimeInput = document.getElementById("row-t-int");
    intTimeInput.classList.add("d-none");
}

const hideInvalidMessages = (hidden) => {
    const allInvalidMessages =
        document.querySelectorAll(".invalid-message");
    allInvalidMessages.forEach(input => {
        input.hidden = hidden;
    });
}

const handleInstrumentSelection = (e) => {
    const selectedInstrument = e.target.value;
        
    // Send the selected instrument to the backend to set it as the chosen_instrument
    setChosenInstrument(selectedInstrument);
}

const setChosenInstrument = async (instrumentName) => {
    try {
        const data = await setInstrument(instrumentName);
        console.log(data);
    } catch (error) {
        console.error("Error setting instrument:", error);
        // Optionally display error message to user
        alert(`Failed to set instrument: ${error.message}`);
    }
}

const showDifferentInstrumentOptions = (dropdown_choice) => {
    const instrument_name = document.getElementById(dropdown_choice);
    instrument_name.addEventListener("change", handleInstrumentSelection);
}
    
const disableCalculateBtn = (disable) => {
    const calculateBtn = document.getElementById("calculate");
    calculateBtn.disabled = disable;
}

const showCalculatedValue = (value, unit) => {
    const outputBox = document.querySelector("#output");

    // Set the calculated state
    outputBox.classList.add("calculated");

    // Convert the value to a float and round to 4 decimal places
    const roundedVal = (+value).toFixed(4);
    outputBox.innerHTML = `${roundedVal} ${unit}`;
}

const resetOutputBox = () => {
    const outputBox = document.querySelector("#output");
    outputBox.classList.remove("calculated");
    outputBox.innerHTML = "";
}

const initializeInputs = () => {
    // Set up the user input field for all parameters
    const allUserInput = document.querySelectorAll(".param-input");

    allUserInput.forEach(input => {
        // Add the placeholder text
        input.setAttribute("placeholder", "Enter a value...");

        // Make the input required
        input.required = true;
    });

    // TODO Initialize the number of polarizations
}

const initializeUnits = (paramData) => {
    // Set up all the dropdowns with units
    const allUnitsInput = document.querySelectorAll('.units-input');

    allUnitsInput.forEach(input => {
        // Get the parameter data corresponding to the current input
        const paramName = input.id.replace('-units', '');
        // Get the permitted units for this parameter
        const allowedUnits = paramData[paramName]['units'];
        // Get the default unit for this parameters
        const defaultUnit = paramData[paramName]['default_unit']

        // Add an option for each allowed unit and select the default
        allowedUnits.forEach(unit => {
            const option = document.createElement('option');
            option.setAttribute('value', unit);
            option.innerHTML = unit;

            if (unit === defaultUnit) {
                option.setAttribute('selected', 'selected');
            }
            input.appendChild(option);
        });
    });
}

const toggleSpinner = (action, completed) => {
    if (completed) {
        document.getElementById(`${action}-spinner`)
                .classList.add("d-none");
        document.getElementById(`${action}`).classList.remove("d-none");
    } else {
        document.getElementById(`${action}-spinner`)
                .classList.remove("d-none");
        document.getElementById(`${action}`).classList.add("d-none");
    }
}

export {setUIInitialState, hideInvalidMessages, showDifferentInstrumentOptions,
        showCalculatedValue, disableCalculateBtn, initializeInputs, 
        initializeUnits, resetOutputBox, toggleSpinner}
