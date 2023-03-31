import {geParamValuesUnits, calculate} from './rest_calls.js';
import {validateInput} from './validators.js'
import * as CalculatorUI from './calculator_ui.js'

$(document).ready(() => {

//    CalculatorUI.initializeRadioButtons();
    CalculatorUI.initializeInputs();
    CalculatorUI.hideInvalidMessages(true);

    // Get the parameter default values, default units, permitted range, etc.
    // then set up event listeners and do the initial calculation with default
    // input values.
    geParamValuesUnits()
        .then((data) => {

            let formValidated = false;

            // Set up the event listeners on user input fields
            const allUserInput = document.querySelectorAll(".param-input");

            allUserInput.forEach(input => {
                // Validate the initial input data (should never fail!)
                formValidated = validateInput(input, data[input.name]);

                // Add an event listener to validate input when it changes
                input.addEventListener("change", e => {
                    if (input === e.target) {
                        formValidated = validateInput(input, data[input.name]);
                        // Disable the calculation button if the form has not
                        // been validated, or enable if it has
                        CalculatorUI.disableCalculateBtn(!formValidated);
                        if (formValidated) {
                            CalculatorUI.resetOutputBox();
                        }
                    }
                });
            });


            const calcOptions =
                document.querySelectorAll('input[name="calc-options"');
            let checkedOption;
            // Add an event listener to the radio buttons to show or hide the
            //   appropriate input box depending on selection.
            // Keep track of which option is checked so we know whether to
            // re-enable the Calculate button.
            for (const option of calcOptions) {
                // Keep track of which radio button is currently checked
                if (option.checked) {
                    checkedOption = option;
                }

                // Add an event listener to toggle the 'disabled' attribute of the
                //   radio button options
                option.addEventListener("click", (e) => {
                    // Re-enable to Calculate button if we've changed the
                    // the checked radio button
                    if (e.target !== checkedOption) {
                        CalculatorUI.disableCalculateBtn(false);
                        CalculatorUI.resetOutputBox();
                    }
                    // Update the checked option
                    checkedOption = e.target;

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
                });
            }

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
                  CalculatorUI.setUIInitialState(data);

                  // Reset the reference to the checked radio button
                  for (const option of calcOptions) {
                    // Keep track of which radio button is currently checked
                    if (option.checked) {
                        checkedOption = option;
                    }
                  }

                  doCalculation(data);
                })
            });

            // Calculate the integration time using the default values
            doCalculation(data);

        })
        .catch((error) => {
            // TODO handle the error
            console.log('got an error', error);
        });
});

const doCalculation = (paramData) => {

    CalculatorUI.toggleSpinner('calculate', false);

    const inputData = {};

    for (const param in paramData) {
        // Get the input element for the current param and retrieve its
        //  value
        // TODO: include inputs for units
        const elem = document.querySelector(`[name=${param}]`);
        if (elem) {
            inputData[param] =
                {'value': elem.value.trim(),
                 'unit': paramData[param].default_unit};
        }
    }

    // Find which of the two calculation options are checked
    const calcOptions =
        document.querySelectorAll('input[name="calc-options"');

    for (const option of calcOptions) {
        if (option.checked) {
            calculate(inputData, option.getAttribute("calculation"))
            .then((data) => {
                CalculatorUI.showCalculatedValue(data.value, data.unit);
                CalculatorUI.disableCalculateBtn(true);
                CalculatorUI.toggleSpinner('calculate', true);
            })
            .catch((error) => {
                // TODO handle the error
                console.log('got an error', error);
            });

            break;
        }
    }
}
