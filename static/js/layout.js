$(function () {
  console.log('layout.js loaded');
});

function handleMessage(e) {
  console.log('message received');
   if (e.origin == '*') {
     return;
   } else {
     message = e.data;
//     message = JSON.stringify(e.data);
//     data = JSON.parse(message);
     
//     data = jQuery.parseJSON( message );
     data = {};
     
     varName = Object.keys(message)[0];
     varValue = message[ varName ];
     
     data[String(varName)] = varValue;
     
     varObj = {
       [varName]: varValue
     };
     
     console.log(varObj);
     less.modifyVars( varObj );
     less.refreshStyles();
   }
};

window.addEventListener("message", handleMessage, false);

//function updateVar( evt ) { 
//  var fields = $("form").serializeArray();
//  var variables = new Object;
//  
//  $.each(fields, function(i, field){
//    variables[field.name.replace('input-@', '@')] = field.value;
//  });
//  
//  less.modifyVars(variables);
//  less.refreshStyles();
//};

// dynamically adding a CSS file

//var stylesheetFile = 'file.css';
//var link  = document.createElement('link');
//link.rel  = "stylesheet";
//link.type = "text/less";
//link.href = stylesheetFile;
//less.sheets.push(link);
//
//less.refresh();
