// initialize application when page loads

$(function () {
  // create application UI event listeners
  $('#category-select a').click(selectCategory);
  $('[data-toggle="popover"]').popover({
      container:'#config-panel'
    });
  
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
  
  // update theme data
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
