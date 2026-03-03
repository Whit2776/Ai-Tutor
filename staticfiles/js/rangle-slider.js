(function ($) {
  "use strict";

  var rangestructural = function () {
    if ($("#slider-structural").length) {
      var dirSlider = document.getElementById("slider-structural");
      noUiSlider.create(dirSlider, {
        start: 7,
        connect: [true, false],
        range: {
          min: 0,
          max: 15,
        },
      });
      var dirVal = document.querySelector(".field-structural");
      dirSlider.noUiSlider.on("update", function (val, e) {
        dirVal.innerHTML = val[e];
      });
    }
  };

  var rangeweight = function () {
    if ($("#slider-weight").length) {
      var dirSlider = document.getElementById("slider-weight");
      noUiSlider.create(dirSlider, {
        start: 6.8,
        connect: [true, false],
        range: {
          min: 0,
          max: 15,
        },
      });
      var dirVal = document.querySelector(".field-weight");
      dirSlider.noUiSlider.on("update", function (val, e) {
        dirVal.innerHTML = val[e];
      });
    }
  };
  var consistency = function () {
    if ($("#consistency").length) {
      var dirSlider = document.getElementById("consistency");
      noUiSlider.create(dirSlider, {
        start: 1.4,
        connect: [true, false],
        range: {
          min: 0,
          max: 2,
        },
      });
      var dirVal = document.querySelector(".field-consistency");
      dirSlider.noUiSlider.on("update", function (val, e) {
        dirVal.innerHTML = val[e];
      });
    }
  };

  $(function () {

    rangestructural();
    rangeweight();
    consistency();
    
  });
})(jQuery);
