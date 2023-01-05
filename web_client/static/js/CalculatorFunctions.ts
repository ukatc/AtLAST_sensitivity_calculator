//import $ from "jquery";

// === ON SUBMIT === //
// This code will run when the "Calculate" button is clicked.
// Capture and disable form submission. If there are invalid fields, present invalid feedback to the user, otherwise perform calculation.
(function (): void {
    'use strict';
    window.addEventListener('load', function () {
        // Get the forms we want to add validation styles to
        const forms = document.getElementsByClassName('needs-validation');
        // Loop over them (There will only be the one form)
        /* eslint-disable */
        const validation = Array.prototype.filter.call(forms, function (form) {
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
                let input_dict = readForm();
                console.log('after');
                console.log(input_dict);

                // Using AJAX, make a GET request to the '/calc' Flask route in calculate.py
                $.ajax({url: '/v1/sensitivity',
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

// functions to facilitate validating inputs

function isNumeric(val: any): boolean {
    return !(val instanceof Array) && (val - parseFloat(val) + 1) >= 0;
}

function parseRA(RA: string): boolean {
    return (/^\d{1,2}:\d{1,2}:\d+(\.\d+)?$/.test(RA));
}

function parseDec(Dec: string): boolean {
    return (/[-+]\d{1,2}:\d{1,2}:\d+(\.\d+)?$/.test(Dec));
}

// Validate a frequency input, making sure it is not empty and is a number.
function validateObsFreq(field: string, obs_freq: string | number, obs_freq_scaled: string, obs_band: string): boolean {
    const frequency_feedback = <HTMLInputElement>document.getElementById(field + "-invalid");
    const frequency_input = <HTMLInputElement>document.getElementById(field + "-input");
    if (!isNumeric(obs_freq) || obs_freq == "") {
        frequency_feedback.textContent = "Please enter a number";
        frequency_feedback.style.display = "block";
        frequency_input.setCustomValidity("Invalid Field.");
        return false;
    } else {
    }
    return true;
}

// Validate a bandwidth input, making sure it is not empty and is a number.
function validateBandwidth(field: string, bandwidth: string | number, bandwidth_scaled: string, obs_freq_scaled: string, obs_band: string): boolean {
    const bandwidth_feedback = document.getElementById(field + "-invalid");
    const bandwidth_input = <HTMLInputElement>document.getElementById(field + "-input");
    if (!isNumeric(bandwidth) || bandwidth == "") {
        bandwidth_feedback.textContent = "Please enter a number";
        bandwidth_feedback.style.display = "block";
        bandwidth_input.setCustomValidity("Invalid Field.");
        return false;
    }
    return true;
}

// function to convert Sexagesimal declination to decimal for source validation

function Sexa2Dec(Dec: string): number {
    const DecSplit = Dec.split(':', 3)

    if (Number(DecSplit[0]) < 0) {
        return (Number(DecSplit[0]) -  Number(DecSplit[1]) / 60 - Number(DecSplit[2]) / 3600)
    } else {
        return (Number(DecSplit[0]) +  Number(DecSplit[1]) / 60 + Number(DecSplit[2]) / 3600)
    }
}

function isAboveHorizon(Dec: string): boolean {
    // this is a very coarse way to do this validation. Review in future.
    const SkaLatitude = Sexa2Dec("-30:43:16.068")
    if (Sexa2Dec(Dec) < 90.0 + SkaLatitude) {
        return true
    }
    return false
}

// Validate right ascension input
function validateRA(coords: string): boolean {
    const feedback = document.getElementById("RA-invalid");
    const input = <HTMLInputElement>document.getElementById("RA-input");

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
function validateDec(coords:string): boolean {
    const feedback = document.getElementById("dec-invalid");
    const input = <HTMLInputElement>document.getElementById("dec-input");
    if (!parseDec(coords)) {
        feedback.textContent = "Input formatted incorrectly.";
        feedback.style.display = "block";
        input.setCustomValidity("Invalid Field.");
        return false;
    } else if (!isAboveHorizon(coords)) {
        feedback.textContent = "Target is never above the horizon";
        feedback.style.display = "block";
        input.setCustomValidity("Invalid Field.");
        return false
    }

    feedback.style.display = "none";
    input.setCustomValidity("");
    return true;
}

// Validate a given eta input, making sure it is not empty and is a number
function validateEta(field: string, value: string | number): boolean {
    const feedback = document.getElementById(field + "-invalid");
    const input = <HTMLInputElement>document.getElementById(field + "-input");

    if (input.disabled) {
        feedback.style.display = "none";
        input.setCustomValidity("");
    } else {
        if (!isNumeric(value) || value == "") {
            feedback.textContent = "Please enter a number";
            feedback.style.display = "block";
            input.setCustomValidity("Invalid Field.");
            return false;
        } else {
            if (value <= 0 || value > 1) {
                feedback.textContent = "Value must be between 0 and 1";
                feedback.style.display = "block";
                input.setCustomValidity("Invalid Field.");
                return false;
            } else {
                feedback.style.display = "none";
                input.setCustomValidity("");
            }
        }
    }
    return true;
}

// General function to validate an input that needs no special treatment
function validateGeneral(field: string, value: string | number): boolean {
    const feedback = document.getElementById(field + "-invalid");
    const input = <HTMLInputElement>document.getElementById(field + "-input");
    if (input.disabled) {
        feedback.style.display = "none";
        input.setCustomValidity("");
    } else {
        if (!isNumeric(value) || value == "") {
            feedback.textContent = "Please enter a number";
            feedback.style.display = "block";
            input.setCustomValidity("Invalid Field.");
            return false;
        } else {
            if (value <= 0) {
                feedback.textContent = "Value must be greater than 0";
                feedback.style.display = "block";
                input.setCustomValidity("Invalid Field.");
                return false;
            } else {
                feedback.style.display = "none";
                input.setCustomValidity("");
            }
        }
    }
    return true;
}

function validateInteger(field: string, value: number | string): boolean {
    const feedback = document.getElementById(field + "-invalid");
    const input = <HTMLInputElement>document.getElementById(field + "-input");
    if (input.disabled) {
        feedback.style.display = "none";
        input.setCustomValidity("");
    } else {
        if (!isNumeric(value) || value == "") {
            feedback.textContent = "Please enter a number";
            feedback.style.display = "block";

            input.setCustomValidity("Invalid Field.");
            return false;
        } else {
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
function validateNumberMinMax(field: string, value: string, min: number, max: number): boolean {
    const feedback = document.getElementById(field + "-invalid");
    const input = <HTMLInputElement>document.getElementById(field + "-input");

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

    const numval = parseFloat(value);
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
function validateInput(input_dict,observing_modes: { [x: string]: boolean; continuum: boolean;
line: boolean; pulsars: boolean; }): boolean {
    // This will be set to false if there are any issues
    let return_bool = true;

    // --- Universal Inputs --- //
    return_bool = return_bool && validateRA(input_dict.right_asc);
    return_bool = return_bool && validateDec(input_dict.dec);
    return_bool = return_bool && validateInteger("nMeer", input_dict.nMeer);
    return_bool = return_bool && validateInteger("nSKA", input_dict.nSKA);
    return_bool = return_bool && validateNumberMinMax("pwv", input_dict.weather, 3, 25);
    return_bool = return_bool && validateNumberMinMax("elev", input_dict.elevation, 5, 90);

    // If we're using the internal version, we want to check these extra inputs
    if (input_dict.calculator_mode === "Internal") {
        return_bool = return_bool && validateEta("etaPointing", input_dict.etaPointing)
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
    } else {
        document.getElementById("main-integration-invalid").style.display = "none";
        (<HTMLInputElement>document.getElementById("main-integration-input")).setCustomValidity("");
    }

    // --- Continuum Inputs --- //
    if (observing_modes["continuum"]) {
        return_bool = return_bool && validateObsFreq("continuum-frequency", input_dict.continuum_obs_freq, input_dict.continuum_obs_freq_scaled, input_dict.obs_band);
        return_bool = return_bool && validateBandwidth("continuum-bandwidth", input_dict.continuum_bandwidth, input_dict.continuum_bandwidth_scaled, input_dict.continuum_obs_freq_scaled, input_dict.obs_band);
        return_bool = return_bool && validateGeneral("continuum-chunks", input_dict.continuum_n_chunks)

        // Only want to validate one of either integration or sensitivity
        if (input_dict.continuum_supplied == "IntegrationTime") {
            return_bool = return_bool && validateGeneral("continuum-integration", input_dict.continuum_int_time);
        } else {
            return_bool = return_bool && validateGeneral("continuum-sensitivity", input_dict.continuum_sensitivity);
        }
    } else {
        // If Continuum is not an active observing mode, we ignore these inputs and assume they're all fine
        document.getElementById("continuum-frequency-invalid").style.display = "none";
        (<HTMLInputElement>document.getElementById("continuum-frequency-input")).setCustomValidity("");

        document.getElementById("continuum-bandwidth-invalid").style.display = "none";
        (<HTMLInputElement>document.getElementById("continuum-bandwidth-input")).setCustomValidity("");

        document.getElementById("continuum-chunks-invalid").style.display = "none";
        (<HTMLInputElement>document.getElementById("continuum-chunks-input")).setCustomValidity("");

        document.getElementById("continuum-integration-invalid").style.display = "none";
        (<HTMLInputElement>document.getElementById("continuum-integration-input")).setCustomValidity("");

        document.getElementById("continuum-sensitivity-invalid").style.display = "none";
        (<HTMLInputElement>document.getElementById("continuum-sensitivity-input")).setCustomValidity("");
    }

    return return_bool;
}

// This function is a utility used in the readForm function when using internal mode. Updated by Liz to make the value
// null if the element is disabled, rather than capturing what's in the field.

function getElementValueOrNull(element_id: string, ): string | null {
    if ((<HTMLInputElement>document.getElementById(element_id)).disabled) {
        return  null
    } else {
        const temp = (<HTMLInputElement>document.getElementById(element_id)).value.trim();
        if (temp.length === 0) {
            return null
        } else {
            return temp
        }
    }
}

// This function scans through the page and collects the values, units, etc from every input
function readForm() {
    // --- Universal Inputs --- //

    const elev = (<HTMLInputElement>document.getElementById("elev-input")).value.trim();
    const obs_freq = (<HTMLInputElement>document.getElementById("obs-freq-input")).value.trim();
    const bandwidth = (<HTMLInputElement>document.getElementById("bandwidth-input")).value.trim();
    const pwv = (<HTMLInputElement>document.getElementById("pwv-input")).value.trim();
    const npol = (<HTMLInputElement>document.getElementById("npol-input")).value.trim();
    const Trx = (<HTMLInputElement>document.getElementById("Trx-input")).value.trim();
    const Tamb = (<HTMLInputElement>document.getElementById("Tamb-input")).value.trim();
    const g = (<HTMLInputElement>document.getElementById("g-input")).value.trim();
    const eta_eff = (<HTMLInputElement>document.getElementById("eta-eff-input")).value.trim();
    const eta_ill = (<HTMLInputElement>document.getElementById("eta-ill-input")).value.trim();
    const eta_g = (<HTMLInputElement>document.getElementById("eta-g-input")).value.trim();

    const integration_time_disabled = (<HTMLInputElement>document.getElementById("integration-time-input")).disabled;
    console.log(integration_time_disabled);
    const integration_time = (<HTMLInputElement>document.getElementById("integration-time-input")).value.trim();
    console.log(integration_time);
    let sensitivity_disabled = (<HTMLInputElement>document.getElementById("sensitivity-input")).disabled;
    console.log(sensitivity_disabled);
    const sensitivity = (<HTMLInputElement>document.getElementById("sensitivity-input")).value.trim();
    console.log(sensitivity);

    // Gather values into a dictionary and return
    const return_dict = {
        "elevation": elev,
        "obs_freq": obs_freq,
        "bandwidth": bandwidth,
        "pwv": pwv,
        "npol": npol,
        "Trx": Trx,
        "Tamb": Tamb,
        "g": g,
        "eta_eff": eta_eff,
        "eta_ill": eta_ill,
        "eta_g": eta_g,
    }

    // It's not supposed to but the form starts up with neither 
    // input disabled. In this case, disable sensitivity.
    if (!sensitivity_disabled && !integration_time_disabled) {
        console.log('oops 2');
        (<HTMLInputElement>document.getElementById("sensitivity-input")).disabled = true;
        sensitivity_disabled = (<HTMLInputElement>document.getElementById("sensitivity-input")).disabled;
    }

    // Now decide if the user has set integration time or sensitivity
    if (sensitivity_disabled) {
        return_dict["integration_time"] = integration_time;
    }
    if (integration_time_disabled) {
        return_dict["sensitivity"] = sensitivity;
    }
    if (sensitivity_disabled && integration_time_disabled) {
        console.log('oops 1');
    }
    if (!sensitivity_disabled && !integration_time_disabled) {
        console.log('oops 3');
    }

    console.log('readForm');
    console.log(return_dict)
    return return_dict
}

// Function to find which observing modes are currently active
function getObservingModes(): { [x: string]: boolean; continuum: boolean; line: boolean; pulsars: boolean; } {
    return {
        "continuum": document.getElementById("collapse-continuum").classList.contains("show"),
        "line": document.getElementById("collapse-line").classList.contains("show"),
        "pulsars": document.getElementById("collapse-pulsars").classList.contains("show")
    }
}

// Function to sort the results object keys in order of decreasing PWV
function sortResults(data){
	
    // Assemble a list of [key,pwv] pairs
    let keyval: [string, string];
    const datamap: Array<typeof keyval> = [];
    for (const k in data)
    {
        const pwv = !("calculator_state" in data[k]) ? null 
             : !("pwv" in data[k]["calculator_state"]) ? null
             : data[k]["calculator_state"]["pwv"];
        datamap.push([k, pwv]);
    }

    // Sort the list in decreasing PWV
    datamap.sort(function(a, b) {
        const pwv_a = a[1];
        const pwv_b = b[1];
        if (pwv_a == null) {
            return 0;
        }
        if (pwv_b == null) {
            return 0;
        }
        const pwv_a_float = parseFloat(pwv_a);
        const pwv_b_float = parseFloat(pwv_b);
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


function continuumOutputForSensitivity(input_dict, data){

    let out_string = '';

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

    const datamap = sortResults(data);

    // format the results in turn

    for (const k2 in datamap) {
        const key = datamap[k2][0];

        out_string += "<div class='row row-padding'>";
        out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content row-text'>"+key+"</div>";			
        out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content row-text'>"+data[key]["cont_int_time"]+"</div>";
        out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content row-text'>";
        for(let i = 0; i < data[key]["chunk_int_times"].length; i++){
            out_string += "<span class='margin-right'>"+data[key]["chunk_int_times"][i]+" <br> </span>"		
        }
        out_string += "</div>";
        out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content row-text'>";
        for(let i = 0; i < data[key]["chunk_centres"].length; i++){
            out_string += "<span class='margin-right'>"+data[key]["chunk_centres"][i]+" <br> </span>"		
        }
        out_string += "</div>";	
        out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content row-text'>"+data[key]["cont_line_int_time"]+"</div>";
        out_string += "<div class='col-lg-1 col-xl-1 col-md-1 column-content row-text'>"+(data[key]["calculator_state"]["pwv"]==undefined ? 'null' : data[key]["calculator_state"]["pwv"])+"</div>";
        out_string += "<div class='col-lg-1 col-xl-1 col-md-1 column-content row-text'>"+(data[key]["calculator_state"]["elevation"] || 'null')+"</div>";		
        out_string += "</div>";			
    }
    out_string+="</div></br><div>";	
    out_string += "<p>The target RMS noise is <b> "+String(input_dict.continuum_sensitivity) + String(input_dict.continuum_sensitivity_units) + "</b></p>"; 
    if (input_dict.continuum_n_chunks > 1) {
        out_string += "<p>The band is divided into <b>" + String(input_dict.continuum_n_chunks) + "</b> chunks, each <b>" + String(data[Object.keys(data)[0]]["chunk_width"]) + " </b>wide.</p>";
    }
    out_string += "<p>The line int. time is for the central frequency (<b>" + String(input_dict.continuum_obs_freq) + String(input_dict.continuum_obs_freq_units)
    out_string += "</b>) , with a resolution of <b>" + String(input_dict.continuum_resolution / 1000.0) + "kHz</b></p></div>"	
    return out_string
}

function continuumOutputForIntegrationTime(input_dict, data): string {
	
    let out_string = '';

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

    const datamap = sortResults(data);

    // format the results in turn

    for (const k2 in datamap) {
        const key = datamap[k2][0];
        out_string += "<div class='row row-padding'>";
        out_string += "<div class='col-lg-1 col-xl-1 col-md-1 column-content row-text'>"+key+"</div>";			
        out_string += "<div class='col-lg-1 col-xl-1 col-md-1 column-content row-text'>"+(input_dict.main_int_time == null ? String(input_dict.continuum_int_time) + String(input_dict.continuum_int_time_units) : String(input_dict.main_int_time) + String(input_dict.main_int_time_units))+"</div>";
        out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content row-text'>"+data[key]["cont_sens"]+"</div>";
        out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content row-text'>";
        for(let i =0; i < data[key]["chunk_sensitivities"].length;i++){
            out_string += "<span class='margin-right'>"+data[key]["chunk_sensitivities"][i]+" <br> </span>";
        }
        out_string += "</div>";
        out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content row-text'>";
        for(let i =0; i < data[key]["chunk_centres"].length;i++){
            out_string += "<span class='margin-right'>"+data[key]["chunk_centres"][i]+" <br> </span>";	
        }
        out_string += "</div>";	
        out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content row-text'>"+data[key]["cont_line_sens"]+"</div>";
        out_string += "<div class='col-lg-1 col-xl-1 col-md-1 column-content row-text'>"+(data[key]["calculator_state"]["pwv"]==undefined ? 'null' : data[key]["calculator_state"]["pwv"])+"</div>";
        out_string += "<div class='col-lg-1 col-xl-1 col-md-1 column-content row-text'>"+(data[key]["calculator_state"]["elevation"] || 'null')+"</div>";
        out_string += "</div>";
    }
    out_string+="</div></br></br><div>";
    if (input_dict.continuum_n_chunks > 1) {
        out_string += "<p>Dividing the bandwidth into <b>" + String(input_dict.continuum_n_chunks) + ", " + String(data[Object.keys(data)[0]]["chunk_width"]) + " </b>chunks.</p>";
    }
    out_string += "<p>The Line noise is at the central frequency of (<b>" + String(input_dict.continuum_obs_freq) + String(input_dict.continuum_obs_freq_units);
    out_string += "</b>) , with a resolution of <b>" + String(input_dict.continuum_resolution / 1000.0) + "kHz</b></p></div>";
    return out_string;
}

/* eslint-enable */

// Function which decides, based on active observing modes, which outputs need to be rendered
function updateOutput(input_dict, data): void {
    console.log('updateOutput');

    // Get output element and reveal it
    const cont_output = document.getElementById("output");
    cont_output.classList.remove("hidden");

    // Begin building up output HTML string
    let out_string = "";	
        console.log(data)

    if ("sensitivity" in data) {
        out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content row-text'>"+data['sensitivity']+"</div>";
    } else if ("integration_time" in data) {
        out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content row-text'>"+data['integration_time']+"</div>";
    } else {
        out_string += "<div class='col-lg-2 col-xl-2 col-md-2 column-content row-text'>uncoded response</div>";
    }

    // Copy HTML string we've built up to the output element on the page
    cont_output.innerHTML = out_string;
}

function updateDisabledCheckboxes(fields: string[]): void {
    for (const item in fields) {
        (<HTMLInputElement>document.getElementById(fields[item] +  "-input")).disabled = true;
        document.getElementById("checkbox-" + fields[item]).textContent = "Enter Manually";
    }
}

// Function used in the internal version to disable inputs when needed
function disableInputs(field: string): void {
    if (field == "Tsys_SKA" ) {
        updateDisabledCheckboxes(["Trcv_SKA", "Tspl_SKA", "Tsky", "Tgal", "alpha"])
    }
    if (field === "Trcv_SKA" || field === "Tspl_SKA" || field === "Tsky") {
        updateDisabledCheckboxes(["Tsys_SKA"])
    }
    if (field === "Tsys_Meer" ) {
        updateDisabledCheckboxes(["Trcv_Meer", "Tspl_Meer", "Tsky", "Tgal", "alpha"])
    }
    if (field === "Trcv_Meer" || field === "Tspl_Meer" || field === "Tsky") {
        updateDisabledCheckboxes(["Tsys_Meer"])
    }
    if (field === "Tgal") {
        updateDisabledCheckboxes(["Tsys_SKA", "Tsys_Meer", "Tsky", "alpha"])
    }
    if (field === "Tsky") {
        updateDisabledCheckboxes(["Tgal", "alpha"])
    }
    if (field === "alpha") {
        updateDisabledCheckboxes(["Tsys_SKA", "Tsys_Meer", "Tsky", "Tgal"])
    }
}

// If "Enter Manually" is clicked, swap that element on the page to say "Calculate Automatically" and vice-versa
/* eslint-disable */
// all of the following functions trigger no-unused-var warnings in eslint. disabling these for now ahead of refactoring
function updateCheckbox(field: string): void {
    if (document.getElementById("checkbox-" + field).textContent.trim() === "Enter Manually") {
        document.getElementById("checkbox-" + field).textContent = "Calculate Automatically";
        (<HTMLInputElement>document.getElementById(field + "-input")).disabled = false;

        // revealInputs(field);
        disableInputs(field);
    } else {
        document.getElementById("checkbox-" + field).textContent = "Enter Manually";
        (<HTMLInputElement>document.getElementById(field + "-input")).disabled = true;

        // hideInputs(field);
    }
}


// Function added by Liz as a proof of concept. It probably needs refactoring

function outputInput(data: Record<string, number>): void {
    for (const variable in data) {
        let value = String(data[variable]);
        (<HTMLInputElement>document.getElementById(variable + "-input")).value = value;
    }
}

// When one of the inputs is changed, this function is called to run the validation.
// This is helpful to the user, as they can see if they've made an error immediately after changing an input.
function updateForm(): void {
    const observing_modes = getObservingModes();
    const input_dict = readForm();

    validateInput(input_dict, observing_modes)
}

// For the observing mode cards, when the header is clicked to expand/collapse, swap between a plus/minus to suit
function swapPlusMinus(card_link_id: string): void {
    const card_link_element = document.getElementById("card-link-" + card_link_id);
    const collapse_element = document.getElementById("collapse-" + card_link_id);

    // Assuming the card is not already in the "collapsing" state, swap the +/-
    if (!collapse_element.classList.contains("collapsing")) {
        if (card_link_element.textContent.trim()[0] == "+") {
            card_link_element.textContent = card_link_element.textContent.replace("+", "-");
        } else {
            card_link_element.textContent = card_link_element.textContent.replace("-", "+");
        }
    }
}

// Function to swap which of the sensitivity/integration inputs is disabled/enabled for a given card.
function setInputs(name: string): void {
    const sens_row = <HTMLInputElement>document.getElementById("row-sensitivity");
    const sens_input = <HTMLInputElement>document.getElementById("sensitivity-input");
    const time_row = <HTMLInputElement>document.getElementById("row-integration-time");
    const time_input = <HTMLInputElement>document.getElementById("integration-time-input");

    switch (name) {

        case 'integration':
            sens_input.disabled = true;
            sens_row.style.display = "none";
            time_input.disabled = false;
            time_row.style.display = "flex";
            break;

        case 'sensitivity':
            sens_input.disabled = false;
            sens_row.style.display = "flex";
            time_input.disabled = true;
            time_row.style.display = "none";
            break;

        default:
            console.log('oops')
    }
}

export {parseRA, parseDec, sortResults};

/*eslint-enable */

