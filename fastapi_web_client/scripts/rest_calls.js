const geParamValuesUnits = () => {
    return new Promise((resolve, reject) => {
        // Get the defaults and allowed values/units for each param
        $.ajax({
            url: '/v1/param-values-units',
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
//    console.log(inputData);
    return new Promise((resolve, reject) => {
        $.ajax({
            url: `/v1/${targetPath}`,
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

export {geParamValuesUnits, calculate}