const apiVersion = () => {
    return `v${document.getElementById('api_version').innerHTML}`;
}

const getParamValuesUnits = () => {
    const version = apiVersion();

    return new Promise((resolve, reject) => {
        // Get the defaults and allowed values/units for each param
        $.ajax({
            url: `/${version}/param-values-units`,
            type: 'GET',
            success: function(data) {
                resolve(data);
            },
            error: function(error) {
                reject(error);
            }
        });
    });
}

const calculate = (inputData, targetPath) => {
    const version = apiVersion();

    return new Promise((resolve, reject) => {
        $.ajax({
            url: `/${version}/${targetPath}`,
            type: 'POST',
            data: JSON.stringify(inputData),
            contentType: 'application/json',
            success: function(data) {
                resolve(data);
            },
            error: function(error) {
                reject(error);
            }
        });
    });
}

const setInstrument = (instrumentName) => {
    const version = apiVersion();

    return new Promise((resolve, reject) => {
        $.ajax({
            url: `/${version}/set-instrument`,
            type: 'POST',
            data: JSON.stringify({ instrument_name: instrumentName }),
            contentType: 'application/json',
            success: function(data) {
                resolve(data);
            },
            error: function(error) {
                reject(error);
            }
        });
    });
}

export {getParamValuesUnits, calculate, setInstrument}