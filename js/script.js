// initialize application when page loads

$(function () {
  // create UI event listeners
  $('#category-select a').click(selectCategory);
});

function selectCategory( evt ){
  var category = $(this).data("value");
  console.log(category);
};
