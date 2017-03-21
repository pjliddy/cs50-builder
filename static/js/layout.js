$(function () {
  console.log('layout.js loaded');
});

window.addEventListener("message", handleMessage, false);

function handleMessage(e) {
  console.log('message received');
   if (e.origin == '*') {
     return;
   } else {
     message = e.data;
     varName = Object.keys(message)[0];
     varValue = message[ varName ];
          
     varObj = {
       [varName]: varValue
     };
     
     console.log(varObj);
     less.modifyVars( varObj );
     less.refreshStyles();
   }
};


