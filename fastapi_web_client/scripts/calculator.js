import {geParamValuesUnits, calculate} from './rest_calls.js';
import {validateInput} from './validators.js'

$(document).ready(() => {

    const highlightRecalculate = () => {
        // TODO: do I really want to do this?
    }

    const doCalculation = (param_data) => {

        const inputData = {};

        for (const param in param_data) {
            // Get the input element for the current param
            const elem = document.querySelector(`[name=${param}]`);
            if (elem) {
                inputData[param] =
                    {'value': elem.value.trim(),
                     'unit': param_data[param].default_unit};
            }
        }

        // Find which of the two calculation options are checked
        const calc_options =
            document.querySelectorAll('input[name="calc-options"');

        for (const option of calc_options) {
            if (option.checked) {
                calculate(inputData, option.getAttribute("calculation"))
                .then((data) => {
                    console.log('got response', data);
                })
                .catch((error) => {
                    // TODO handle the error
                    console.log('got an error', error);
                });

                break;
            }
        }
    }

    // Hide all of the invalid-message divs
    const allInvalidMessages =
        document.querySelectorAll(".invalid-message");
    allInvalidMessages.forEach(input => {
        input.hidden = true;
    });

    geParamValuesUnits()
        .then((data) => {
            let formValidated = false;

            // Set up the user input field on all input fields
            const allUserInput = document.querySelectorAll(".param-input");

            allUserInput.forEach(input => {
                // Add the placeholder text
                input.setAttribute("placeholder", "Enter a value...");

                // Set the required attribute
                input.required = true;

                // Validate the initial input
                formValidated = validateInput(input, data[input.name]);

                // Add an event listener to validate input when it changes
                input.addEventListener("change", e => {
                    if (input === e.target) {
                        formValidated = validateInput(input, data[input.name]);
                    }
                });
            });

            const form = document.getElementById("calculator-form");
            form.addEventListener("submit", (e) => {
                e.preventDefault();

                if (formValidated) {
                    doCalculation(data);
                }
            })
        })
        .catch((error) => {
            // TODO handle the error
            console.log('got an error', error);
        });
});