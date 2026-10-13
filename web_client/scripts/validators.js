import { convertVelocityToFrequency } from './rest_calls.js';

const specialUnits = ['km / s', 'm / s']

const getDefaultInvalidMessage = (input) => {
    const invalidMessageElement =
        document.getElementById(`${input.id}-invalid`);
    if (!invalidMessageElement) {
        return null;
    }

    if (invalidMessageElement.dataset.defaultMessage === undefined) {
        invalidMessageElement.dataset.defaultMessage =
            invalidMessageElement.textContent;
    }
    return invalidMessageElement.dataset.defaultMessage;
}

const validateInput = (input, units, paramData) => {
    const setUpValidState = (validState) => {
        const validStateMessage = (validState)? "" : "invalid";
        input.setCustomValidity(validStateMessage);

        // Show or hide the validation message for each input
        const invalid_msg_elem = document.getElementById(`${input.id}-invalid`);
        getDefaultInvalidMessage(input);
        invalid_msg_elem.hidden = (validState)? true: false;
    }

    // All values should be numeric
    if (!isNum(input.value)) {
        setUpValidState(false);
        const invalidMessageElement = document.getElementById(`${input.id}-invalid`);
        const defaultMessage = getDefaultInvalidMessage(input);
        if (invalidMessageElement && defaultMessage !== null) {
            invalidMessageElement.textContent = defaultMessage;
        }
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
        let valueToValidate;

        // Get the corresponding unit for the input
        const unitsElem = document.getElementById(`${input.name}-units`);
        if (units) {
            // Convert the input value from the specified to the default
            //  units for this parameter
            valueToValidate =
                input.value * paramData.data_conversion[units.value];
        }
        else {
            valueToValidate = input.value;
        }

        if (!isInRange(
                valueToValidate,
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

const validateInputAgainstInstrumentRange = async (input, rangeText, userSelectedUnit = null) => {
    const setUpValidState = (validState, message = "") => {
        const validStateMessage = validState ? "" : message;
        input.setCustomValidity(validStateMessage);

        const calculateButton = document.getElementById("calculate");
        if (validState == false) {
            calculateButton.disabled = true;
        } else {
            calculateButton.disabled = false;
        }

        const invalid_msg_elem = document.getElementById(`${input.id}-invalid`);
        if (invalid_msg_elem) {
            getDefaultInvalidMessage(input);
            if (message) {
                invalid_msg_elem.textContent = message;
            }
            invalid_msg_elem.hidden = validState;
        }
    }

    const parsedRangeList = parseInstrumentRange(rangeText);
    let numericValue = Number(input.value);
    if (!isNum(input.value)) {
        setUpValidState(false, getDefaultInvalidMessage(input) || "");
        document.getElementById("calculate").disabled = true;
        return false;
    }

    if (specialUnits.includes(userSelectedUnit)) {
        const obsFreqInput = document.getElementById("obs-freq-input");
        if (!obsFreqInput || !isNum(obsFreqInput.value)) {
            document.getElementById("calculate").disabled = true;
            return false;
        }

        const conversion = await convertVelocityToFrequency({
            obs_freq: Number(obsFreqInput.value),
            velocity: numericValue,
            velocity_unit: userSelectedUnit,
        });
        numericValue = conversion.value;
    }

    let valueInRange = false;
    for (const parsedRange of parsedRangeList) {
        const parsedRangeUnit = parsedRange.unit === null || parsedRange.unit === undefined ? "Hz" : parsedRange.unit;
        const valueToValidate = convertValueToUnit(numericValue, userSelectedUnit, parsedRangeUnit);
        const aboveLowerBound = parsedRange.upper === null
            ? valueToValidate > parsedRange.lower
            : valueToValidate >= parsedRange.lower;
        const belowUpperBound = parsedRange.upper === null || parsedRange.upper === undefined
            || valueToValidate <= parsedRange.upper;

        if (aboveLowerBound && belowUpperBound) {
            valueInRange = true;
            setUpValidState(true);
            break;
        }
    }

    if (!valueInRange) {
        setUpValidState(false, `Value must be between allowed ranges 
            for the chosen instrument.`);
    }
    return valueInRange;
}

const parseInstrumentRange = (rangeText) => {

    const trimmed = rangeText.trim();

    const unitMatch = trimmed.match(/(Hz|kHz|MHz|GHz|THz)$/i);
    const unit = unitMatch ? unitMatch[1] : 'GHz';

    const values = trimmed.match(/[-+]?((\d+(\.\d*)?)|(\.\d+))(e[-+]?\d+)?/g);

    if (trimmed.includes('>')) {
        const numericValue = Number(values[0]);
        return [{ lower: numericValue, upper: null, unit }];
    }

    if (values.length % 2 == 0) {
        let ranges = [];
        for (let range=0; range < values.length; range += 2) {
            const lower = Number(values[range]);
            const upper = Number(values[range + 1]);
            ranges.push({ lower, upper, unit });
        }
    return ranges;
    }
}

const convertValueToUnit = (value, fromUnit, toUnit) => {
    const unitToHz = {
        hz: 1,
        khz: 1e3,
        mhz: 1e6,
        ghz: 1e9
    };

    const normalizedFrom = fromUnit.toLowerCase();
    const normalizedTo = toUnit.toLowerCase();

    if (!unitToHz[normalizedFrom] || !unitToHz[normalizedTo]) {
        return value;
    }

    return value * unitToHz[normalizedFrom] / unitToHz[normalizedTo];
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

export {validateInput, validateInputAgainstInstrumentRange}