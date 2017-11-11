$(document).ready(function() {
    // On adding and deleting a new stdent basic profile
    $('#addBasicProfile').on('submit', function(event){
        event.preventDefault();
        $.ajax({
            type : "POST",
            url : "add_basic_profile/",
            dataType: 'json',
            data : {
                'name' : $('#studentName').val(),
                'batch' : $('#studentBatch').val(),
                'rollno' : $('#studentRollNo').val(),
                'phoneno' : $('#phoneNo').val(),
                'programme' : $('#studentProgramme').val()
            },
            success : function(data) {
                $('#name').val('');
                $('#batch').val('');
                $('#rollno').val('');
                $('#phoneno').val('');
                $('#programme').val('');
                $("#basic_profile_list").prepend("<tr><td>"+data.name+"</td><td>"+data.rollno+"</td><td>"+data.batch+"</td><td>"+data.programme+"</td><td></td>"+data.phoneno+"<td><button type='submit' value='{{ s.id }}' name='delete'><i class='trash outline icon' style='font-size:1.3vw;color:red;'></i></button></form></td></tr>");
                console.log("success");
            },
            error : function(data) {
                alert("Something went wrong");
            }
        });
    });

    $("#basic_profile_list").on('click', 'a[id^=remove-student-]', function(){
        var student_id = $(this).attr('id').split('-')[2];
        if (confirm('Are you sure you want to remove this student?')==true){
            $.ajax({
                url : "delete_basic_profile/"+student_id, // the endpoint
                type : "DELETE", // http method
                data : { 'student_id' : student_id }, // data sent with the delete request
                success : function(data) {
                  $('#student-'+student_id).hide(); // hide the post on success
                  alert("student removed");
                },
                error : function(xhr,errmsg,err) {
                    alert("Something went wrong");
                }
            });
        } else {
            return false;
        }
    });
});     