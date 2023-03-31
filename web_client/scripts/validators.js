const validateInput = (input, paramData) => {

    const setUpValidState = (validState) => {
        const validStateMessage = (validState)? "" : "invalid";
        input.setCustomValidity(validStateMessage);

        // Show or hide the validation message for each input
        input.nextElementSibling.hidden = (validState)? true: false;
    }

    // All values should be numeric
    if (!isNum(input.value)) {
        setUpValidState(false);
        return false;
    }

    // Where applicable, validate that the value one of the allowed
    //  values
    if (paramData.allowed_values !== null) {
        if (!isAllowedValue(input.value, paramData.allowed_values)) {
            setUpValidState(false);
            return false;
        }
    }

    // Where applicable, validate that the value is within the permitted
    //  range
    if (paramData.lower_value !== null || paramData.upper_value !== null) {
        if (!isInRange(
                input.value,
                {'lowerValue': paramData.lower_value,
                 'upperValue': paramData.upper_value,
                 'lowerValueIsFloor': paramData.lower_value_is_floor,
                 'upperValueIsCeil': paramData.upper_value_is_ceil})
                 ) {
            setUpValidState(false);
            return false;
        }
    }

    // If we got this far, validation checks must have passed
    setUpValidState(true);
    return true;
}

const isNum = (val) => {
    return !(isNaN(+val));
}

const isInRange = (val, ...rangeInfo) => {
    rangeInfo = rangeInfo[0];

    // Check the value is within the lower bounds
    if (rangeInfo.lowerValue !== null) {
        if (rangeInfo.lowerValueIsFloor && val <= rangeInfo.lowerValue) {
            return false;
        } else {
            if (val < rangeInfo.lowerValue) {
                return false;
            }
        }
    }
    // Check the value is within the upper bounds
    if (rangeInfo.upperValue != null) {
        if (rangeInfo.upperValueIsCeil && val >= rangeInfo.upperValue) {
            return false;
        } else {
            if (val > rangeInfo.upperValue) {
                return false;
            }
        }
    }
    return true;
}

const isAllowedValue = (val, allowedValues) => {
    return true;
}

export {validateInput}