// initialize application when page loads

$(function () {
  // new theme link listener
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
  window.location.replace("/new_theme?n=" + themeName);
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