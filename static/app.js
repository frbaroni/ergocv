(function() {
    function updateImg() {
        $('#img').attr('src', '/image?' + (new Date()).toISOString());
    }
    function autoUpdateImg() {
                updateImg();
                setTimeout(autoUpdateImg, 2000);
    }
    autoUpdateImg();
})();
