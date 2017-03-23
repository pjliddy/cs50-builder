$(function () {
  console.log('layout.js loaded');
});

window.addEventListener("message", handleMessage, false);

function handleMessage(e) {
  console.log('message received: ' + e.data);
  if (e.origin == '*') {
   return;
  } else {
    if (e.data == 'updateVars') {
      $.ajax({
        url: '/getvars',
        type: 'POST',
        success: function(response) {
          // console.log('response: ' + response);
          varObjs = response;
          var vars = new Object;

          $.each( varObjs, function( i, varObj ) {
            vars['@' + varObj.name] = varObj.output;
          });

          console.log(vars);
          less.modifyVars( vars );
          less.refreshStyles();
        },
        error: function(error) {
            console.log('error: ' + error);
        }
      });
    }
  }
};


