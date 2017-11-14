$(document).ready(function() {
    // On adding and deleting a senate member
    $('#senate-member').on('submit', function(event){
        event.preventDefault();
        $.ajax({
            type : "POST",
            url : "senator/",
            dataType: 'json',
            data : {
                'rollno' : $('#rollno').val()
            },
            success : function(data) {
                $('#rollno').val('');
                $("#senate_list").prepend("<tr id='senate-"+data.rollno+"'><td>"+data.name+"</td><td>"+data.programme+"</td><td>"+data.rollno+"</td><td><a id='delete-senate-"+data.rollno+"'><button>Remove</button></a></td></tr>");
                console.log("success");
            },
            error : function(data) {
                alert("Something went wrong");
            }
        });
    });

    $("#senate_list").on('click', 'a[id^=remove-senate-]', function(){
        var senate_id = $(this).attr('id').split('-')[2];
        if (confirm('Are you sure you want to remove this senate from the list?')==true){
            $.ajax({
                url : "deleteSenator/"+senate_id,
                type : "DELETE",
                data : { senate_id : senate_id },
                success : function(data) {
                  $('#senate-'+senate_id).hide();
                  alert("senator removed");
                },
                error : function(xhr,errmsg,err) {
                    alert("Something went wrong");
                }
            });
        } else {
            return false;
        }
    });

    // On adding and deleting co/convenor member
    $('#add-convenor').on('submit', function(event){
        event.preventDefault();
        $.ajax({
            type : "POST",
            url : "add_convenor/",
            dataType: 'json',
            data : {
                'rollno_convenor' : $('#rollno_convenor').val(),
                'designation' : $('#designation').val()
            },
            success : function(data) {
                $('#rollno_convenor').val('');
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
    });

    $("#convenor_list").on('click', 'a[id^=remove-convenor-]', function(){
        var convenor_id = $(this).attr('id').split('-')[2];
        delete_convenor(convenor_id);
    });
    $("#convenor_list").on('click', 'a[id^=remove-coconvenor-]', function(){
        var convenor_id = $(this).attr('id').split('-')[2];
        delete_convenor(convenor_id);
    });

    // On adding and deleting minute
    $('#minutes').on('submit', function(event){
        event.preventDefault();
        $.ajax({
            type : "POST", // http method
            url : "addMinute/", // the endpoint
            dataType: 'json',
            data : {
                'date' : $('#id_date').val(),
                'minutes_file' : $('#id_minutes_file').val()
            },
            // data sent with the post request
            // handle a successful response
            success : function(data) {
                $('#date').val(''); // remove the value from the input
                $('#minutes_file').val('')
                $("#minute_list").prepend("<tr id='minute-'><td>"+data.date+"</td><td></td><td>"+data.minutes_file+"</td><td><a id='delete-minute-'><button>Remove</button></a></td></tr>");
                console.log("success"); //check
            },
            error : function(data) {
                alert("Something went wrong");
            }
        });
    });
});

//function to delete co/convenor
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