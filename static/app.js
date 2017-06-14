(function() {

    function updateImg() {
        //$('#img').attr('src', '/image?' + (new Date()).toISOString());
    }

    function autoUpdateImg() {
                updateImg();
                setTimeout(autoUpdateImg, 2000);
    }

    autoUpdateImg();

    new Vue({
      el: '#content',
      data: {
        frequency: 5000,
        camera: 0,
        image_url: '/image',
        cameraSelectorIndexes: [],
        cameraSelectorShow: false
      },
      methods: {
        selectCamera: function() {
          var vm = this;
          vm.cameraSelectorShow: false;
          axios
            .get('/camera/indexes')
            .then(function(response) {
              vm.cameraSelectorIndexes = response.data['cameras'];
              vm.cameraSelectorShow = true;
            });
        }
      }
    });
})();
