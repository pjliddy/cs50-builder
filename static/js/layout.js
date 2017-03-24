$(function () {
  // updateTheme when layout loads
  updateVars();
  window.addEventListener("message", handleMessage, false);
});

function handleMessage(e) {
//  console.log('message received:');
//  console.log(e.data);
  message = e.data.message;
  
  if (e.origin == '*') {
   return;
  } else {
    if (message == 'updateVars') {
      updateVars();
    } else if (message == 'updateCategory') {
      category = e.data.category;
      
      // UPDATE CONTENT FOR THIS CATEGORY
      
      data = {'category':category }
  
      // POST new category to server
      $.ajax({
        url: '/category',
        data: data,
        type: 'POST',
        success: function(response) {
          // use jquery to replace variables in #config-vars
          updateLayoutContent(response);
        },
        error: function(error) {
          console.log(error);
        }
      });
    }
  }
};

function updateVars() {
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

//      console.log(vars);
      less.modifyVars( vars );
      less.refreshStyles();
    },
    error: function(error) {
        console.log('error: ' + error);
    }
  });
};

function updateLayoutContent( content ){
//  console.log( $('.layout-content').html() );
  
  $('.layout-content').html( content );
};