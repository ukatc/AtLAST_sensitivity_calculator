const geParamValuesUnits = () => {
    return new Promise((resolve, reject) => {
        // Get the defaults and allowed values/units for each param
        $.ajax({ url: '/v1/param-values-units',
            type: 'GET',
            success: function (data) {
                console.log(typeof data);
                console.log(data);
                resolve(data);
            },
            error: function (error) {
                console.log(error);
                reject(error);
            }
        });
    });
}

export {geParamValuesUnits}