import {geParamValuesUnits, calculate} from './rest_calls.js';
import {validateInput} from './validators.js'

$(document).ready(() => {

    let calculationPerformed = false;

    const setUIInitialState = (paramData) => {
        // Set all inputs to a valid state
        const allUserInput = document.querySelectorAll(".param-input");
        allUserInput.forEach(input => {
            input.setCustomValidity("");
        });

        // Hide all the invalid messages
        hideInvalidMessages(true);

        // Set the state of the Calculate button
        setCalculateBtnState();

        // Show the Sensitivity input and hide the Integration time input
        const sensitivityInput = document.getElementById("row-sensitivity");
        sensitivityInput.classList.remove("d-none");
        const intTimeInput = document.getElementById("row-t-int");
        intTimeInput.classList.add("d-none");

        doCalculation(paramData);
    }

    const hideInvalidMessages = (hidden) => {
        const allInvalidMessages =
            document.querySelectorAll(".invalid-message");
        allInvalidMessages.forEach(input => {
            input.hidden = hidden;
        });
    }

    const setCalculateBtnState = () => {
        // Change the text and style of the 'Calculate' button
        const calculateBtn = document.getElementById("calculate");
        calculateBtn.innerHTML = "Calculate";
        calculateBtn.classList.remove("btn-danger");
        calculateBtn.classList.add("btn-primary");

        // Change the style of the output card
        document.querySelector("#output").classList.remove("recalculate");
    }

    const setRecalculateBtnState = () => {
        // Change the text and style of the 'Calculate' button
        const calculateBtn = document.getElementById("calculate");
        calculateBtn.innerHTML = "Recalculate";
        calculateBtn.classList.remove("btn-primary");
        calculateBtn.classList.add("btn-danger");

        // Change the style of the output card
        document.querySelector("#output").classList.add("recalculate");
    }

    const doCalculation = (paramData) => {

        const inputData = {};

        for (const param in paramData) {
            // Get the input element for the current param
            const elem = document.querySelector(`[name=${param}]`);
            if (elem) {
                inputData[param] =
                    {'value': elem.value.trim(),
                     'unit': paramData[param].default_unit};
            }
        }

        console.log('doing the calculation with input data', inputData);

        // Find which of the two calculation options are checked
        const calcOptions =
            document.querySelectorAll('input[name="calc-options"');

        for (const option of calcOptions) {
            if (option.checked) {
                calculate(inputData, option.getAttribute("calculation"))
                .then((data) => {
                    showCalculatedValue(data.value, data.unit);
                    calculationPerformed = true;
                })
                .catch((error) => {
                    // TODO handle the error
                    console.log('got an error', error);
                });

                break;
            }
        }
    }

    const showCalculatedValue = (value, unit) => {

        // Convert the value to a float and round to 4 decimal places
        const roundedVal = (+value).toFixed(4);

        const outputBox = document.querySelector("#output");

        // Make sure the output isn't in the 'recalculate' state
        document.querySelector("#output").classList.remove("recalculate");

        output.innerHTML = `${roundedVal} ${unit}`;
    }

    // Hide all of the invalid-message divs
    hideInvalidMessages(true);

    // Initialize the calculation radio buttons (select integration time as
    //   the default)
    const calcOptions = document.querySelectorAll('input[name="calc-options"');
    for (const option of calcOptions) {
        // Add an event listener to toggle the 'disabled' attribute of the
        //   radio button options
        option.addEventListener("click", (e) => {
            // Iterate over the radio buttons. For the one that's clicked,
            // hide the corresponding input box, otherwise show the
            // corresponding box.
            for (const opt of calcOptions) {
                // Strip 'btn' from the id prepend with 'row-2'.
                // This can be used to match the name of the corresponding
                // input box row.
                const inputBoxRowId =
                    "row-" + opt.id.replace("btn-", "");
                const inputBoxRow = document.getElementById(inputBoxRowId);

                if (opt === e.target) {
                    inputBoxRow.classList.add("d-none");
                } else {
                    inputBoxRow.classList.remove("d-none");
                }
            }
            // Set the 'recalculate' state of the UI
            setRecalculateBtnState();
        });
    }

    geParamValuesUnits()
        .then((data) => {
            let formValidated = false;

            // Set up the user input field for all parameters
            const allUserInput = document.querySelectorAll(".param-input");

            allUserInput.forEach(input => {
                // Add the placeholder text
                input.setAttribute("placeholder", "Enter a value...");

                // Make the input required
                input.required = true;

                // Validate the initial input data (should never fail!)
                formValidated = validateInput(input, data[input.name]);

                // Add an event listener to validate input when it changes
                input.addEventListener("change", e => {
                    if (input === e.target) {
                        formValidated = validateInput(input, data[input.name]);
                    }
                });
            });

            // Calculate the integration time using the default values
            doCalculation(data);

            // Add an event listener to do the calculation when the form is
            //  submitted
            const form = document.getElementById("calculator-form");
            form.addEventListener("submit", (e) => {
                e.preventDefault();

                if (formValidated) {
                    doCalculation(data);
                }
            });

            // Add an event listener to the Reset button to reset the UI
            // NB: overriding the default 'reset' event handler because we
            //  have to wait for the DOM to be fully rendered before
            //  redoing the calculation
            const resetBtn = document.getElementById("reset-ui");
            resetBtn.addEventListener("click", (e) => {
                e.preventDefault();

                return new Promise((resolve, reject) => resolve(form.reset()))
                .then(() => {
                  setUIInitialState(data);
                })
            });
        })
        .catch((error) => {
            // TODO handle the error
            console.log('got an error', error);
        });
});