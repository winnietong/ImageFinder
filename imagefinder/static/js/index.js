/**
* Created by winnie on 7/25/14.
*/


$(document).ready(function(){

    var page = 1;
    $("#searchButton").on('click', function(){
        $('#projects').html('');
        $('.search-heading').show();
        $('#seeMoreButton').show();
        $('#services').hide();

        pixabayGet(page);
    });

    function pixabayGet(page){
        var query = $("#search").val();
        // Should abstract out and save the pixabay url, your username, and key to reuse in calls down below as well
        PixabayURL = "http://pixabay.com/api/?username=tongwinnie&key=32fc5bc54bf1e1dbcb82&search_term=" + query +
            "&image_type=photo&page=" + page + "&per_page=10";
        console.log(PixabayURL);
        $.ajax({
            url: PixabayURL,
            type: "GET",
            dataType: "json",
            success: function(data) {
                console.log(data);
                for (i=0; i<10; i++){
                    imageInfo = {};
                    imageInfo = data.hits[i];
                    imageInfo.author = imageInfo.user;
                    imageInfo.imageURL = imageInfo.webformatURL;
                    imageInfo.thumbnailURL = imageInfo.imageURL;
                    imageInfo.api_id = imageInfo.id;
                    imageInfo.referrer = "Pixabay";
                    console.log(imageInfo);
                    showImage(imageInfo);
                }
            },
            error: function(response){
                console.log(response);
            }
        });
    }

    // print one image at a time
    function showImage(imageInfo){
        imageInfo = JSON.stringify(imageInfo);
        $.ajax({
            url: '/show_image/',
            type: 'POST',
            dataType: 'html',
            data: imageInfo,
            success: function(response) {
                $('#projects').append(response);
            },
            error: function(error_response) {
                console.log(error_response);
            }
        });
    }

    function saveImage(imageInfo){
        imageInfo = JSON.stringify(imageInfo);
        $.ajax({
            url: "/save_image/",
            type: "POST",
            dataType: 'html',
            data: imageInfo,
            success: function(response) {
                console.log("saved");
                console.log(response);
            },
            error: function(response) {
                console.log(response);
            }
        });
    }

    function unfavoriteImage(imageInfo){
        imageInfo = JSON.stringify(imageInfo);
        $.ajax({
            url: "/unfavorite_image/",
            type: "POST",
            dataType: 'html',
            data: imageInfo,
            success: function(response) {
                console.log("unfavorited!");
                console.log(response);
            },
            error: function(response) {
                console.log(response);
            }
        });
    }

    // STYLE ATTRIBUTES //
    $(document).on('mouseenter', '.portfolio-hover', function(){
        $(this).addClass('portfolio-cover');
    });

    $(document).on('mouseleave', '.portfolio-hover', function(){
        $(this).removeClass('portfolio-cover');
    });


    $(document).on('click', '.portfolio-hover', function(){
        console.log("clicked");
        imageURL = ($(this).attr('data-img-url'));
        $('.modal-body').children().attr('src', $(this).attr('data-img-url'));
//        $('.modal-title').text(" ");
        $('#downloadImage').attr('href', imageURL);
        $('#downloadImage').attr('download', imageURL);
    });

    // Favorite Logic
    $(document).on('click', '.glyphicon-heart-empty', function(){
        var id = $(this).parent().parent().data('id');
        $(this).removeClass('glyphicon-heart-empty');
        $(this).addClass('glyphicon-heart');
        var referrer = $(this).parent().parent().data('referrer');
        console.log(referrer);

        // It looks like you've already gotten all of these details your saving before about the pixabay image
        // You could save this image data in javascript and just retrieve it out of a hash based on the id
        // when a user clicks the favorite button instead of having to make another API call to pixabay
        if (referrer == "Pixabay"){
            url = "http://pixabay.com/api/?username=tongwinnie&key=32fc5bc54bf1e1dbcb82&id=" + id;
            imageInfo = {};
            $.ajax({
                url: url,
                type: "GET",
                dataType: "json",
                success: function (data) {
                    imageInfo = {};
                    imageInfo = data.hits[0];
                    imageInfo.title = "Pixabay Image";
                    imageInfo.apiURL = "http://pixabay.com/api/?username=tongwinnie&key=32fc5bc54bf1e1dbcb82&id=171646" +
                        imageInfo.id;
                    imageInfo.author = imageInfo.user;
                    imageInfo.imageURL = imageInfo.webformatURL;
                    imageInfo.thumbnailURL = imageInfo.previewURL;
                    imageInfo.api_id = imageInfo.id;
                    imageInfo.referrer = "Pixabay";
                    saveImage(imageInfo);
                },
                error: function (response) {
                    console.log(response);
                }
            });
        }
        else{
            console.log("Something went wrong");
        }
    });

    // Unfavorite Logic
    $(document).on('click', '.glyphicon-heart', function(){
        var id = $(this).parent().parent().data('id');
        var referrer = $(this).parent().parent().data('referrer');
        $(this).removeClass('glyphicon-heart');
        $(this).addClass('glyphicon-heart-empty');

        if (referrer == "Pixabay"){
            url = "http://pixabay.com/api/?username=tongwinnie&key=32fc5bc54bf1e1dbcb82&id=" + id;

            $.ajax({
                url: url,
                type: "GET",
                dataType: "json",
                success: function(data) {
                    unfavoriteImage(data.hits[0]);
                },
                error: function(response){
                    console.log(response);
                }
            });
            if(window.location.pathname == "/profile/") {
                $(this).parent().parent().parent().fadeOut('slow');
            }
        }
    });

    // Show More Button
    $(document).on('click', '#seeMoreButton', function(){
        console.log("clicked");
        page +=1;
        pixabayGet(page);
    });

});
