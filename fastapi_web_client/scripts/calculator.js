import {geParamValuesUnits} from './rest_calls.js';
import {isNum} from './validators.js'

$(document).ready(() => {

    const validateInput = (value, data) => {
        if (!isNum(value)) {
            // TODO handle the error
            console.log(`${value} is not a valid number`);
        }
        // TODO do the rest of the validation
    }

    const highlightRecalculate = () => {
        // TODO: do I really want to do this?
    }

    const doCalculation = () => {
        // TODO: submit the request to do the calculation
    }

    geParamValuesUnits()
        .then((data) => {
            // Set up the user input field on all input fields
            const allUserInput = document.querySelectorAll(".param-input");
            console.log(allUserInput);

            allUserInput.forEach(input => {
                // Add the placeholder text
                input.setAttribute("placeholder", "Enter a value...");

                // Validate the initial input
                validateInput(input.value, data[input.name]);

                // Add an event listener to validate input when it changes
                input.addEventListener("change", e => {
                    if (input === e.target) {
                        validateInput(input.value, data[input.name]);
                    }
                })
            });
        })
        .catch((error) => {
            // TODO handle the error
            console.log('got an error', error);
        });
});