const isNum = (val) => {
    return !(isNaN(+val));
}

const isInRange = (val, range) => {
    return true;
}

const isAllowedValue = (val, allowedValues) => {
    return true;
}

export {isNum, isInRange, isAllowedValue}