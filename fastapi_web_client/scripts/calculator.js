// window.addEventListener("load", () => {
//     console.log($);
// });

$(document).ready(() => {
   const validateInput = (param_input) => {
       // TODO: validate the input
       console.log('validating...', param_input.value);
   }

   const highlightRecalculate = () => {
       // TODO: do I really want to do this?
   }

   const do_calculation = () => {
       // TODO: submit the request to do the calculation
   }

   // TODO: pick up from here/
    //      Need to make sure we have all the values and units before enabling editing and validation
   const get_param_values_units = () => {
       // Get the defaults and allowed values/units for each param
       $.ajax({ url: '/v1/param-values-units',
           type: 'GET',
           success: function (data) {
                console.log('finished');
               console.log(data);
           }
       });
   }

   // window.addEventListener('load', () => {
   get_param_values_units();
   // Validate user input (and highlight recalc?) on all input
   // fields
   const allUserInput = document.querySelectorAll(".param-input");
   console.log(allUserInput);

   allUserInput.forEach(input => {
       // Add the placeholder text
       input.setAttribute("placeholder", "Enter a value...");

       input.addEventListener("input", e => {
           if (input === e.target) {
               validateInput(input);
           }
       })
   });
   // });
});