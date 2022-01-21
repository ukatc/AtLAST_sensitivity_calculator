"use strict";
//import $ from "jquery";
exports.__esModule = true;
exports.sortResults = exports.parseDec = exports.parseRA = void 0;
// === ON SUBMIT === //
// This code will run when the "Calculate" button is clicked.
// Capture and disable form submission. If there are invalid fields, present invalid feedback to the user, otherwise perform calculation.
(function () {
    'use strict';
    window.addEventListener('load', function () {
        // Get the forms we want to add validation styles to
        var forms = document.getElementsByClassName('needs-validation');
        // Loop over them (There will only be the one form)
        /* eslint-disable */
        var validation = Array.prototype.filter.call(forms, function (form) {
            /*eslint-enable */
            form.addEventListener('submit', function (event) {
                console.log('submit');
                // Prevent form submission to stop a page change/refresh
                event.preventDefault();
                event.stopPropagation();
                // Add the "was-validated" class to the form to indicate 
                // validation has happened at least once (Used by bootstrap).
                form.classList.add('was-validated');
                // Read inputs from the page
                var input_dict = readForm();
                console.log('after');
                console.log(input_dict);
                // Using AJAX, make a GET request to the '/calc' Flask route in calculate.py
                $.ajax({ url: '/v1/sensitivity',
                    type: 'GET',
                    data: input_dict,
                    success: function (data) {
                        updateOutput(input_dict, data);
                    }
                });
            }, false);
        });
    }, false);
})();
// Function to check if given bandwidth is entirely contained within the band.
function isBandwidthContained(obs_freq_scaled, bandwidth_scaled, obs_band) {
    var obs_freq_scaled_num = Number(obs_freq_scaled);
    var half_bandwidth = Number(bandwidth_scaled) / 2.0;
    var lower_bound = obs_freq_scaled_num - half_bandwidth;
    var upper_bound = obs_freq_scaled_num + half_bandwidth;
    switch (obs_band) {
        case "Band 1":
            if (lower_bound < 0.35e9 || upper_bound > 1.05e9) {
                return false;
            }
            break;
        case "Band 2":
            if (lower_bound < 0.95e9 || upper_bound > 1.76e9) {
                return false;
            }
            break;
        case "Band 5a":
            if (lower_bound < 4.6e9 || upper_bound > 8.4e9) {
                return false;
            }
            break;
        case "Band 5b":
            if (lower_bound < 8.4e9 || upper_bound > 15.4e9) {
                return false;
            }
            break;
    }
    return true;
}
// functions to facilitate validating inputs
function isNumeric(val) {
    return !(val instanceof Array) && (val - parseFloat(val) + 1) >= 0;
}
function parseRA(RA) {
    return (/^\d{1,2}:\d{1,2}:\d+(\.\d+)?$/.test(RA));
}
exports.parseRA = parseRA;
function parseDec(Dec) {
    return (/[-+]\d{1,2}:\d{1,2}:\d+(\.\d+)?$/.test(Dec));
}
exports.parseDec = parseDec;
// Validate a frequency input, making sure it is not empty and is a number.
function validateObsFreq(field, obs_freq, obs_freq_scaled, obs_band) {
    var frequency_feedback = document.getElementById(field + "-invalid");
    var frequency_input = document.getElementById(field + "-input");
    if (!isNumeric(obs_freq) || obs_freq == "") {
        frequency_feedback.textContent = "Please enter a number";
        frequency_feedback.style.display = "block";
        frequency_input.setCustomValidity("Invalid Field.");
        return false;
    }
    else {
    }
    return true;
}
// Validate a bandwidth input, making sure it is not empty and is a number.
function validateBandwidth(field, bandwidth, bandwidth_scaled, obs_freq_scaled, obs_band) {
    var bandwidth_feedback = document.getElementById(field + "-invalid");
    var bandwidth_input = document.getElementById(field + "-input");
    if (!isNumeric(bandwidth) || bandwidth == "") {
        bandwidth_feedback.textContent = "Please enter a number";
        bandwidth_feedback.style.display = "block";
        bandwidth_input.setCustomValidity("Invalid Field.");
        return false;
    }
    else {
        if (isBandwidthContained(obs_freq_scaled, bandwidth_scaled, obs_band)) {
            bandwidth_feedback.style.display = "none";
            bandwidth_input.setCustomValidity("");
        }
        else {
            bandwidth_feedback.textContent = "Bandwidth must be fully contained within the band.";
            bandwidth_feedback.style.display = "block";
            bandwidth_input.setCustomValidity("Invalid Field.");
            return false;
        }
    }
    return true;
}
// function to convert Sexagesimal declination to decimal for source validation
function Sexa2Dec(Dec) {
    var DecSplit = Dec.split(':', 3);
    if (Number(DecSplit[0]) < 0) {
        return (Number(DecSplit[0]) - Number(DecSplit[1]) / 60 - Number(DecSplit[2]) / 3600);
    }
    else {
        return (Number(DecSplit[0]) + Number(DecSplit[1]) / 60 + Number(DecSplit[2]) / 3600);
    }
}
function isAboveHorizon(Dec) {
    // this is a very coarse way to do this validation. Review in future.
    var SkaLatitude = Sexa2Dec("-30:43:16.068");
    if (Sexa2Dec(Dec) < 90.0 + SkaLatitude) {
        return true;
    }
    return false;
}
// Validate right ascension input
function validateRA(coords) {
    var feedback = document.getElementById("RA-invalid");
    var input = document.getElementById("RA-input");
    if (parseRA(coords)) {
        feedback.style.display = "none";
        input.setCustomValidity("");
        return true;
    }
    feedback.textContent = "Input formatted incorrectly.";
    feedback.style.display = "block";
    input.setCustomValidity("Invalid Field.");
    return false;
}
// Validate declination input
function validateDec(coords) {
    var feedback = document.getElementById("dec-invalid");
    var input = document.getElementById("dec-input");
    if (!parseDec(coords)) {
        feedback.textContent = "Input formatted incorrectly.";
        feedback.style.display = "block";
        input.setCustomValidity("Invalid Field.");
        return false;
    }
    else if (!isAboveHorizon(coords)) {
        feedback.textContent = "Target is never above the horizon";
        feedback.style.display = "block";
        input.setCustomValidity("Invalid Field.");
        return false;
    }
    feedback.style.display = "none";
    input.setCustomValidity("");
    return true;
}
// Validate a given eta input, making sure it is not empty and is a number
function validateEta(field, value) {
    var feedback = document.getElementById(field + "-invalid");
    var input = document.getElementById(field + "-input");
    if (input.disabled) {
        feedback.style.display = "none";
        input.setCustomValidity("");
    }
    else {
        if (!isNumeric(value) || value == "") {
            feedback.textContent = "Please enter a number";
            feedback.style.display = "block";
            input.setCustomValidity("Invalid Field.");
            return false;
        }
        else {
            if (value <= 0 || value > 1) {
                feedback.textContent = "Value must be between 0 and 1";
                feedback.style.display = "block";
                input.setCustomValidity("Invalid Field.");
                return false;
            }
            else {
                feedback.style.display = "none";
                input.setCustomValidity("");
            }
        }
    }
    return true;
}
// General function to validate and input that needs no special treatment
function validateGeneral(field, value) {
    var feedback = document.getElementById(field + "-invalid");
    var input = document.getElementById(field + "-input");
    if (input.disabled) {
        feedback.style.display = "none";
        input.setCustomValidity("");
    }
    else {
        if (!isNumeric(value) || value == "") {
            feedback.textContent = "Please enter a number";
            feedback.style.display = "block";
            input.setCustomValidity("Invalid Field.");
            return false;
        }
        else {
            if (value <= 0) {
                feedback.textContent = "Value must be greater than 0";
                feedback.style.display = "block";
                input.setCustomValidity("Invalid Field.");
                return false;
            }
            else {
                feedback.style.display = "none";
                input.setCustomValidity("");
            }
        }
    }
    return true;
}
// Validate zoom inputs
function validateZooms(zoom_freqs, zoom_freqs_scaled, zoom_resolution, obs_band) {
    var return_bools = [true, true, true, true];
    for (var i = 0; i < 4; i++) {
        var zoom_feedback = document.getElementById("zoom" + String(i + 1) + "-frequency-invalid");
        var zoom_input = document.getElementById("zoom" + String(i + 1) + "-frequency-input");
        if (!zoom_input.disabled) {
            if (zoom_freqs[i] == "") {
                if (i == 0) {
                    // If the first input is blank, need to invalidate form
                    zoom_feedback.textContent = "Please enter a number";
                    zoom_feedback.style.display = "block";
                    zoom_input.setCustomValidity("Invalid Field.");
                    return_bools[i] = false;
                }
                else {
                    zoom_feedback.style.display = "none";
                    zoom_input.setCustomValidity("");
                }
            }
            else if (!isNumeric(zoom_freqs[i])) {
                zoom_feedback.textContent = "Please enter a number";
                zoom_feedback.style.display = "block";
                zoom_input.setCustomValidity("Invalid Field.");
                return_bools[i] = false;
            }
            else if (!isBandwidthContained(zoom_freqs_scaled[i], zoom_resolution[i], obs_band)) {
                zoom_feedback.textContent = "Zoom resolution must be entirely contained within the observing band";
                zoom_feedback.style.display = "block";
                zoom_input.setCustomValidity("Invalid Field.");
                return_bools[i] = false;
            }
            else {
                zoom_feedback.style.display = "none";
                zoom_input.setCustomValidity("");
            }
        }
        else {
            zoom_feedback.style.display = "none";
            zoom_input.setCustomValidity("");
        }
    }
    return return_bools;
}
function validateInteger(field, value) {
    var feedback = document.getElementById(field + "-invalid");
    var input = document.getElementById(field + "-input");
    if (input.disabled) {
        feedback.style.display = "none";
        input.setCustomValidity("");
    }
    else {
        if (!isNumeric(value) || value == "") {
            feedback.textContent = "Please enter a number";
            feedback.style.display = "block";
            input.setCustomValidity("Invalid Field.");
            return false;
        }
        else {
            if (value < 0) {
                feedback.textContent = "Value cannot be negative";
                feedback.style.display = "block";
                input.setCustomValidity("Invalid Field.");
                return false;
            }
        }
    }
    return true;
}
// Function to validate fields that can either contain an empty string or
// a number between min and max.
function validateNumberMinMax(field, value, min, max) {
    var feedback = document.getElementById(field + "-invalid");
    var input = document.getElementById(field + "-input");
    // Got through possible situtations in turn.
    if (input.disabled) {
        feedback.style.display = "none";
        input.setCustomValidity("");
        return true;
    }
    if (value == "") {
        feedback.style.display = "none";
        input.setCustomValidity("");
        return true;
    }
    if (!isNumeric(value)) {
        feedback.textContent = "Please enter a number between " + min + " and " + max;
        feedback.style.display = "block";
        input.setCustomValidity("Invalid Field.");
        return false;
    }
    var numval = parseFloat(value);
    if (numval < min) {
        feedback.textContent = "Please enter a number between " + min + " and " + max;
        feedback.style.display = "block";
        input.setCustomValidity("Invalid Field.");
        return false;
    }
    if (numval > max) {
        feedback.textContent = "Please enter a number between " + min + " and " + max;
        feedback.style.display = "block";
        input.setCustomValidity("Invalid Field.");
        return false;
    }
    feedback.style.display = "none";
    input.setCustomValidity("");
    return true;
}
// Function to perform input validation.
// Checks that a value has been entered for each input, that each value is formatted correctly and that each value
// is within acceptable ranges. Returns a boolean to indicate whether there were any invalid inputs.
function validateInput(input_dict, observing_modes) {
    // This will be set to false if there are any issues
    var return_bool = true;
    // --- Universal Inputs --- //
    return_bool = return_bool && validateRA(input_dict.right_asc);
    return_bool = return_bool && validateDec(input_dict.dec);
    return_bool = return_bool && validateInteger("nMeer", input_dict.nMeer);
    return_bool = return_bool && validateInteger("nSKA", input_dict.nSKA);
    return_bool = return_bool && validateNumberMinMax("pwv", input_dict.weather, 3, 25);
    return_bool = return_bool && validateNumberMinMax("elev", input_dict.elevation, 5, 90);
    // If we're using the internal version, we want to check these extra inputs
    if (input_dict.calculator_mode === "Internal") {
        return_bool = return_bool && validateEta("etaPointing", input_dict.etaPointing);
        return_bool = return_bool && validateEta("etaCoherence", input_dict.etaCoherence);
        return_bool = return_bool && validateEta("etaDigitisation", input_dict.etaDigitisation);
        return_bool = return_bool && validateEta("etaCorrelation", input_dict.etaCorrelation);
        return_bool = return_bool && validateEta("etaBandpass", input_dict.etaBandpass);
        return_bool = return_bool && validateGeneral("Tsys_SKA", input_dict.Tsys_SKA);
        return_bool = return_bool && validateGeneral("Trcv_SKA", input_dict.Trcv_SKA);
        return_bool = return_bool && validateGeneral("Tspl_SKA", input_dict.Tspl_SKA);
        return_bool = return_bool && validateGeneral("Tsys_Meer", input_dict.Tsys_Meer);
        return_bool = return_bool && validateGeneral("Trcv_Meer", input_dict.Trcv_Meer);
        return_bool = return_bool && validateGeneral("Tspl_Meer", input_dict.Tspl_Meer);
        return_bool = return_bool && validateGeneral("Tsky", input_dict.Tsky);
        return_bool = return_bool && validateGeneral("Tgal", input_dict.Tgal);
        return_bool = return_bool && validateGeneral("alpha", input_dict.alpha);
        return_bool = return_bool && validateEta("etaSKA", input_dict.etaSKA);
        return_bool = return_bool && validateEta("etaMeer", input_dict.etaMeer);
    }
    // Special case for Integration Time Override, since it's allowed to be left blank
    if (input_dict.main_int_time != null) {
        return_bool = return_bool && validateGeneral("main-integration", input_dict.main_int_time);
    }
    else {
        document.getElementById("main-integration-invalid").style.display = "none";
        document.getElementById("main-integration-input").setCustomValidity("");
    }
    // --- Continuum Inputs --- //
    if (observing_modes["continuum"]) {
        return_bool = return_bool && validateObsFreq("continuum-frequency", input_dict.continuum_obs_freq, input_dict.continuum_obs_freq_scaled, input_dict.obs_band);
        return_bool = return_bool && validateBandwidth("continuum-bandwidth", input_dict.continuum_bandwidth, input_dict.continuum_bandwidth_scaled, input_dict.continuum_obs_freq_scaled, input_dict.obs_band);
        return_bool = return_bool && validateGeneral("continuum-chunks", input_dict.continuum_n_chunks);
        // Only want to validate one of either integration or sensitivity
        if (input_dict.continuum_supplied == "IntegrationTime") {
            return_bool = return_bool && validateGeneral("continuum-integration", input_dict.continuum_int_time);
        }
        else {
            return_bool = return_bool && validateGeneral("continuum-sensitivity", input_dict.continuum_sensitivity);
        }
    }
    else {
        // If Continuum is not an active observing mode, we ignore these inputs and assume they're all fine
        document.getElementById("continuum-frequency-invalid").style.display = "none";
        document.getElementById("continuum-frequency-input").setCustomValidity("");
        document.getElementById("continuum-bandwidth-invalid").style.display = "none";
        document.getElementById("continuum-bandwidth-input").setCustomValidity("");
        document.getElementById("continuum-chunks-invalid").style.display = "none";
        document.getElementById("continuum-chunks-input").setCustomValidity("");
        document.getElementById("continuum-integration-invalid").style.display = "none";
        document.getElementById("continuum-integration-input").setCustomValidity("");
        document.getElementById("continuum-sensitivity-invalid").style.display = "none";
        document.getElementById("continuum-sensitivity-input").setCustomValidity("");
    }
    // --- Line Inputs --- //
    if (observing_modes["line"]) {
        // Validate zooms, getting an array of bools. Use each one in turn to update return_bool
        var zoom_bools = validateZooms(input_dict.zoom_freqs, input_dict.zoom_freqs_scaled, input_dict.zoom_resolutions, input_dict.obs_band);
        zoom_bools.forEach(function (bool) { return return_bool == return_bool && bool; });
        return_bool == return_bool && validateGeneral("line-integration", input_dict.line_int_time);
        return_bool == return_bool && validateGeneral("line-sensitivity", input_dict.line_sensitivity);
    }
    else {
        // If Line is not an active observing mode, we ignore these inputs and assumw they're all fine
        for (var i = 0; i < 4; i++) {
            document.getElementById("zoom" + String(i + 1) + "-frequency-invalid").style.display = "none";
            document.getElementById("zoom" + String(i + 1) + "-frequency-input").setCustomValidity("");
        }
        document.getElementById("line-integration-invalid").style.display = "none";
        document.getElementById("line-integration-input").setCustomValidity("");
        document.getElementById("line-sensitivity-invalid").style.display = "none";
        document.getElementById("line-sensitivity-input").setCustomValidity("");
    }
    return return_bool;
}
//Function to convert a given frequency to Hz according to the units
function scaleFrequency(freq_val, freq_units) {
    var freq_val_scaled = 0;
    switch (freq_units) {
        case "kHz":
            freq_val_scaled = freq_val * 1000;
            break;
        case "MHz":
            freq_val_scaled = freq_val * 1000000;
            break;
        case "GHz":
            freq_val_scaled = freq_val * 1000000000;
            break;
        case "Hz":
            freq_val_scaled = freq_val;
            break;
        default: freq_val_scaled = freq_val;
    }
    return freq_val_scaled;
}
function scaleTime(time_val, time_units) {
    var time_val_scaled = null;
    if (isNumeric(time_val)) {
        switch (time_units) {
            case "ms":
                time_val_scaled = Number(time_val) / 1000;
                break;
            case "us":
                time_val_scaled = Number(time_val) / 1000000;
                break;
            case "ns":
                time_val_scaled = Number(time_val) / 1000000000;
                break;
            case "m":
                time_val_scaled = Number(time_val) * 60;
                break;
            case "h":
                time_val_scaled = Number(time_val) * 3600;
                break;
            case "d":
                time_val_scaled = Number(time_val) * 86400;
                break;
            case "s":
                time_val_scaled = Number(time_val);
                break;
            default: time_val_scaled = Number(time_val);
        }
    }
    return time_val_scaled;
}
//Function to convert a given sensitivity into Janskys according to the units
function scaleSensitivity(sens_val, sens_units) {
    var sens_val_scaled = 0;
    switch (sens_units) {
        case "Jy":
            sens_val_scaled = sens_val;
            break;
        case "mJy":
            sens_val_scaled = sens_val / 1000;
            break;
        case "uJy":
            sens_val_scaled = sens_val / 1000000;
            break;
        case "nJy":
            sens_val_scaled = sens_val / 1000000000;
            break;
        default: sens_val_scaled = sens_val;
    }
    return sens_val_scaled;
}
// This function is a utility used in the readForm function when using internal mode. Updated by Liz to make the value
// null if the element is disabled, rather than capturing what's in the field.
function getElementValueOrNull(element_id) {
    if (document.getElementById(element_id).disabled) {
        return null;
    }
    else {
        var temp = document.getElementById(element_id).value.trim();
        if (temp.length === 0) {
            return null;
        }
        else {
            return temp;
        }
    }
}
// This function scans through the page and collects the values, units, etc from every input
function readForm() {
    // --- Universal Inputs --- //
    // RA and dec
    var right_asc = document.getElementById("RA-input").value.trim();
    var dec = document.getElementById("dec-input").value.trim();
    // Gather values into a dictionary and return
    var return_dict = {
        "right_asc": right_asc,
        "dec": dec
    };
    console.log('readForm');
    console.log(return_dict);
    return return_dict;
}
// Function to skim through the input dictionary and remove any key-value pairs which aren't needed anymore.
// This reduces the amount of data sent to the server in the AJAX calls.
function reduceInputs(input_dict, observing_modes) {
    // If continuum is not an active observing mode, we can remove all of these inputs.
    if (!observing_modes["continuum"]) {
        delete input_dict["continuum_obs_freq_scaled"];
        delete input_dict["continuum_bandwidth_scaled"];
        delete input_dict["continuum_resolution"];
        delete input_dict["continuum_n_chunks"];
        delete input_dict["continuum_int_time_scaled"];
        delete input_dict["continuum_sensitivity_scaled"];
        delete input_dict["continuum_supplied"];
    }
    // Likewise for line...
    if (!observing_modes["line"]) {
        delete input_dict["zoom_freqs_scaled"];
        delete input_dict["zoom_resolutions"];
        delete input_dict["line_int_time_scaled"];
        delete input_dict["line_sensitivity_scaled"];
        delete input_dict["line_supplied"];
    }
    // By this point we don't need to know if we're using the internal/public version of the calculator
    delete input_dict["calculator_mode"];
    // Return the reduced form of the input_dict
    return input_dict;
}
// Function to find which observing modes are currently active
function getObservingModes() {
    return {
        "continuum": document.getElementById("collapse-continuum").classList.contains("show"),
        "line": document.getElementById("collapse-line").classList.contains("show"),
        "pulsars": document.getElementById("collapse-pulsars").classList.contains("show")
    };
}
// Function to sort the results object keys in order of decreasing PWV
function sortResults(data) {
    // Assemble a list of [key,pwv] pairs
    var keyval;
    var datamap = [];
    for (var k in data) {
        var pwv = !("calculator_state" in data[k]) ? null
            : !("pwv" in data[k]["calculator_state"]) ? null
                : data[k]["calculator_state"]["pwv"];
        datamap.push([k, pwv]);
    }
    // Sort the list in decreasing PWV
    datamap.sort(function (a, b) {
        var pwv_a = a[1];
        var pwv_b = b[1];
        if (pwv_a == null) {
            return 0;
        }
        if (pwv_b == null) {
            return 0;
        }
        var pwv_a_float = parseFloat(pwv_a);
        var pwv_b_float = parseFloat(pwv_b);
        if (pwv_a_float < pwv_b_float) {
            return 1;
        }
        if (pwv_a_float > pwv_b_float) {
            return -1;
        }
        // pwvs must be equal
        return 0;
    });
    return datamap;
}
exports.sortResults = sortResults;
function continuumOutputForSensitivity(input_dict, data) {
    var out_string = '';
    out_string += "<div class='table-wrapper'><div class='row' style='border-bottom: 1px solid rgba(0, 0, 0, 0.3);'>";
    out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content header-text'>Weather</div>";
    out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content header-text'>Int.Time Full BW</div>";
    out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content header-text'>Int.Time Chunk</div>";
    out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content header-text'>Chunk Centre</div>";
    out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content header-text'>Int.Time Line</div>";
    out_string += "<div class='col-lg-1 col-xl-1 col-md-1 column-content header-text'>PWV</div>";
    out_string += "<div class='col-lg-1 col-xl-1 col-md-1 column-content header-text'>Elevation</div>";
    out_string += "</div>";
    // sort the results in order of increasing PWV
    var datamap = sortResults(data);
    // format the results in turn
    for (var k2 in datamap) {
        var key = datamap[k2][0];
        out_string += "<div class='row row-padding'>";
        out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content row-text'>" + key + "</div>";
        out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content row-text'>" + data[key]["cont_int_time"] + "</div>";
        out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content row-text'>";
        for (var i = 0; i < data[key]["chunk_int_times"].length; i++) {
            out_string += "<span class='margin-right'>" + data[key]["chunk_int_times"][i] + " <br> </span>";
        }
        out_string += "</div>";
        out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content row-text'>";
        for (var i = 0; i < data[key]["chunk_centres"].length; i++) {
            out_string += "<span class='margin-right'>" + data[key]["chunk_centres"][i] + " <br> </span>";
        }
        out_string += "</div>";
        out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content row-text'>" + data[key]["cont_line_int_time"] + "</div>";
        out_string += "<div class='col-lg-1 col-xl-1 col-md-1 column-content row-text'>" + (data[key]["calculator_state"]["pwv"] == undefined ? 'null' : data[key]["calculator_state"]["pwv"]) + "</div>";
        out_string += "<div class='col-lg-1 col-xl-1 col-md-1 column-content row-text'>" + (data[key]["calculator_state"]["elevation"] || 'null') + "</div>";
        out_string += "</div>";
    }
    out_string += "</div></br><div>";
    out_string += "<p>The target RMS noise is <b> " + String(input_dict.continuum_sensitivity) + String(input_dict.continuum_sensitivity_units) + "</b></p>";
    if (input_dict.continuum_n_chunks > 1) {
        out_string += "<p>The band is divided into <b>" + String(input_dict.continuum_n_chunks) + "</b> chunks, each <b>" + String(data[Object.keys(data)[0]]["chunk_width"]) + " </b>wide.</p>";
    }
    out_string += "<p>The line int. time is for the central frequency (<b>" + String(input_dict.continuum_obs_freq) + String(input_dict.continuum_obs_freq_units);
    out_string += "</b>) , with a resolution of <b>" + String(input_dict.continuum_resolution / 1000.0) + "kHz</b></p></div>";
    return out_string;
}
function continuumOutputForIntegrationTime(input_dict, data) {
    var out_string = '';
    out_string += "<div class='table-wrapper'><div class='row' style='border-bottom: 1px solid rgba(0, 0, 0, 0.3);'>";
    out_string += "<div class='col-lg-1 col-xl-1 col-md-1 column-content header-text'>Weather</div>";
    out_string += "<div class='col-lg-1 col-xl-1 col-md-1 column-content header-text'>Integration Time</div>";
    out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content header-text'>Noise Full BW</div>";
    out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content header-text'>Noise Chunk</div>";
    out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content header-text'>Chunk Centre</div>";
    out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content header-text'>Line Noise</div>";
    out_string += "<div class='col-lg-1 col-xl-1 col-md-1 column-content header-text'>PWV</div>";
    out_string += "<div class='col-lg-1 col-xl-1 col-md-1 column-content header-text'>Elevation</div>";
    out_string += "</div>";
    // sort the results in order of increasing PWV
    var datamap = sortResults(data);
    // format the results in turn
    for (var k2 in datamap) {
        var key = datamap[k2][0];
        out_string += "<div class='row row-padding'>";
        out_string += "<div class='col-lg-1 col-xl-1 col-md-1 column-content row-text'>" + key + "</div>";
        out_string += "<div class='col-lg-1 col-xl-1 col-md-1 column-content row-text'>" + (input_dict.main_int_time == null ? String(input_dict.continuum_int_time) + String(input_dict.continuum_int_time_units) : String(input_dict.main_int_time) + String(input_dict.main_int_time_units)) + "</div>";
        out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content row-text'>" + data[key]["cont_sens"] + "</div>";
        out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content row-text'>";
        for (var i = 0; i < data[key]["chunk_sensitivities"].length; i++) {
            out_string += "<span class='margin-right'>" + data[key]["chunk_sensitivities"][i] + " <br> </span>";
        }
        out_string += "</div>";
        out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content row-text'>";
        for (var i = 0; i < data[key]["chunk_centres"].length; i++) {
            out_string += "<span class='margin-right'>" + data[key]["chunk_centres"][i] + " <br> </span>";
        }
        out_string += "</div>";
        out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content row-text'>" + data[key]["cont_line_sens"] + "</div>";
        out_string += "<div class='col-lg-1 col-xl-1 col-md-1 column-content row-text'>" + (data[key]["calculator_state"]["pwv"] == undefined ? 'null' : data[key]["calculator_state"]["pwv"]) + "</div>";
        out_string += "<div class='col-lg-1 col-xl-1 col-md-1 column-content row-text'>" + (data[key]["calculator_state"]["elevation"] || 'null') + "</div>";
        out_string += "</div>";
    }
    out_string += "</div></br></br><div>";
    if (input_dict.continuum_n_chunks > 1) {
        out_string += "<p>Dividing the bandwidth into <b>" + String(input_dict.continuum_n_chunks) + ", " + String(data[Object.keys(data)[0]]["chunk_width"]) + " </b>chunks.</p>";
    }
    out_string += "<p>The Line noise is at the central frequency of (<b>" + String(input_dict.continuum_obs_freq) + String(input_dict.continuum_obs_freq_units);
    out_string += "</b>) , with a resolution of <b>" + String(input_dict.continuum_resolution / 1000.0) + "kHz</b></p></div>";
    return out_string;
}
// Function to render the line report to the page
function outputLine(input_dict, data) {
    var line_output = document.getElementById("line-output");
    line_output.classList.remove("hidden");
    var out_string = "";
    // Check whether Integration/Sensitiviy was supplied. We report each differently
    if (input_dict.line_supplied == "IntegrationTime") {
        out_string += lineOutputForIntegrationTime(input_dict, data);
    }
    else {
        out_string += lineOutputForSensitivity(input_dict, data);
    }
    // Copy HTML string we've built up to the output element on the page
    line_output.innerHTML = out_string;
    outputInput(data["calculator_state"]);
}
function lineOutputForIntegrationTime(input_dict, data) {
    var out_string = "";
    out_string += "<div class='table-wrapper'><div class='row' style='border-bottom: 1px solid rgba(0, 0, 0, 0.3);'>";
    out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content header-text'>Weather</div>";
    out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content header-text'>ZoomID</div>";
    out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content header-text'>Zoom Noise</div>";
    out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content header-text'>Zoom Centre</div>";
    out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content header-text'>Zoom Resolution</div>";
    out_string += "<div class='col-lg-1 col-xl-1 col-md-1 column-content header-text'>PWV</div>";
    out_string += "<div class='col-lg-1 col-xl-1 col-md-1 column-content header-text'>Elevation</div>";
    out_string += "</div>";
    // sort the results in order of increasing PWV
    var datamap = sortResults(data);
    // format the results in turn
    for (var k2 in datamap) {
        var key = datamap[k2][0];
        out_string += "<div class='row row-padding'>";
        out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content row-text'>" + key + "</div>";
        out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content row-text'>";
        for (var i = 0; i < input_dict.zoom_freqs_scaled.length; i++) {
            if (input_dict.zoom_freqs_scaled[i] != null) {
                out_string += "<span class='margin-right'>" + (i + 1) + "<br> </span>";
            }
        }
        out_string += "</div>";
        out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content row-text'>";
        for (var i = 0; i < input_dict.zoom_freqs_scaled.length; i++) {
            if (input_dict.zoom_freqs_scaled[i] != null) {
                out_string += "<span class='margin-right'>" + data[key]["zoom_sensitivities"][i] + "<br> </span>";
            }
        }
        out_string += "</div>";
        out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content row-text'>";
        for (var i = 0; i < input_dict.zoom_freqs_scaled.length; i++) {
            if (input_dict.zoom_freqs_scaled[i] != null) {
                out_string += "<span class='margin-right'>" + input_dict.zoom_freqs[i] + " " + input_dict.zoom_freq_units[i] + "<br> </span>";
            }
        }
        out_string += "</div>";
        out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content row-text'>";
        for (var i = 0; i < input_dict.zoom_freqs_scaled.length; i++) {
            if (input_dict.zoom_freqs_scaled[i] != null) {
                out_string += "<span class='margin-right'>" + String(input_dict.zoom_resolutions[i] / 1000.0) + " kHz<br> </span>";
            }
        }
        out_string += "</div>";
        out_string += "<div class='col-lg-1 col-xl-1 col-md-1 column-content row-text'>" + (data[key]["calculator_state"]["pwv"] == undefined ? 'null' : data[key]["calculator_state"]["pwv"]) + "</div>";
        out_string += "<div class='col-lg-1 col-xl-1 col-md-1 column-content row-text'>" + (data[key]["calculator_state"]["elevation"] || 'null') + "</div>";
        out_string += "</div>";
    }
    out_string += "</div></br></br><div>";
    out_string += "<p>The integration time is " + (input_dict.main_int_time == null ? String(input_dict.line_int_time) + String(input_dict.line_int_time_units) : String(input_dict.main_int_time) + String(input_dict.main_int_time_units)) + " .</p></div>";
    return out_string;
}
function lineOutputForSensitivity(input_dict, data) {
    var out_string = "";
    out_string += "<div class='table-wrapper'><div class='row' style='border-bottom: 1px solid rgba(0, 0, 0, 0.3);'>";
    out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content header-text'>Weather</div>";
    out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content header-text'>ZoomID</div>";
    out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content header-text'>Zoom Int.Time</div>";
    out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content header-text'>Zoom Centre</div>";
    out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content header-text'>Zoom Resolution</div>";
    out_string += "<div class='col-lg-1 col-xl-1 col-md-1 column-content header-text'>PWV</div>";
    out_string += "<div class='col-lg-1 col-xl-1 col-md-1 column-content header-text'>Elevation</div>";
    out_string += "</div>";
    // sort the results in order of increasing PWV
    var datamap = sortResults(data);
    // format the results in turn
    for (var k2 in datamap) {
        var key = datamap[k2][0];
        out_string += "<div class='row row-padding'>";
        out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content row-text'>" + key + "</div>";
        out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content row-text'>";
        for (var i = 0; i < input_dict.zoom_freqs_scaled.length; i++) {
            if (input_dict.zoom_freqs_scaled[i] != null) {
                out_string += "<span class='margin-right'>" + (i + 1) + "<br> </span>";
            }
        }
        out_string += "</div>";
        out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content row-text'>";
        for (var i = 0; i < input_dict.zoom_freqs_scaled.length; i++) {
            if (input_dict.zoom_freqs_scaled[i] != null) {
                out_string += "<span class='margin-right'>" + data[key]["zoom_int_times"][i] + "<br> </span>";
            }
        }
        out_string += "</div>";
        out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content row-text'>";
        for (var i = 0; i < input_dict.zoom_freqs_scaled.length; i++) {
            if (input_dict.zoom_freqs_scaled[i] != null) {
                out_string += "<span class='margin-right'>" + input_dict.zoom_freqs[i] + " " + input_dict.zoom_freq_units[i] + "<br> </span>";
            }
        }
        out_string += "</div>";
        // out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content row-text'>"+String(input_dict.zoom_resolutions[0] / 1000.0) +" kHz</div>";
        out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content row-text'>";
        for (var i = 0; i < input_dict.zoom_freqs_scaled.length; i++) {
            if (input_dict.zoom_freqs_scaled[i] != null) {
                out_string += "<span class='margin-right'>" + String(input_dict.zoom_resolutions[i] / 1000.0) + " kHz<br> </span>";
            }
        }
        out_string += "</div>";
        out_string += "<div class='col-lg-1 col-xl-1 col-md-1 column-content row-text'>" + (data[key]["calculator_state"]["pwv"] == undefined ? 'null' : data[key]["calculator_state"]["pwv"]) + "</div>";
        out_string += "<div class='col-lg-1 col-xl-1 col-md-1 column-content row-text'>" + (data[key]["calculator_state"]["elevation"] || 'null') + "</div>";
        out_string += "</div>";
    }
    out_string += "</div></br></br><div>";
    out_string += "<p>The target RMS noise is <b> " + String(input_dict.line_sensitivity) + String(input_dict.line_sensitivity_units) + "</b>.</p></div>";
    return out_string;
}
// Function to render the pulsars output report to the page (Not yet implemented, just left as an example)
/* eslint-disable */ // turns off lint warning for no-unused-vars for input_dict and data
function outputPulsars(input_dict, data) {
    return 0;
}
/* eslint-enable */
// Function which decides, based on active observing modes, which outputs need to be rendered
function updateOutput(input_dict, data) {
    console.log('updateOutput');
    // Get output element and reveal it
    var cont_output = document.getElementById("output");
    cont_output.classList.remove("hidden");
    // Begin building up output HTML string
    var out_string = "";
    console.log(data);
    var key = "sensitivity";
    out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content row-text'>" + data[key] + "</div>";
    // Copy HTML string we've built up to the output element on the page
    cont_output.innerHTML = out_string;
}
// Retrieve subarray configuration list
function retrieveSubarrays() {
    $.ajax({
        url: '/subarrays',
        type: 'GET',
        success: function (data) {
            populateDropdown(data);
        }
    });
}
// Function to populate the dropdown menu.
function populateDropdown(data) {
    var dropdownElementHolder = document.getElementById("subarrays-dropdown");
    var dropdownDefault = dropdownElementHolder.innerHTML;
    var dropdown = "";
    data.forEach(function (subarray, index) {
        var entry = "<a class=\"dropdown-item array-config-option\" href=\"#\" " +
            "onclick=\"event.preventDefault(); updateDropdown('array-config', '" +
            subarray + "')\">" + subarray + "</a>\n";
        // Check that the placeholder subarray entered in AT2-606 is removed when necessary
        if (subarray !== "custom") {
            dropdown += entry;
        }
    });
    dropdown += dropdownDefault;
    dropdownElementHolder.innerHTML = dropdown;
}
// Function to update text on dropdown button when an option is selected.
function updateDropdown(field, label) {
    document.getElementById("dropdown-button-" + field).textContent = label;
    if ((field === "array-config") && (label === "custom")) {
        document.getElementById("nSKA-input").disabled = false;
        document.getElementById("nMeer-input").disabled = false;
    }
    else if ((field === "array-config") && (label !== "custom")) {
        document.getElementById("nSKA-input").disabled = true;
        document.getElementById("nMeer-input").disabled = true;
    }
}
// Function used in the internal version to reveal hidden inputs when needed.
// perhaps better to be implemented in the html with bootstrap in future
// function revealInputs(field: string): void {
// 	//const dependents = [];
// 	switch (field) {
// 		case "Tsys_SKA" || "Tsys_Meer":
// 			// hide the option to change the weather
// 			document.getElementById("row-weather").classList.add("d-none");
// 			break;
// 		case "Tsky":
// 			// hide the option to change the weather
// 			document.getElementById("row-weather").classList.add("d-none");
// 			break;
// 		case "Tgal":
// 			// Reveal the option to change the weather
// 			document.getElementById("row-weather").classList.remove("d-none");
// 			break;
// 	}
// }
//
// // Function used in the internal version to hide visible inputs when needed
// function hideInputs(field: string): void {
// 	//const dependents = [];
// 	switch (field) {
// 		case "Tsys_SKA":
// 			// Reveal the option to change the weather
// 			document.getElementById("row-weather").classList.remove("d-none");
// 			break;
// 		case "Tsky":
// 			// Also want to reveal the option to change the weather
// 			document.getElementById("row-weather").classList.add("d-none");
// 			break;
// 		case "Tgal":
// 			// Reveal the option to change the weather
// 			document.getElementById("row-weather").classList.add("d-none");
// 			break;
// 	}
// }
// This function is clears the input of the fields that have disabled by enabling another field. It also updates the
// check boxes and disables the fields
function updateDisabledCheckboxes(fields) {
    for (var item in fields) {
        document.getElementById(fields[item] + "-input").disabled = true;
        document.getElementById("checkbox-" + fields[item]).textContent = "Enter Manually";
    }
}
// Function used in the internal version to disable inputs when needed
function disableInputs(field) {
    if (field == "Tsys_SKA") {
        updateDisabledCheckboxes(["Trcv_SKA", "Tspl_SKA", "Tsky", "Tgal", "alpha"]);
    }
    if (field === "Trcv_SKA" || field === "Tspl_SKA" || field === "Tsky") {
        updateDisabledCheckboxes(["Tsys_SKA"]);
    }
    if (field === "Tsys_Meer") {
        updateDisabledCheckboxes(["Trcv_Meer", "Tspl_Meer", "Tsky", "Tgal", "alpha"]);
    }
    if (field === "Trcv_Meer" || field === "Tspl_Meer" || field === "Tsky") {
        updateDisabledCheckboxes(["Tsys_Meer"]);
    }
    if (field === "Tgal") {
        updateDisabledCheckboxes(["Tsys_SKA", "Tsys_Meer", "Tsky", "alpha"]);
    }
    if (field === "Tsky") {
        updateDisabledCheckboxes(["Tgal", "alpha"]);
    }
    if (field === "alpha") {
        updateDisabledCheckboxes(["Tsys_SKA", "Tsys_Meer", "Tsky", "Tgal"]);
    }
}
// If "Enter Manually" is clicked, swap that element on the page to say "Calculate Automatically" and vice-versa
/* eslint-disable */
// all of the following functions trigger no-unused-var warnings in eslint. disabling these for now ahead of refactoring
function updateCheckbox(field) {
    if (document.getElementById("checkbox-" + field).textContent.trim() === "Enter Manually") {
        document.getElementById("checkbox-" + field).textContent = "Calculate Automatically";
        document.getElementById(field + "-input").disabled = false;
        // revealInputs(field);
        disableInputs(field);
    }
    else {
        document.getElementById("checkbox-" + field).textContent = "Enter Manually";
        document.getElementById(field + "-input").disabled = true;
        // hideInputs(field);
    }
}
// Function added by Liz as a proof of concept. It probably needs refactoring
function outputInput(data) {
    for (var variable in data) {
        var value = String(data[variable]);
        document.getElementById(variable + "-input").value = value;
    }
}
// When the observing band is changed, we update any frequency/bandwidth options to some defaults within that band.
// For bands 1 and 2, the user is offered the entire band by default
function updateBandSelection(selected_band) {
    var cont_freq_input = document.getElementById("continuum-frequency-input");
    var cont_band_input = document.getElementById("continuum-bandwidth-input");
    var zoom_freq_inputs = [
        document.getElementById("zoom1-frequency-input"),
        document.getElementById("zoom2-frequency-input"),
        document.getElementById("zoom3-frequency-input"),
        document.getElementById("zoom4-frequency-input"),
    ];
    switch (selected_band) {
        case '1':
            cont_freq_input.value = "0.7";
            cont_band_input.value = "0.7";
            for (var i = 0; i < zoom_freq_inputs.length; i++) {
                if (zoom_freq_inputs[i].value != "" && !zoom_freq_inputs[i].disabled) {
                    zoom_freq_inputs[i].value = "0.7";
                }
            }
            break;
        case '2':
            cont_freq_input.value = "1.35";
            cont_band_input.value = "0.81";
            for (var i = 0; i < zoom_freq_inputs.length; i++) {
                if (zoom_freq_inputs[i].value != "" && !zoom_freq_inputs[i].disabled) {
                    zoom_freq_inputs[i].value = "1.35";
                }
            }
            break;
        case '5a':
            cont_freq_input.value = "6.5";
            cont_band_input.value = "0.8";
            for (var i = 0; i < zoom_freq_inputs.length; i++) {
                if (zoom_freq_inputs[i].value != "" && !zoom_freq_inputs[i].disabled) {
                    zoom_freq_inputs[i].value = "6.5";
                }
            }
            break;
        case '5b':
            cont_freq_input.value = "11.9";
            cont_band_input.value = "0.8";
            for (var i = 0; i < zoom_freq_inputs.length; i++) {
                if (zoom_freq_inputs[i].value != "" && !zoom_freq_inputs[i].disabled) {
                    zoom_freq_inputs[i].value = "11.9";
                }
            }
            break;
    }
}
// When a change is detected to a zoom text input, this function handles which of those inputs should currently be enabled/disabled.
function manageActiveZooms(zoom_num) {
    var changed_input = document.getElementById("zoom" + String(zoom_num) + "-frequency-input");
    if (changed_input.value == "") {
        var i = void 0;
        for (i = zoom_num + 1; i <= 4; i++) {
            document.getElementById("zoom" + String(i) + "-frequency-input").disabled = true;
            document.getElementById("dropdown-button-zoom" + String(i) + "-frequency").disabled = true;
            document.getElementById("dropdown-button-zoom" + String(i) + "-resolution").disabled = true;
        }
    }
    else {
        if (zoom_num < 4) {
            document.getElementById("zoom" + String(zoom_num + 1) + "-frequency-input").disabled = false;
            document.getElementById("dropdown-button-zoom" + String(zoom_num + 1) + "-frequency").disabled = false;
            document.getElementById("dropdown-button-zoom" + String(zoom_num + 1) + "-resolution").disabled = false;
            manageActiveZooms(zoom_num + 1);
        }
    }
}
// When one of the inputs is changed, this function is called to run the validation.
// This is helpful to the user, as they can see if they've made an error immediately after changing an input.
function updateForm() {
    var observing_modes = getObservingModes();
    var input_dict = readForm();
    validateInput(input_dict, observing_modes);
}
// For the observing mode cards, when the header is clicked to expand/collapse, swap between a plus/minus to suit
function swapPlusMinus(card_link_id) {
    var card_link_element = document.getElementById("card-link-" + card_link_id);
    var collapse_element = document.getElementById("collapse-" + card_link_id);
    // Assuming the card is not already in the "collapsing" state, swap the +/-
    if (!collapse_element.classList.contains("collapsing")) {
        if (card_link_element.textContent.trim()[0] == "+") {
            card_link_element.textContent = card_link_element.textContent.replace("+", "-");
        }
        else {
            card_link_element.textContent = card_link_element.textContent.replace("-", "+");
        }
    }
}
// Function to swap which of the sensitivity/integration inputs is disabled/enabled for a given card.
function setInputs(name, card) {
    var sens_input = document.getElementById(card + "-sensitivity-input");
    var time_input = document.getElementById(card + "-integration-input");
    switch (name) {
        case 'Integration':
            sens_input.disabled = true;
            time_input.disabled = false;
            break;
        case 'Sensitivity':
            sens_input.disabled = false;
            time_input.disabled = true;
            break;
        default:
            console.log('oops');
    }
}
/*eslint-enable */
