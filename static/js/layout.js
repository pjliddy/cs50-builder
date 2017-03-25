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
    // replace with switch
    if (message == 'updateVars') {
      updateVars();
    } else if (message == 'updateCategory') {
      updateCategory(e.data.category);
    }
  }
};

function updateVars() {
  $.ajax({
    url: '/getvars',
    type: 'POST',
    success: function( varObjs ) {
      var vars = new Object;

      $.each( varObjs, function( i, varObj ) {
        vars['@' + varObj.name] = varObj.output;
      });

      less.modifyVars( vars );
      less.refreshStyles();
    },
    error: function(error) {
      console.log('error: ' + error);
    }
  });
};

function updateCategory(category) {      
  data = {'category':category }

  $.ajax({
    url: '/category',
    data: data,
    type: 'POST',
    success: function( response ) {
      // replace html in layout-content div
      $('.layout-content').html( response );
    },
    error: function(error) {
      console.log(error);
    }
  });
};