// Submit post on submit
$(document).ready(function() {
    $('#senate-member').on('submit', function(event){
        create_member();
    });
});

function create_member() {
    $.ajax({
        type : "POST", // http method
        url : "senate/", // the endpoint
        dataType: 'json',
        data : {
            'rollno' : $('#rollno').val()
        },
        // data sent with the post request
        // handle a successful response
        success : function(data) {
            alert("success");
        },
        error : function(data) {
            alert("fail");
        }
    });
};
    
    
       