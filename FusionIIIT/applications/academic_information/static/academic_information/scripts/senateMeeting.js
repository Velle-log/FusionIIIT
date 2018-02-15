$(document).ready(function() {
    // On adding and deleting a meeting
    $('#senate-meeting').on('submit', function(event){
        event.preventDefault();
        $.ajax({
            type : "POST",
            url : "addMinute/",
            dataType: 'json',
            data : {
                'date' : $('#date').val(),
                'minutes_file' : $('#minutes_file').val()
            },
            success : function(data) {
                $('#date').val('');
                $('#minutes_file').val('');
                $("#senate_list").prepend("<tr><td>"+date.file_name+"</td><td>"+data.date+"</td><td></td><td></td></tr>");
                console.log("success");
            },
            error : function(data) {
                alert("Something went wrong");
            }
        });
    });   
});