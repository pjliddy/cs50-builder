// initialize application when page loads

$(function () {
  // create application UI event listeners
  $('#category-select a').click(selectCategory);
  $('[data-toggle="popover"]').popover({
      container:'#config-panel'
    });
  
  $('#config-panel input').change(updateVar);
  $('#new-theme').click(newTheme);
  $('#theme-name-input').keyup(validateThemeNameInput);
  $('#create-theme-btn').click(submitNewTheme);
});

function selectCategory( evt ){
  var category = $(this).data("value");
  
  // should be refreshing page (through flask), not reloading
  
  window.location.replace("/category?c=" + category);
};

function updateVar( evt ) {
  varName = $(this).closest(".variable-display").attr("id");
  varValue = $(this).val();
  message = {
    [varName]: varValue
  };
  
  // tell server to update theme data
  $.ajax({
      url: '/update',
      data: message,
      type: 'POST',
      success: function(response) {
        console.log(response);
      },
      error: function(error) {
        console.log(error);
      }
  });

//  // send message to iframe for update
//  iframe = document.getElementById('layout');
//  iframe.contentWindow.postMessage(message, '*');   
  
  // send message to iframe for update
  iframe = document.getElementById('layout');
  iframe.contentWindow.postMessage("updateVars", '*');
};

function newTheme( evt ) {
  // show the modal
  $('#modal-private').modal('show');
};

function validateThemeNameInput( evt ) {
  if ($('#theme-name-input').val().length > 0) {
    // enable button
    $('#create-theme-btn').prop('disabled', false);
  } else {
    // disable button
    $('#create-theme-btn').prop('disabled', true);
  }
};

function submitNewTheme( evt ) {
  themeName = $('#theme-name-input').val();
  window.location.replace("/new_theme?n=" + themeName);
  // tell server to update theme data
//  $.ajax({
//      url: '/update',
//      data: message,
//      type: 'POST',
//      success: function(response) {
//        console.log(response);
//      },
//      error: function(error) {
//        console.log(error);
//      }
//  });
};

  // let validator make sure form fields are valid  
//  $('#theme-name-form').validator().on('submit', function( evt ) {
//    if (! evt.isDefaultPrevented()) {
//      // form is good
//      var theme_name = $('#theme-name').val();
//      console.log(theme_name)
//      var path = '/new_theme?n=' + theme_name;
//      console.log(path)
//      $('#modal-private').modal('hide');
//      window.location.replace(path);
//    }
//  });

//      $.ajax({
//        url: '/new_theme',
//        data: {'theme_name':theme_name },
//        type: 'POST',
//        success: function(response) {
//          // go to new theme page 
//          console.log(response);
//          
//        },
//        error: function(error) {
//          console.log('error: ' + error);
//        }
//      });


//function validateThemeName( evt ) {
//  var theme_name = $('#theme-name').val();
//  
//  if (theme_name){
//    console.log('post: ' + theme_name)
//    // tell server to validate
//    $.ajax({
//        url: '/new_theme',
//        data: {'theme_name':theme_name },
//        type: 'POST',
//        success: function(response) {
//          console.log('new:' + response);
//        },
//        error: function(error) {
//          console.log('error: ' + error);
//        }
//    });
//  };
//};

