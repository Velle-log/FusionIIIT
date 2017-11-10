// On adding a new senate member
$(document).ready(function() {
    $('#senate-member').on('submit', function(event){
        event.preventDefault();
        create_member();
    });
});

//AJAX for adding the new senate member on the list
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
            $('#rollno').val(''); // remove the value from the input
            $("#senate_list").prepend("<tr id='senate-"+data.rollno+"'><td>"+data.name+"</td><td>"+data.programme+"</td><td>"+data.rollno+"</td><td><a id='delete-senate-"+data.rollno+"'><button>Remove</button></a></td></tr>");
            console.log("success"); //check
        },
        error : function(data) {
            alert("Something went wrong");
        }
    });
};

//on deleting the senate members
$(document).ready(function() {
    $("#senate_list").on('click', 'a[id^=remove-senate-]', function(){
        //alert($(this).attr('id').split('-')[2]);
        var senate_id = $(this).attr('id').split('-')[2];
        delete_senate(senate_id);
    });
});

// AJAX for deleting
function delete_senate(senate_id){
    if (confirm('Are you sure you want to remove this senate from the list?')==true){
        $.ajax({
            url : "deleteSenator/"+senate_id, // the endpoint
            type : "DELETE", // http method
            data : { senate_id : senate_id }, // data sent with the delete request
            success : function(data) {
              $('#senate-'+senate_id).hide(); // hide the post on success
              alert("senator removed");
            },
            error : function(xhr,errmsg,err) {
                alert("Something went wrong");
            }
        });
    } else {
        return false;
    }
};

    
    
       