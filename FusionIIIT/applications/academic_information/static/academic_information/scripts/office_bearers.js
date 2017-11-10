// On adding a new co/convenor
$(document).ready(function() {
    $('#add-convenor').on('submit', function(event){
        event.preventDefault();
        create_member();
    });
});

//AJAX for adding the new co/convenor member on the list
function create_member() {
    $.ajax({
        type : "POST", // http method
        url : "add_convenor/", // the endpoint
        dataType: 'json',
        data : {
            'rollno_convenor' : $('#rollno_convenor').val(),
            'designation' : $('#designation').val()
        },
        // data sent with the post request
        // handle a successful response
        success : function(data) {
            $('#rollno_convenor').val(''); // remove the value from the input
            $('#designation').val('');
            if(data.designation == 'Convenor'){
                $("#convenor_list").prepend("<tr id='convenor-"+data.rollno_convenor+"'><td>"+data.name+"</td><td>Convener</td><td>"+data.rollno_convenor+"</td><td><a id='remove-convenor-"+data.rollno_convenor+"'><button>Remove</button></a></td></tr>");
            }
            else{
                $("#convenor_list").prepend("<tr id='coconvenor-"+data.rollno_convenor+"'><td>"+data.name+"</td><td>Co Convener</td><td>"+data.rollno_convenor+"</td><td><a id='remove-coconvenor-"+data.rollno_convenor+"'><button>Remove</button></a></td></tr>");
            }     
        },

        error : function(data) {
            alert("Something went wrong");
        }
    });
};

//on deleting the co/convenor members
$(document).ready(function() {
    $("#convenor_list").on('click', 'a[id^=remove-convenor-]', function(){
        var convenor_id = $(this).attr('id').split('-')[2];
        delete_convenor(convenor_id);
    });
    $("#convenor_list").on('click', 'a[id^=remove-coconvenor-]', function(){
        var convenor_id = $(this).attr('id').split('-')[2];
        delete_convenor(convenor_id);
    });
});

// AJAX for deleting
function delete_convenor(convenor_id){
    if (confirm('Are you sure you want to remove this student from the list?')==true){
        $.ajax({
            url : "deleteConvenor/"+convenor_id, // the endpoint
            type : "DELETE", // http method
            data : { convenor_id : convenor_id }, // data sent with the delete request
            success : function(data) {
                if(data.designation == "Convenor")
                    $('#convenor-'+data.id).hide(); // hide the post on success
                else
                    $('#coconvenor-'+data.id).hide();
                alert("Removed");
            },
            error : function(xhr,errmsg,err) {
                alert("Something went wrong");
            }
        });
    } else {
        return false;
    }
};

    
    
       