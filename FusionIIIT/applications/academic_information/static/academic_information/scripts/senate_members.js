// Submit post on submit
$(document).ready(function() {
    $('#senate-member').on('submit', function(event){
        create_member();
    });
});

function create_member() {
    $.ajax({
        type : "POST", // http method
        url : "senator/", // the endpoint
        dataType: 'json',
        data : {
            'rollno' : $('#rollno').val()
        },
        // data sent with the post request
        // handle a successful response
        success : function(data) {
            alert("New Senator Added");
        },
        error : function(data) {
            alert("Something went wrong");
        }
    });
};
    
    
       