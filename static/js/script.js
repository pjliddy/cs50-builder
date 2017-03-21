// initialize application when page loads

$(function () {
  // create application UI event listeners
  $('#category-select a').click(selectCategory);
  $('[data-toggle="popover"]').popover({
      container:'#config-panel'
    });
  $('#config-panel input').change(updateVar);
  //  $('#config-panel input').submit(function(e){ e.preventDefault(); updateVar();});

});

function selectCategory( evt ){
  var category = $(this).data("value");
//  console.log("/category?c=" + category);
  window.location.replace("/category?c=" + category);
};

function updateVar( evt ) {
  varName = $(this).closest(".variable-display").attr("id");
  varValue = $(this).val();
  message = {};
  message['@' + varName] = varValue;

  iframe = document.getElementById('layout');
  iframe.contentWindow.postMessage(message, '*');    
};
