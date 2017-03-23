// initialize application when page loads

$(function ( ) {
  // save theme button listener
  $('#save-theme-btn').click(saveTheme);
  
  // new theme button listener
  $('#new-theme-btn').click(newTheme);
  // new theme name input field validation listener
  $('#theme-name-input').keyup(validateThemeNameInput);
  // create theme button post-validation listener
  $('#create-theme-btn').click(submitNewTheme);
  
  // create load theme button listener
  $('.load-theme-btn').click(loadTheme);
  // create delete theme button listener
  $('.delete-theme-btn').click(deleteTheme);
  // create confirm delete theme button listener
  $('#confirm-delete-btn').click(confirmDelete);
  
  // layout category selection menu item listener
  $('#category-select a').click(selectCategory);
  // variable config help text popover listener
  $('[data-toggle="popover"]').popover({ container:'#config-panel'});
  // variable config input field update listener
  $('#config-panel input').change(updateVar); 
  
  // set focus on new theme modal to theme name input
  $('#modal-new-theme').on('shown.bs.modal', function () {
    $('#theme-name-input').focus();
  });
  // set focus on delete theme modal to yes button
  $('#modal-delete').on('shown.bs.modal', function () {
    $('#confirm-delete-btn').focus();
  });
  
  // close category select when any click outside of it
  $(document).on('click',function(){
    $('#category-select').collapse('hide');
  })
});

function selectCategory( evt ){
  var category = $(this).data("value");
  
  updateConfigVars( category );
  
  // notify iframe to update its content with category
  iframe = document.getElementById('layout');
  data = {
    "message": "updateCategory",
    "category": category
  }
  iframe.contentWindow.postMessage(data, '*');
  
  $('#category-select').collapse("hide");
};

function updateVar( evt ) {
  varName = $(this).closest(".variable-display").attr("id");
  varValue = $(this).val();
  message = {
    [varName]: varValue
  };
  
  // tell server to update theme data IN DB
  $.ajax({
      url: '/update',
      data: message,
      type: 'POST',
      success: function(response) {
        // console.log(response);
        updateTheme('layout');
      },
      error: function(error) {
        console.log(error);
      }
  });
  
  

  // send message to iframe for update
//  iframe = document.getElementById('layout');
//  
//  data = {
//    "message": "updateVars"
//  }
//  
//  iframe.contentWindow.postMessage(message, '*');   
  
  // send message to iframe for update
//  iframe = document.getElementById('layout');
//  iframe.contentWindow.postMessage("updateVars", '*');
};

function newTheme( evt ) {
  // show the modal
  $('#modal-new-theme').modal('show');
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

// replace these with post commands?
function submitNewTheme( evt ) {
  themeName = $('#theme-name-input').val();
  window.location.replace("/new?n=" + themeName);
};

// replace these with post commands?
function loadTheme( evt ) {
  var value = $(this).data("value");
  window.location.replace("/load?id=" + value);
};

// replace these with post commands?
function deleteTheme( evt ) {
  var value = $(this).data("value");
  $('#modal-delete').attr('data-value', $(this).data("value"));
  $('#modal-delete').modal('show');
};

function confirmDelete( evt ) {
  var value = $('#modal-delete').data('value');
  window.location.replace("/delete?id=" + value);
};

// update theme layout in iframe

function updateTheme( layout ) {
  iframe = document.getElementById('layout');
  
  data = {
    "message": "updateVars"
  }
  
  iframe.contentWindow.postMessage(data, '*');
};

function updateConfigVars( category ) {
  message = {
    "category": category
  };
  
  $.ajax({
    url: '/config',
    data: message,
    type: 'POST',
    success: function(response) {
      // update category title
      $('.category-select-title').text(category);
      
      // change html of config-vars ui
      html = response;
      $('#config-vars').html( html );
      
      // update variable config input listener
      $('#config-panel input').change(updateVar); 
    },
    error: function(error) {
        console.log('error: ' + error);
    }
  });
};

function saveTheme( ) {
//  message = {
//    "category": category
//  };
  
  $.ajax({
    url: '/save',
    data: message,
    type: 'POST',
    success: function(response) {
      console.log('success: ' + error);
      // modal alert confirm
      alert("Theme saved!");
    },
    error: function(error) {
        console.log('error: ' + error);
    }
  });
};



