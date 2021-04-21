$(document).ready(function () {
    // Init
    $('.image-section1').hide();
    $('#btn-predict').hide();
    $('#btn-download').hide();
    $('.loader').hide();
    $('#result').hide();
    $('.image-section2').hide();
    $('.duration').hide();

    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }

    $("#imageUpload").change(function () {
        $('.image-section1').show();
        $('#btn-predict').show();
        $('#btn-download').hide();
        $('#result').text('');
        $('#result').hide();
        $('.image-section2').hide();
        $('.duration').hide();
        readURL(this);
    });

    // Predict
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);
        // Show loading animation
        $(this).hide();
        $('.loader').show();
        var t0 =performance.now();
        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Get and display the result
                $('.loader').hide();
                $('.image-section2').show();
                $('#btn-predict').hide();
                var imgsrc= "static/js/Results/bg-removed-" + data;
                $('#imagePreview2').attr("src", imgsrc);
                console.log('Success!');
                $('#btn-download').show();
                var t1 =performance.now();
                var time = ((t1-t0)/1000).toFixed(2);
                document.getElementById("duration").innerHTML="Background removed from image in " + time + " seconds";
            },
        });
    });
});