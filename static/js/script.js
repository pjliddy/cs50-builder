// initialize application when page loads

$(function () {
  // create application UI event listeners
  $('#category-select a').click(selectCategory);
//  $('[data-toggle="tooltip"]').tooltip();
  $('[data-toggle="popover"]').popover({
      container:'#config-panel'
    });
  $('.variable-display input').blur(updateVar);
});

function selectCategory( evt ){
  var category = $(this).data("value");
  console.log("/category?c=" + category);
  window.location.replace("/category?c=" + category);
};

function updateVar( evt ) {
  var newVal = $(this).val();
  console.log(newVal);
}
