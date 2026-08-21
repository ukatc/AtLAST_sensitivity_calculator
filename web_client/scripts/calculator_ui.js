import { setInstrument, getInstrumentRanges, setApplicableInstruments } from './rest_calls.js';
import { validateInputAgainstInstrumentRange } from './validators.js';

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

    // Set the initial instrument ranges display
    const instrumentDropdown = document.getElementById("instrument-type");
    if (instrumentDropdown) {
        updateInstrumentRangesDisplay(instrumentDropdown.value);
    }

    // Show the applicable instruments given the current input values
    showApplicableInstruments();

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

const updateInstrumentRangesDisplay = async (instrumentName) => {
    try {
        const ranges = await getInstrumentRanges(instrumentName);
        const freqRangeDiv = document.getElementById("freq-range");
        const bwRangeDiv = document.getElementById("bw-range");
        const allowedSetupsTitle = document.getElementById("allowed-setups-title");

        if (allowedSetupsTitle) {
            allowedSetupsTitle.textContent = `${instrumentName} Allowed Setup`;
        }
        
        if (freqRangeDiv && ranges.freq_range) {
            freqRangeDiv.textContent = `${ranges.freq_range}`;
        }
        if (bwRangeDiv && ranges.bw_range) {
            bwRangeDiv.textContent = `${ranges.bw_range}`;
        }
    } catch (error) {
        console.error("Error fetching instrument ranges:", error);
    }
}

const handleInstrumentSelection = (e) => {
    const selectedInstrument = e.target.value;
    setChosenInstrument(selectedInstrument);
}

const showApplicableInstruments = async () => {
    const obsFreqInput = document.getElementById("obs-freq-input").value;
    const bandwInput = document.getElementById("bandwidth-input").value;
    const bandwUnit = document.getElementById("bandwidth-units").value;
    const inputData = {
        obs_freq: obsFreqInput,
        bandwidth: bandwInput,
        bandwidth_unit: bandwUnit
    };
    const applicableInstrumentsData = await setApplicableInstruments(inputData);
    const applicableInstrumentsDiv = document.getElementById("applicable-instruments");
    if (applicableInstrumentsDiv) {
        applicableInstrumentsDiv.textContent = `${applicableInstrumentsData}`;
    }
}

const validateCurrentInputsAgainstInstrument = (instrumentName) => {

    const instrumentRanges = document.getElementById("instrument-ranges-display");
    if (!instrumentRanges) {
        return;
    }

    const rangeFields = {
        obs_freq: document.getElementById("freq-range")?.textContent || "",
        bandwidth: document.getElementById("bw-range")?.textContent || ""
    };

    const inputsToValidate = [
        document.getElementById("obs-freq-input"),
        document.getElementById("bandwidth-input")
    ];

    const inputValuesInRange = inputsToValidate.map((input) => {
        const relevantRange = input.id === "obs-freq-input" ? rangeFields.obs_freq : rangeFields.bandwidth;
        const userSelectedUnit = input.id === "obs-freq-input" ? "GHz" : document.getElementById(`${input.name}-units`).value;
        return validateInputAgainstInstrumentRange(input, relevantRange, userSelectedUnit);
    });
    return inputValuesInRange;
}



const setChosenInstrument = async (instrumentName) => {
    try {
        const data = await setInstrument(instrumentName);
        console.log(data);
        // Update the ranges display for the new instrument
        await updateInstrumentRangesDisplay(data.instrument);
        // Validate current inputs against the newly set instrument
        const inputsInRange = validateCurrentInputsAgainstInstrument(instrumentName);

        if (inputsInRange === true) {
            disableCalculateBtn(false);
            resetOutputBox();
        } else {
            disableCalculateBtn(true);
        }   
        
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
        initializeUnits, resetOutputBox, toggleSpinner, validateCurrentInputsAgainstInstrument,
        showApplicableInstruments}
