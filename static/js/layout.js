$(function () {
  console.log('layout.js loaded');
});

window.addEventListener("message", handleMessage, false);

function handleMessage(e) {
  console.log('message received: ' + e.data);
   if (e.origin == '*') {
     return;
   } else {
     
//     message = e.data;
//     varName = Object.keys(message)[0];
//     varValue = message[ varName ];
//          
//     varObj = {
//       [varName]: varValue
//     };
     
     
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
            
//            for (var i in response){
//              var obj = response[i];
//              varName = obj.name;
//              varValue = obj.output;
//              
//              vars[varName] = varValue;
//            }
            
            console.log(vars);
            less.modifyVars( vars );
            less.refreshStyles();
          },
          error: function(error) {
              console.log('error: ' + error);
          }
        });
      }
                 
      
     
//     console.log(varObj);
//     less.modifyVars( varObj );
//     less.refreshStyles();
   }
};


