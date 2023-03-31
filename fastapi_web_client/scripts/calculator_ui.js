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

const initializeInputs = (formValidated) => {
    // Set up the user input field for all parameters
    const allUserInput = document.querySelectorAll(".param-input");

    allUserInput.forEach(input => {
        // Add the placeholder text
        input.setAttribute("placeholder", "Enter a value...");

        // Make the input required
        input.required = true;
    });
}

export {setUIInitialState, hideInvalidMessages, showCalculatedValue,
        disableCalculateBtn, initializeInputs, resetOutputBox}
